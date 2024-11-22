import datetime, docker, os, psutil
from PIL import Image, ImageFont, ImageDraw
from functions import *

small05 = ImageFont.truetype(f"{PATH}/fonts/small05.ttf", 5)

isRoot = (os.geteuid() == 0)
if isRoot: client = docker.from_env()

def get(ts):
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)  
    d.fontmode = "1"

    # d.point([(n,0) for n in range(1,64,2)] + [(0,n) for n in range(1,32,2)], fill="#f00")

    d.text((0, 0), "CPU", fill="#fff", font=small05)
    d.text((0, 7), "TMP", fill="#fff", font=small05)
    d.text((0, 14), "FAN", fill="#fff", font=small05)

    cpu = psutil.cpu_percent()
    temp = round(psutil.sensors_temperatures()['cpu_thermal'][0].current)
    fan = round((psutil.sensors_fans()['pwmfan'][0].current/8000)*100)

    cpuColor  = (color["green"] if cpu < 25 else (color["orange"] if cpu < 75 else color["red"]))
    tempColor = (color["green"] if temp < 50 else (color["orange"] if temp < 80 else color["red"]))
    fanColor  = (color["blue"] if fan < 10 else (color["green"] if fan < 50 else (color["orange"] if fan < 75 else color["red"])))

    d.text((32 - small05.getlength(f"{cpu}%"),0), f"{cpu}%", font=small05, fill=cpuColor)
    d.text((32 - small05.getlength(f"{temp}C"),7), f"{temp}C", font=small05, fill=tempColor)
    d.text((32 - small05.getlength(f"{fan}%"),14), f"{fan}%", font=small05, fill=fanColor)

    if isRoot:
        d.text((0, 27), "HA", fill="#fff", font=small05)
        has = client.containers.get("homeassistant").attrs["State"]["Running"]
        if has: d.text((24,27), "UP", font=small05, fill=color["green"])
        else: d.text((13,27), "DOWN", font=small05, fill=color["red"])

    return PIL2frame(im)