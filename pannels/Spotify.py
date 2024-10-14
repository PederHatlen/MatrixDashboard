import requests, time, json, base64, functions, datetime
from PIL import Image, ImageFont, ImageDraw


"""
TO USE THIS INTEGRATION:
You need a Spotify developer app (https://developer.spotify.com/dashboard)
Get a refresh token, client id, and client secret
    The two last can be retrieved from the spotify app you have made
    You can get a refresh token by completing the Oauth2 initiation ritual
all these needs to be added to the json file "spotifysecrets.json" in the root of the project (where the main.py file is)

"""

small10 = ImageFont.truetype(f"{functions.PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)
icons06 = ImageFont.truetype(f"{functions.PATH}/fonts/icons.ttf", 7)

spotifyColor = "#1ed760"
scrollSpeed = 0.5 # (pixel/100ms)

prev_dial_turn = 0

covers = {}
olddata = {"playing":False, "time":0, "data":{}}
oldTS = 0

spotySecrets = {}

with open(f"{functions.PATH}/spotifysecrets.json", "r") as fi:
    file = json.load(fi)
    spotySecrets["refresh_token"] = file["refresh_token"]
    spotySecrets["Authorization"] = base64.b64encode("".join([file["client_id"], ":", file["client_secret"]]).encode("ascii")).decode("ascii")

def getDaToken():
    if "runout" not in spotySecrets or spotySecrets["runout"] < time.time():
        data = {
            'grant_type':'refresh_token',
            'refresh_token':spotySecrets["refresh_token"]
        }
        headers = {
            'Authorization':f'Basic {spotySecrets["Authorization"]}',
            'Content-Type':'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", "https://accounts.spotify.com/api/token", data=data, headers=headers).json()
        spotySecrets["access_token"] = response["access_token"]
        spotySecrets["runout"] = (int(time.time()) + response["expires_in"] - 10)
    return spotySecrets["access_token"]

def get_data():
    global olddata
    olddata["time"] = time.time()
    try: response = requests.get("https://api.spotify.com/v1/me/player", headers={'Authorization':f'Bearer {getDaToken()}'})
    except requests.exceptions.ConnectionError:
        print("Couldnt connect to internet")
        olddata["playing"] = False
        return
    if response.status_code != 200:
        print("Not playing annything")
        olddata["playing"] = False
        return
    currentlyPlaying = response.json()
    print(currentlyPlaying)
    olddata["playing"] = currentlyPlaying["is_playing"]
    olddata["data"] = currentlyPlaying

def next():
    response = requests.post("https://api.spotify.com/v1/me/player/next", headers={'Authorization':f'Bearer {getDaToken()}'})
    if response.status_code == 200: get_data()
    else: print(f"Error: {response.status_code}")
def previous():
    response = requests.post("https://api.spotify.com/v1/me/player/previous", headers={'Authorization':f'Bearer {getDaToken()}'})
    if response.status_code == 200: get_data()
    else: print(f"Error: {response.status_code}")
def play():
    response = requests.put("https://api.spotify.com/v1/me/player/play", headers={'Authorization':f'Bearer {getDaToken()}'})
    if response.status_code == 200: olddata["playing"] = True
    else: print(f"Error: {response.status_code}")
def pause():
    response = requests.put("https://api.spotify.com/v1/me/player/pause", headers={'Authorization':f'Bearer {getDaToken()}'})
    if response.status_code == 200: olddata["playing"] = False
    else: print(f"Error: {response.status_code}")

def btn(): (pause() if olddata["playing"] else play())

def dial(e):
    global prev_dial_turn
    if prev_dial_turn > datetime.datetime.now().timestamp() - 1: return
    prev_dial_turn = datetime.datetime.now().timestamp()
    
    if e == "2H": next()
    elif e == "2L": previous()

def get(fn):
    global olddata, covers
    
    # Get new data from spotify every 10 seconds
    if olddata["time"] < time.time()-10: get_data()

    # If the song just ended, get new data
    elif (olddata["playing"] and (olddata["data"]["progress_ms"]+(time.time()-olddata["time"])*1000)-100 >= olddata["data"]["item"]["duration_ms"]):
        get_data()

    im = Image.new(mode="RGB", size=(64, 32))

    # If you are not playing annything on spotify return black screen
    if olddata["data"] == {}:
        return functions.PIL2frame(im)

    # Set localdata to stored data
    currentlyPlaying = olddata["data"]

    # get the cover url, and download it if not allready
    coverURL = currentlyPlaying["item"]["album"]["images"][0]["url"]
    if coverURL not in covers:
        covers[coverURL] = Image.open(requests.get(currentlyPlaying["item"]["album"]["images"][-1]["url"], stream=True).raw).resize((32,32))
        if len(covers) > 20: covers = covers[-20:]

    infoArea = Image.new(mode="RGB", size=(30,30))
    info = ImageDraw.Draw(infoArea)
    info.fontmode = "1"

    titlelength = small05.getlength(f'{currentlyPlaying["item"]["name"]}    ')

    if titlelength > 32: 
        textPos = (-int((fn*scrollSpeed)%(max(titlelength, 32))),0)
        info.text(textPos, "    ".join([currentlyPlaying["item"]["name"]]*3), font=small05, fill=(255,255,255))
    else: info.text((0,0), currentlyPlaying["item"]["name"], font=small05, fill="#fff")
    
    artists = "    ".join([e["name"] for e in currentlyPlaying["item"]["artists"]])
    artistlength = small05.getlength(f"{artists}    ")
    if artistlength > 32:
        textPos = (-int((fn*scrollSpeed)%(max(artistlength, 32))),8)
        info.text(textPos, f"{artists}    {artists}", font=small05, fill="#888")
    else: info.text((0,8), artists, font=small05, fill="#888")

    progress = ((currentlyPlaying["progress_ms"]+((time.time()-olddata["time"]) if olddata["playing"] else 0)*1000)/currentlyPlaying["item"]["duration_ms"])
    info.line([(0,29),(29,29)], fill="#fff", width=1)
    info.line([(0,29),(round(progress*30),29)], fill=spotifyColor, width=1)

    info.text((12, 20), text=("1" if olddata["playing"] else "0"), font=icons06, fill=spotifyColor)

    im.paste(covers[coverURL], (0,0))
    im.paste(infoArea, (33,1))

    return functions.PIL2frame(im)