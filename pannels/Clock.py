import datetime, functions
from PIL import Image, ImageFont, ImageDraw

small10 = ImageFont.truetype(f"{functions.PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

def get(ts):
    now = datetime.datetime.now()

    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)  
    d.fontmode = "1"

    d.text((5,5), ":".join([str(now.hour).rjust(2,"0"), str(now.minute).rjust(2,"0"), str(now.second).rjust(2,"0")]), font=small10, fill=(255,255,255))
    # d.text((0,11), ":".join([str(now.hour).rjust(2,"0"), str(now.minute).rjust(2,"0"), str(now.second).rjust(2,"0")]), font=small05, fill=(255,255,255))

    return functions.PIL2frame(im)