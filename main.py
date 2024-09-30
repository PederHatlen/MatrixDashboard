import time, virtual_display, functions, pannels, gpiozero, datetime
from PIL import Image, ImageFont, ImageDraw

small10 = ImageFont.truetype(f"{functions.PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

t = 0

oldoutTS = 0

menuSelected = 4
menuActive = False

pNames = pannels.__all__

colors = {
    "Clock":"#ff8800",
    "ColorNoice":"#f060df",
    "NormalMap":"#ff0000",
    "Spotify":"#1ed760",
    "Sun":"#FFDF22"
}

socketio = virtual_display.run("1337", allow_cors=True)

def buttonpress():
    print("pressed!")
    pannels.spotify.toggle()

def render(frame, ts):
    global oldoutTS
    if ts - oldoutTS >= 1: 
        oldoutTS = ts
        functions.renderConsole(frame)
        print(f"Current temperature: {int(open('/sys/class/thermal/thermal_zone0/temp').read())/1000}")
    socketio.emit("refresh", frame)

def menu(pannels = pannels):
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)

    for i in range(len(pannels.packages)):
        if i == menuSelected: d.rectangle(((((i*4)%64), ((i//64)*4)), (((i*4)%64)+2, ((i//64)*4)+2)), "#fff")
        d.point((((i*4)%64)+1, ((i//64)*4)+1), colors[pNames[i]] if pNames[i] in colors else "#444")

    d.text((0, 16), pNames[menuSelected], "#fff",small05)
    return functions.PIL2frame(im)

def toggleMenu():
    print("activated")
    global menuActive
    menuActive = not menuActive
    if menuActive: render(menu(), t)
def menuCW(): 
    if not menuActive: return
    global menuSelected
    menuSelected = (menuSelected+1) % len(pannels.packages)
    print("CW")
    render(menu(), t)
def menuCC(): 
    if not menuActive: return
    global menuSelected
    menuSelected = ((menuSelected-1) if menuSelected > 0 else len(pannels.packages)-1)
    print("CC")
    render(menu(), t)

menuBTN = gpiozero.Button(26,bounce_time=0.1)
menuDial = gpiozero.RotaryEncoder(20,21, wrap=True, max_steps=0);
menuBTN.when_activated = toggleMenu
menuDial.when_rotated_clockwise = menuCW
menuDial.when_rotated_counter_clockwise = menuCC

dial1BTN = gpiozero.Button(16,bounce_time=0.1)
dial1Dial = gpiozero.RotaryEncoder(19,13, wrap=True, max_steps=0);
dial1BTN.when_activated = (lambda a: print("Dial 1 Button click"))
dial1Dial.when_rotated_clockwise = (lambda a: print("Dial1 CW"))
dial1Dial.when_rotated_counter_clockwise = (lambda a: print("Dial1 CC"))

dial2BTN = gpiozero.Button(12,bounce_time=0.1)
dial2Dial = gpiozero.RotaryEncoder(5,6, wrap=True, max_steps=0);
dial2BTN.when_activated = (lambda a: print("Dial 2 Button click"))
dial2Dial.when_rotated_clockwise = (lambda a: print("Dial2 CW"))
dial2Dial.when_rotated_counter_clockwise = (lambda a: print("Dial2 CC"))

framenum = 0
while True:
    t = datetime.datetime.now().timestamp()
    if not menuActive: render(pannels.packages[menuSelected].get(t), t)
    time.sleep(0.2)