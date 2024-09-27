import requests, time, json
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from functions import *
from threading import Thread

small10 = ImageFont.truetype(f"{PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{PATH}/fonts/small05.ttf", 5)
icons06 = ImageFont.truetype(f"{PATH}/fonts/icons.ttf", 7)

covers = {}
olddata = {"playing":False, "time":0, "data":{}}

with open(f"{PATH}/spotifysecrets.json", "r") as fi:
    spotySecrets = json.load(fi)

def getDaToken():
    if "runout" not in spotySecrets or spotySecrets["runout"] < time.time():
        response = requests.request("POST", "https://accounts.spotify.com/api/token", data={'grant_type':'refresh_token','refresh_token':spotySecrets["refresh_token"]}, headers={'Authorization':f'Basic {spotySecrets["the_code"]}','Content-Type':'application/x-www-form-urlencoded'}).json()
        spotySecrets["access_token"] = response["access_token"]
        spotySecrets["runout"] = (int(time.time()) + response["expires_in"] - 10)
    return spotySecrets["access_token"]

def askSpotify(endpoint): return requests.get(endpoint, headers={'Authorization':f'Bearer {getDaToken()}'})

def getNewData():
    response = askSpotify("https://api.spotify.com/v1/me/player")
    olddata["time"] = time.time()
    if response.status_code != 200:
        askSpotify("https://api.spotify.com/v1/me/player/play")
        olddata["playing"] = False
        return
    currentlyPlaying = response.json()
    print(currentlyPlaying)
    olddata["playing"] = currentlyPlaying["is_playing"]
    olddata["data"] = currentlyPlaying

def play():
    response = requests.put("https://api.spotify.com/v1/me/player/play", headers={'Authorization':f'Bearer {getDaToken()}'})
    if response.status_code == 200:
        olddata["playing"] = True
        print("Playing")
    else: print(f"Error: {response.status_code}")
def pause():
    response = requests.put("https://api.spotify.com/v1/me/player/pause", headers={'Authorization':f'Bearer {getDaToken()}'})
    if response.status_code == 200:
        olddata["playing"] = False
        print("Paused")
    else: print(f"Error: {response.status_code}")

def toggle(): (pause() if olddata["playing"] else play())

def get(frame):
    global olddata
    global covers
    
    if olddata["time"] < time.time()-10: getNewData()

    currentlyPlaying = olddata["data"]

    coverURL = currentlyPlaying["item"]["album"]["images"][0]["url"]


    if coverURL not in covers:
        covers[coverURL] = Image.open(requests.get(currentlyPlaying["item"]["album"]["images"][-1]["url"], stream=True).raw).resize((32,32))
        if len(covers) > 20: covers = covers[-20:]

    im = Image.new(mode="RGB", size=(64, 32))
    infoArea = Image.new(mode="RGB", size=(30,30))

    info = ImageDraw.Draw(infoArea)
    info.fontmode = "1"

    titlelength = small05.getlength(f'{currentlyPlaying["item"]["name"]}    ')

    if titlelength > 32: info.text((-int(frame%(max(titlelength, 32))),0), "    ".join([currentlyPlaying["item"]["name"]]*3), font=small05, fill=(255,255,255))
    else: info.text((0,0), currentlyPlaying["item"]["name"], font=small05, fill="#fff")

    artists = "    ".join([e["name"] for e in currentlyPlaying["item"]["artists"]])
    artistlength = small05.getlength(f"{artists}    ")
    if artistlength > 32: info.text((-int(frame%(max(artistlength, 32))),8), f"{artists}    {artists}", font=small05, fill="#888")
    else: info.text((0,8), artists, font=small05, fill="#888")

    progress = ((currentlyPlaying["progress_ms"]+((time.time()-olddata["time"]) if olddata["playing"] else 0)*1000)/currentlyPlaying["item"]["duration_ms"])
    info.line([(0,29),(29,29)], fill="#fff", width=1)
    info.line([(0,29),(round(progress*30),29)], fill="#1ed760", width=1)

    info.text((12, 20), text=("1" if olddata["playing"] else "0"), font=icons06, fill="#1ed760")

    im.paste(covers[coverURL], (0,0))
    im.paste(infoArea, (33,1))

    return [[rgb2hex(y) for y in x] for x in np.array(im).tolist()]
