import time, virtual_display, functions, pannels, gpiozero

socketio = virtual_display.run("1337", allow_cors=True)

def buttonpress():
    print("pressed!")
    pannels.spotify.toggle()

def render(frame, framenum):
    if framenum % 10 == 0: 
        functions.renderConsole(frame)
        print(f"Current temperature: {int(open('/sys/class/thermal/thermal_zone0/temp').read())/1000}")
    socketio.emit("refresh", frame) 

playpauseBTN = gpiozero.Button(21,bounce_time=0.1)
playpauseBTN.when_activated = buttonpress

rotor = gpiozero.RotaryEncoder(4,17, wrap=True, max_steps=0);


framenum = 0
while True:
    render(pannels.spotify.get(framenum))
    # print(f"New frame\nCurrent temperature: {int(open('/sys/class/thermal/thermal_zone0/temp').read())/1000}")
    framenum += 1
    time.sleep(0.2)