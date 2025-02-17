import functions, random
from PIL import Image, ImageFont, ImageDraw

small10 = ImageFont.truetype(f"{functions.PATH}/fonts/small10.ttf", 10)
small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

class trail:
    def __init__(self, x = "", y = ""):
        self.x = x if x != "" else random.randint(0, 63)
        self.y = y if y != "" else random.randint(0, 48)
        
        self.speed = random.randint(4, 10)/10
        self.shade = random.randint(64, 255)
        self.length = random.randint(8, 32)

trails = [trail() for i in range(128)]

def get(fn):
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)  
    d.fontmode = "1"

    remove = []

    for t in trails:
        mY = round(t.y)

        d.point((t.x, mY), "#fff")#f"#{hex(t.shade)[2:]*3}")
        for y in range(1, t.length-1):
            shade = hex(t.shade - (y* (t.shade//t.length)))[2:].rjust(2,'0')
            # print(hex(t.shade - (y* (t.shade//t.length))))
            d.point((t.x, mY - y), f"#00{shade}00")

        if mY >= 32+t.length: remove.append(t)
        t.y += t.speed
    
    for t in remove:
        trails.remove(t)
        trails.append(trail(y=0))

    return im