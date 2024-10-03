import functions
from PIL import Image, ImageDraw

x, y = 0, 0

drawing = [(0,0),]

def get(fn = 0):
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)
    d.point(drawing, "#fff")

    return functions.PIL2frame(im)

def dial(e):
    print(e)
    global x, y
    if e == "CW1":   x += (1 if x < 63 else 0)
    elif e == "CC1": x -= (1 if x > 0 else 0)
    elif e == "CW2": y += (1 if y < 31 else 0)
    elif e == "CC2": y -= (1 if y > 0 else 0)
    if (x, y) not in drawing: drawing.append((x,y))

def btn(btn1, btn2, clicked): 
    print("BTN click")
    global drawing
    if btn1.is_active and btn2.is_active: 
        print("Clearing")
        drawing = []