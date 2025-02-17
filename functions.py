import pathlib
import numpy as np
from PIL import ImageFont
PATH = str(pathlib.Path(__file__).parent.resolve())

asciiTable = "`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

font = {
    "small05": ImageFont.truetype(f"{PATH}/fonts/small05.ttf", 5),
    "icons07": ImageFont.truetype(f"{PATH}/fonts/icons.ttf", 7)
}

color = {
    "red":"#FF0000",
    "lightred":"#FF4040",
    "orange":"#FF8000",
    "yellow":"#FFFF00",
    "green":"#00FF00",
    "mint":"#00FF80",
    "teal":"#00FFFF",
    "lightblue":"#0080FF",
    "blue":"#0000FF",
    "purple":"#8000FF",
    "pink":"#FF00FF",
    "magenta":"#FF0080",
    "white":"#FFFFFF",
    "spotify":"#1ED760"
}

def clamp8(x): return min(255, max(0, int(x)))

def rgb2hex(rgb): return '#%02x%02x%02x' % (clamp8(rgb[0]), clamp8(rgb[1]), clamp8(rgb[2]))

def hex2rgb(hex): return tuple(int(hex[1:][i:i+2], 16) for i in (0, 2, 4))

def rgb2lum(rgb): return (0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2])/255

def hex2lum(hex): return rgb2lum(hex2rgb(hex))

def combineFrames(f1, f2):
    return [[(f1[x][y] if f1[x][y] != "#000000" else f2[x][y]) for y in range(64)] for x in range(32)]

def renderConsole(frame): print("\n".join([" ".join([asciiTable[int(hex2lum(y)*len(asciiTable))] for y in x]) for x in frame]))

def PIL2frame(im): return im
def PIL2Socket(im): return [[rgb2hex(y) for y in x] for x in np.array(im).tolist()]