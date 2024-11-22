from PIL import Image, ImageFont, ImageDraw
from functions import *

small05 = ImageFont.truetype(f"{PATH}/fonts/small05.ttf", 5)

def get(ts):
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)  
    d.fontmode = "1"

    d.multiline_text((0,0), "Nothing to see \nhere", font=small05)

    return PIL2frame(im)