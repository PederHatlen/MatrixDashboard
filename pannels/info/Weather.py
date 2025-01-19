import datetime, requests, json, textwrap, locale
from PIL import Image, ImageDraw
from functions import *
import numpy as np

small05 = font["small05"]

lfn = 0
expires = datetime.datetime.now(tz=datetime.timezone.utc)

lat, long = 63.4224, 10.4320 # Trondheim Norway

# Weather icons from YR
with open("./weatherIcons.json", "r") as fi: weatherIcons = json.load(fi)
icons = {e:Image.open(f"./weatherIcons/{weatherIcons[e]['code']}.png").resize((16,16)) for e in weatherIcons.keys()}

LC, BC = hex2rgb(color["lightblue"]), (0,0,0)
# Percipation icon
rainIcon = Image.fromarray(np.array([[LC,BC,BC,BC,LC],[LC,BC,LC,BC,BC],[BC,BC,LC,BC,LC],[LC,BC,BC,BC,LC],[LC,BC,LC,BC,BC],[BC,BC,LC,BC,BC]], dtype=np.uint8), 'RGB')

def get_data():
    global expires
    headers = {'User-Agent':'https://github.com/PederHatlen/MatrixDashboard email:pederhatlen@gmail.com',}
    response = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={round(lat,4)}&lon={round(long,4)}",headers=headers)
    try: expires = datetime.datetime.strptime(response.headers["Expires"][:-4], "%a, %d %b %Y %H:%M:%S", ).replace(tzinfo=datetime.timezone.utc)
    except Exception as E:
        print(E)
        expires = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=4)
        print("Could not parse expiration time (using +4 hours) Error: {E}")
    print(f"Got new weatherdata, expiration: {expires}")
    return response.json()

def get_data_fake():
    global expires
    with open("./tempWeather.json") as fi:
        data = json.load(fi)
        print("Faked new data")
        expires = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=2)
        return data
    
def get_current_hour(data, t):
    for d in data["properties"]["timeseries"]:
        if d["time"][:13] == t.isoformat()[:13]:
            return d["data"]

# dn = 0
# def dial(e):
#     global dn
#     if e == "2H": dn+=1
#     elif e == "2L": dn-=1

data = {}
def get(fn):
    global data, lfn, weatherIcons, expires

    if datetime.datetime.now(tz=datetime.timezone.utc) > expires: 
        data = get_data()
    
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"

    if data == {}: return PIL2frame(im)

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    currentHour = get_current_hour(data, now)

    # im.paste(icons[list(weatherIcons.keys())[fn//1 % len(weatherIcons.keys())]], (1, 1))
    # im.paste(icons[list(weatherIcons.keys())[fn//1 % len(weatherIcons.keys())]].resize((8,8)), (18, 7))
    # im.paste(icons[list(weatherIcons.keys())[fn//1 % len(weatherIcons.keys())]].resize((8,8)), (27, 7))
    im.paste(icons[currentHour['next_1_hours']['summary']['symbol_code']], (1, 1))
    im.paste(icons[currentHour['next_6_hours']['summary']['symbol_code']].resize((8,8)), (18, 7))
    im.paste(icons[currentHour['next_12_hours']['summary']['symbol_code']].resize((8,8)), (27, 7))

    d.text((18, 1), "06", font=small05)
    d.text((27, 1), "12", font=small05)

    description = "\n".join(textwrap.wrap(weatherIcons[currentHour['next_1_hours']['summary']['symbol_code']]["description"], int(64//small05.getlength("A"))))
    # description = "\n".join(textwrap.wrap(weatherIcons[list(weatherIcons.keys())[fn//1 % len(weatherIcons.keys())]]["description"], int(44//small05.getlength("A"))))
    temp = currentHour["instant"]["details"]["air_temperature"]
    # temp = -25.5
    percipation = str(currentHour["next_1_hours"]["details"]["precipitation_amount"])

    d.text((56 - small05.getlength(str(temp)), 1), str(temp), font=small05)
    d.text((56 - small05.getlength(str(percipation)), 8), str(percipation), font=small05)

    d.text((56, 1), "°C", font=small05, fill=(color["lightblue"] if temp < 0 else color["lightred"]))
    im.paste(rainIcon, (58, 8))

    d.multiline_text((1, 20), description, font=small05, spacing=1)
    
    return PIL2frame(im)
