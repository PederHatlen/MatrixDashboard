from PIL import Image, ImageDraw
from functions import *

small05 = font["small05"]

def get(fn = 0):
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"

    d.multiline_text((1,1), "ABCDEFGHIJKLMNO\nPQRSTUVWXYZÆØÅ\n0123456789", spacing=2, font=small05)

    for c in range(len(color.keys())):
        d.rectangle(((4*c + 1, 23), (4*c + 4, 28)), fill=list(color.values())[c])

    return im