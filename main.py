import time, virtual_display, functions, pannels, gpiozero, datetime
from PIL import Image, ImageFont, ImageDraw

# Initialize the webserver/running screen emulator
socketio = virtual_display.run(1337, allow_cors=True)

small10 = ImageFont.truetype(f"{functions.PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

framenum = 0
oldoutTS = 0

pNames = pannels.__all__
menuSelected = pNames.index("Weather") # Default pannel can be sett here
menuActive = False
menuColor = "#ff8800"

def toggleMenu():
    global menuActive
    menuActive = not menuActive
    if menuActive: render(menu())

def menuTurn(dir): 
    global menuActive, menuSelected
    if not menuActive: return menuDial.dial(dir)
    elif dir == "1H": menuSelected = (menuSelected+1) % len(pannels.packages)
    elif dir == "1L": menuSelected = ((menuSelected-1) if menuSelected > 0 else len(pannels.packages)-1)
    render(menu())

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
        x, y = ((i*4)%64), ((i//64)*4)
        if i == menuSelected: d.rectangle(((x, y), (x+2, y+2)), "#fff")
        d.point((x+1, y+1), menuColor)

    d.text((0, 16), pNames[menuSelected], "#fff",small05)
    return functions.PIL2frame(im)

class dial:
    def __init__(self, dialNumber, BTNpin, D1, D2, menu = False):
        self.BTN = gpiozero.Button(BTNpin,bounce_time=0.1)
        self.DIAL = gpiozero.RotaryEncoder(D1,D2, wrap=True, max_steps=0)
        self.dialNumber = dialNumber

        self.BTN.when_activated = (toggleMenu if menu else self.btn)
        self.DIAL.when_rotated_clockwise = (lambda: menuTurn(f"{self.dialNumber}H") if menu else self.dial(f"{self.dialNumber}H"))
        self.DIAL.when_rotated_counter_clockwise = (lambda: menuTurn(f"{self.dialNumber}L") if menu else self.dial(f"{self.dialNumber}L"))
    
    def dial(self, dir):
        try: pannels.packages[menuSelected].dial(dir)
        except AttributeError: return print(f"{menuSelected} doesn't support dial")
        return render(pannels.packages[menuSelected].get(framenum))
    
    def btn(self):
        try: pannels.packages[menuSelected].btn()
        except AttributeError: return print(f"{menuSelected} doesn't support buttons")
        return render(pannels.packages[menuSelected].get(framenum))
        

# Dials and buttons
menuDial = dial(1, 26, 20, 21, True)
dial1 = dial(2, 16, 19, 13)

while True:
    if not menuActive: render(pannels.packages[menuSelected].get(framenum))
    framenum += 1
    time.sleep(0.1)