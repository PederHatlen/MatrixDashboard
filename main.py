import time, virtual_display, functions, pannels, gpiozero, datetime
from PIL import Image, ImageFont, ImageDraw

global menuActive, menuSelected

small10 = ImageFont.truetype(f"{functions.PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

t = 0
framenum = 0

oldoutTS = 0

menuSelected = 4
menuActive = False

pNames = pannels.__all__

menuColor = "#ff8800"
# colors = {
#     "Clock":"#ff8800",
#     "ColorNoice":"#f060df",
#     "NormalMap":"#ff0000",
#     "Spotify":"#1ed760",
#     "Sun":"#FFDF22"
# }

socketio = virtual_display.run("1337", allow_cors=True)

menuBTN = gpiozero.Button(26,bounce_time=0.1)
menuDial = gpiozero.RotaryEncoder(20,21, wrap=True, max_steps=0)

dial1BTN = gpiozero.Button(16,bounce_time=0.1)
dial1Dial = gpiozero.RotaryEncoder(19,13, wrap=True, max_steps=0)

dial2BTN = gpiozero.Button(12,bounce_time=0.1)
dial2Dial = gpiozero.RotaryEncoder(5,6, wrap=True, max_steps=0)

def render(frame):
    global oldoutTS
    now = datetime.datetime.now().timestamp()
    if now - oldoutTS >= 1: 
        oldoutTS = now
        functions.renderConsole(frame)
        print(f"Current temperature: {int(open('/sys/class/thermal/thermal_zone0/temp').read())/1000}")
    socketio.emit("refresh", frame)

def menu(pannels = pannels):
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)

    for i in range(len(pannels.packages)):
        if i == menuSelected: d.rectangle(((((i*4)%64), ((i//64)*4)), (((i*4)%64)+2, ((i//64)*4)+2)), "#fff")
        d.point((((i*4)%64)+1, ((i//64)*4)+1), menuColor)

    d.text((0, 16), pNames[menuSelected], "#fff",small05)
    return functions.PIL2frame(im)

def toggleMenu():
    global menuActive
    menuActive = not menuActive
    if menuActive: render(menu())
def menuCW(): 
    global menuActive, menuSelected
    if not menuActive: return
    menuSelected = (menuSelected+1) % len(pannels.packages)
    render(menu())

def menuCC(): 
    global menuActive, menuSelected
    if not menuActive: return
    menuSelected = ((menuSelected-1) if menuSelected > 0 else len(pannels.packages)-1)
    render(menu())


def dial(name):
    try:
        pannels.packages[menuSelected].dial(name)
        return render(pannels.packages[menuSelected].get(framenum))
    except AttributeError: print(f"pannel {menuSelected} doesnt support dial")

def btn(clicked):
    try:
        pannels.packages[menuSelected].btn(dial1BTN, dial2BTN, clicked)
        return render(pannels.packages[menuSelected].get(framenum))
    except AttributeError: print(f"pannel {menuSelected} doesnt support buttons")

menuBTN.when_activated = toggleMenu
menuDial.when_rotated_clockwise = menuCW
menuDial.when_rotated_counter_clockwise = menuCC

dial1BTN.when_activated = (lambda a: dial(dial1BTN))
dial1Dial.when_rotated_clockwise = (lambda a: dial("CW1"))
dial1Dial.when_rotated_counter_clockwise = (lambda a: dial("CC1"))

dial2BTN.when_activated = (lambda a: btn(dial2BTN))
dial2Dial.when_rotated_clockwise = (lambda a: dial("CW2"))
dial2Dial.when_rotated_counter_clockwise = (lambda a: dial("CC2"))

while True:
    t = datetime.datetime.now().timestamp()
    if not menuActive: render(pannels.packages[menuSelected].get(framenum))
    framenum += 1
    time.sleep(0.1)