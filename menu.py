import pannels
from PIL import Image, ImageDraw
from functions import *

small05 = font["small05"]

selected = "Clock" # Default pannel can be sett here

PNames = pannels.__all__

menuColor = {
    "system":color["lightred"],
    "clocks":color["orange"],
    "debug":color["yellow"],
    "fun":color["purple"],
    "info":color["green"]
}

def dial(dir):
    global selected

    selectedI = PNames.index(selected)
    if dir == "0R": selected = PNames[(selectedI+1)% len(pannels.packages)]
    elif dir == "0L": selected = PNames[((selectedI-1) if selectedI > 0 else len(pannels.packages)-1)]

def btn(btn):

    return

# def menuTurn(dir): 
#     global menuActive, menuSelected, autoSelected
#     if not menuActive: return menuDial.dial(dir)
#     elif dir == "1R": menuSelected = (menuSelected+1) % len(pannels.packages)
#     elif dir == "1L": menuSelected = ((menuSelected-1) if menuSelected > 0 else len(pannels.packages)-1)
#     autoSelected = False
#     render(menu())

def get():
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)

    for i in range(len(pannels.packages)):
        x, y = ((i*4)%64), ((i//64)*4)
        if PNames[i] == selected: d.rectangle(((x, y), (x+2, y+2)), "#fff")
        tColor = menuColor[pannels.menuINV[PNames[i]]] if (pannels.menuINV[PNames[i]] in menuColor) else "#aaa"
        d.point((x+1, y+1), tColor)

    tColor = menuColor[pannels.menuINV[selected]] if (pannels.menuINV[selected] in menuColor) else "#fff"
    d.text((0, 8), pannels.menuINV[selected], tColor, small05)
    d.text((0, 16), selected, "#fff", small05)

    return im