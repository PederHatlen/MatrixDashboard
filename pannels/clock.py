import datetime
import numpy as np
from functions import *
from PIL import Image, ImageFont, ImageDraw

small10 = ImageFont.truetype(f"{PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{PATH}/fonts/small05.ttf", 5)

def get():
    now = datetime.datetime.now()

    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)  
    d.fontmode = "1"

    d.text((0,0), ":".join([str(now.hour).rjust(2,"0"), str(now.minute).rjust(2,"0"), str(now.second).rjust(2,"0")]), font=small10, fill=(255,255,255))
    d.text((0,11), ":".join([str(now.hour).rjust(2,"0"), str(now.minute).rjust(2,"0"), str(now.second).rjust(2,"0")]), font=small05, fill=(255,255,255))

    return [[rgb2hex(y) for y in x] for x in np.array(im).tolist()]