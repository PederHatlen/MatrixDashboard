import datetime, functions, math
from PIL import Image, ImageFont, ImageDraw

small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

def get(ts):
    now = datetime.datetime.now()

    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)  
    d.fontmode = "1"

    o = 15  # Origo
    r = 15  # Radius
    w = 4   # Width

    hLen = 8    # Hour dial length
    mLen = 10   # Minute dial length
    sLen = 14   # Second dial length

    for deg in range(0, 360, 90):
        x, y = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        d.line((round(x*(r-w+1)) + o, round(y*(r-w+1)) + o, round(x*r)+o, round(y*r)+o), "#fff", 1)
    for deg in range(45, 360, 90):
        x, y = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        d.line((round(x*(r-w+2)) + o, round(y*(r-w+2)) + o, round(x*r)+o, round(y*r)+o), functions.color["orange"], 1)

    hour = ((now.hour/12) * 2*math.pi - math.pi/2)
    minute = ((now.minute/60) * 2*math.pi - math.pi/2)
    second = ((now.second/60) * 2*math.pi - math.pi/2)

    d.line((r, r, round(math.cos(hour)*hLen)+o, round(math.sin(hour)*hLen)+o), functions.color["white"], 1)
    d.line((r, r, round(math.cos(minute)*mLen)+o, round(math.sin(minute)*mLen)+o), functions.color["white"], 1)
    d.line((r, r, round(math.cos(second)*sLen)+o, round(math.sin(second)*sLen)+o), functions.color["orange"])


    d.text((34, 0), now.strftime("%A"), functions.color["orange"], small05)
    d.text((34, 8), now.strftime("%-d %b"), functions.color["white"], small05)
    d.text((34, 16), now.strftime("Week %W"), functions.color["white"], small05)

    # d.point((15, 15), functions.color["orange"])

    # d.point((*[(x*2, 0) for x in range(32)], *[(0, y*2) for y in range(16)]))

    return functions.PIL2frame(im)