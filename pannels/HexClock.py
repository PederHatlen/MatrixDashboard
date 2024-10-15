import datetime, functions
from PIL import Image, ImageFont, ImageDraw

small10 = ImageFont.truetype(f"{functions.PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

current = 0
total = 1

def dial(e):
    global current, total
    if e == "1H": current = (current+1 if current < total else 0)
    elif e == "1L": current = (current-1 if current > 0 else total)

def get(ts):
    now = datetime.datetime.now()

    hexTime = ""
    if current == 0: hexTime = f"#{str(now.hour).rjust(2,'0')}{str(now.minute).rjust(2,'0')}{str(now.second).rjust(2,'0')}"                         # Clock as color
    if current == 1:   hexTime = f"#{round((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()*100):0>6X}".upper()       # Milliseconds -> Hex

    im = Image.new(mode="RGB", size=(64, 32), color=hexTime)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"

    d.text((5,5), hexTime, font=small05, fill=(255,255,255))

    return functions.PIL2frame(im)