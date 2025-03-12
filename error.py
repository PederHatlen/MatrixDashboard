from PIL import Image, ImageDraw
from functions import *

large10 = font["large10"]

im = Image.new(mode="RGB", size=(64, 32))
d = ImageDraw.Draw(im)  
d.fontmode = "1"


d.text((32,16), "ERROR!", font=large10, anchor="mm", fill=color["lightred"])

def get(): return im