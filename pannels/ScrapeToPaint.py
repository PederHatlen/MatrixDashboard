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
    if e == "1H":   x += (1 if x < 63 else 0)
    elif e == "1L": x -= (1 if x > 0 else 0)
    elif e == "2H": y += (1 if y < 31 else 0)
    elif e == "2L": y -= (1 if y > 0 else 0)
    if (x, y) not in drawing: drawing.append((x,y))

def btn(clicked, both): 
    print("BTN click")
    global drawing
    if both: 
        print("Clearing")
        drawing = []