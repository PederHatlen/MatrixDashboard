import datetime, requests, json, textwrap
from PIL import Image, ImageDraw, ImageEnhance
from functions import *
import numpy as np

small05 = font["small05"]

needsRendering = False

lfn = 0
expires = datetime.datetime.now(tz=datetime.timezone.utc)
dataCuttof = datetime.datetime.now(tz=datetime.timezone.utc)

lat, long = 63.4224, 10.4320 # Trondheim Norway

def contrast(img, level=1.25): return ImageEnhance.Contrast(img).enhance(level)

# Weather icons from YR
with open("./weatherIcons.json", "r") as fi: weatherIcons = json.load(fi)
icons = {e:contrast(Image.open(f"./weatherIcons/{weatherIcons[e]['code']}.png")).resize((16,16), Image.Resampling.HAMMING) for e in weatherIcons.keys()}
iconsSmall = {e:contrast(Image.open(f"./weatherIcons/{weatherIcons[e]['code']}.png")).resize((8,8), Image.Resampling.HAMMING) for e in weatherIcons.keys()}

# Icons for current events
LB = hex2rgb(color["lightblue"])
WC, GC, BC = (255,255,255), (100,100,100), (0,0,0)
rainIcon = Image.fromarray(np.array([[LB,BC,BC,BC,LB],[LB,BC,LB,BC,BC],[BC,BC,LB,BC,LB],[LB,BC,BC,BC,LB],[LB,BC,LB,BC,BC],[BC,BC,LB,BC,BC]], dtype=np.uint8), 'RGB')
cloudIcon = Image.fromarray(np.array([
    [BC,WC,WC,BC,BC,BC],
    [WC,WC,WC,WC,WC,BC],
    [WC,WC,WC,WC,WC,WC],
    [WC,WC,WC,WC,WC,WC]], dtype=np.uint8), 'RGB')
windIcon = Image.fromarray(np.array([[BC,BC,WC,GC,BC],[GC,GC,WC,GC,BC],[WC,WC,WC,WC,WC],[BC,GC,WC,GC,GC],[BC,GC,WC,BC,BC]], dtype=np.uint8), 'RGB')

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
    
def get_current_hour(t):
    global data
    for d in data["properties"]["timeseries"]:
        if d["time"][:13] == t.isoformat()[:13]:
            return d["data"]
        
def get_cuttof(data):
    for d in data["properties"]["timeseries"]:
        if not set({"next_12_hours", "next_6_hours", "next_1_hours"}).issubset(set(d["data"].keys())):
            return datetime.datetime.fromisoformat(d["time"])
        
def wantsRender(last):
    global needsRendering
    if datetime.datetime.now(tz=datetime.timezone.utc) > expires: return True
    if last.hour != datetime.datetime.now().hour: return True
    if needsRendering:
        needsRendering = False
        return True

# dn = 0
# def dial(e):
#     global dn
#     if e == "2R": dn+=1
#     elif e == "2L": dn-=1

offsetH = 0
def dial(e):
    global data, dataCuttof, offsetH
    if e == "1R" and dataCuttof > datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=offsetH+1):
        offsetH+=1 
    elif e == "1L" and offsetH > 0:
        offsetH-=1

def btn():
    global offsetH
    offsetH = 0

data = {}
def get(fn = 0):
    global data, lfn, weatherIcons, expires, dataCuttof

    if datetime.datetime.now(tz=datetime.timezone.utc) > expires: 
        data = get_data()
        dataCuttof = get_cuttof(data)
    
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"

    if data == {}: return PIL2frame(im)

    now = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=offsetH)
    currentHour = get_current_hour(now)

    # im.paste(icons[list(weatherIcons.keys())[dn//1 % len(weatherIcons.keys())]], (1, 1))
    # im.paste(icons1[list(weatherIcons.keys())[dn//1 % len(weatherIcons.keys())]], (18, 1))

    # im.paste(iconsSmall[list(weatherIcons.keys())[dn//1 % len(weatherIcons.keys())]], (18, 7))
    # im.paste(iconsSmall1[list(weatherIcons.keys())[dn//1 % len(weatherIcons.keys())]], (27, 7))

    if offsetH == 0: im.paste(icons[currentHour['next_1_hours']['summary']['symbol_code']], (1, 1))
    else:
        im.paste(iconsSmall[currentHour['next_1_hours']['summary']['symbol_code']], (5, 7))
        d.text((1, 1), f"+{offsetH}", font=small05, fill=color["lightred"])

    im.paste(iconsSmall[currentHour['next_6_hours']['summary']['symbol_code']], (18, 7))
    im.paste(iconsSmall[currentHour['next_12_hours']['summary']['symbol_code']], (27, 7))

    d.text((18, 1), "06", font=small05, fill=color["orange"])
    d.text((27, 1), "12", font=small05, fill=color["orange"])

    description = "\n".join(textwrap.wrap(weatherIcons[currentHour['next_1_hours']['summary']['symbol_code']]["description"], int(40//small05.getlength("A")), break_long_words=False))
    # description = "\n".join(textwrap.wrap(weatherIcons[list(weatherIcons.keys())[dn//1 % len(weatherIcons.keys())]]["description"], width=int(40//small05.getlength("A")), break_long_words=False))

    temp = currentHour["instant"]["details"]["air_temperature"]
    percipation = str(currentHour["next_1_hours"]["details"]["precipitation_amount"])
    clouds = f'{str(round(currentHour["instant"]["details"]["cloud_area_fraction"]))}%'
    wind = f'{str(currentHour["instant"]["details"]["wind_speed"])}'

    d.text((56 - small05.getlength(str(temp)), 1), str(temp), font=small05)
    d.text((56 - small05.getlength(str(percipation)), 8), str(percipation), font=small05)
    d.text((56 - small05.getlength(str(clouds)), 15), str(clouds), font=small05)
    d.text((56 - small05.getlength(str(wind)), 22), str(wind), font=small05)

    d.text((56, 1), "°C", font=small05, fill=(color["lightblue"] if temp < 0 else color["lightred"]))
    im.paste(rainIcon, (57, 8))
    im.paste(cloudIcon, (57, 15))
    im.paste(windIcon, (57, 22))

    d.multiline_text((1, (20 if "\n" in description else 26)), description, font=small05, spacing=1)
    
    return im
