import datetime
from PIL import Image, ImageDraw
import functions

small05 = functions.font["small05"]

current = 0
total = 1

def dial(e):
    global current, total
    if e == "1R": current = (current+1 if current < total else 0)
    elif e == "1L": current = (current-1 if current > 0 else total)

def get():
    now = datetime.datetime.now()

    hexTime = ""
    if current == 0: hexTime = f"#{str(now.hour).rjust(2,'0')}{str(now.minute).rjust(2,'0')}{str(now.second).rjust(2,'0')}"                         # Clock as color
    if current == 1: hexTime = f"#{round((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()*100):0>6X}".upper()       # Milliseconds -> Hex

    im, d = functions.getBlankIM()
    d.rectangle((0,0,64,32), fill=hexTime)
    d.text((5,5), hexTime, font=small05, fill=(255,255,255))

    return im