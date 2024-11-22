import datetime
import numpy as np
import astral.sun, astral.moon # Cheating
from PIL import Image, ImageDraw
from math import radians, sin, cos, atan2, asin, degrees
from functions import *

small05 = font["small05"]

BC = 0
GC = 64
WC = 255

# Moon phase images
moonPhases = {
    0:[[BC,GC,GC,GC,GC,BC],[GC,GC,GC,GC,GC,GC],[GC,GC,GC,GC,GC,GC],[GC,GC,GC,GC,GC,GC],[GC,GC,GC,GC,GC,GC],[BC,GC,GC,GC,GC,BC]],
    1:[[BC,GC,GC,WC,WC,BC],[GC,GC,GC,GC,WC,WC],[GC,GC,GC,GC,GC,WC],[GC,GC,GC,GC,GC,WC],[GC,GC,GC,GC,WC,WC],[BC,GC,GC,WC,WC,BC]],
    2:[[BC,GC,GC,WC,WC,BC],[GC,GC,GC,WC,WC,WC],[GC,GC,GC,WC,WC,WC],[GC,GC,GC,WC,WC,WC],[GC,GC,GC,WC,WC,WC],[BC,GC,GC,WC,WC,BC]],
    3:[[BC,GC,GC,WC,WC,BC],[GC,GC,WC,WC,WC,WC],[GC,WC,WC,WC,WC,WC],[GC,WC,WC,WC,WC,WC],[GC,GC,WC,WC,WC,WC],[BC,GC,GC,WC,WC,BC]],
    4:[[BC,WC,WC,WC,WC,BC],[WC,WC,WC,WC,WC,WC],[WC,WC,WC,WC,WC,WC],[WC,WC,WC,WC,WC,WC],[WC,WC,WC,WC,WC,WC],[BC,WC,WC,WC,WC,BC]],
    5:[[BC,WC,WC,GC,GC,BC],[WC,WC,WC,WC,GC,GC],[WC,WC,WC,WC,WC,GC],[WC,WC,WC,WC,WC,GC],[WC,WC,WC,WC,GC,GC],[BC,WC,WC,GC,GC,BC]],
    6:[[BC,WC,WC,GC,GC,BC],[WC,WC,WC,GC,GC,GC],[WC,WC,WC,GC,GC,GC],[WC,WC,WC,GC,GC,GC],[WC,WC,WC,GC,GC,GC],[BC,WC,WC,GC,GC,BC]],
    7:[[BC,WC,WC,GC,GC,BC],[WC,WC,GC,GC,GC,GC],[WC,GC,GC,GC,GC,GC],[WC,GC,GC,GC,GC,GC],[WC,WC,GC,GC,GC,GC],[BC,WC,WC,GC,GC,BC]]
}

fn_last = 0
oldim = Image.new("RGB", size=(64,32))

lat, long = 63.4224, 10.4320 # Trondheim
# lat, long = 69.0645, 18.5152 # Bardufoss
# lat, long = 90, 10.4320 # North pole
# lat, long = 0, 10.4320 # Equator

def getSunAltitude(t:datetime.datetime, lat = lat, long = long):  # Tyholttårnet, Trondheim Norway
    # Souces: 
    # https://en.wikipedia.org/wiki/Position_of_the_Sun
    # https://sceweb.sce.uhcl.edu/helm/WEB-Positional%20Astronomy/Tutorial/Conversion/Conversion.html
    # https://aa.usno.navy.mil/faq/GAST

    D = (t.timestamp() / 86400.0) - 10957.5                                                         # Days since 1st of January 2000 with julian calendar
    L = (280.46646 + 0.98564736 * D)                                                                # Mean longitude of sun (corrected for aberration of light)
    g = radians(357.528 + 0.9856003 * D)                                                            # Mean anomaly of the earth, angle from periapsis in an orbit (from the earths perspective)
    eclipticLong = radians(L + 1.9148 * sin(g) + 0.02 * sin(2 * g))                                 # Ecliptic Longitude of sun
    eclipticTilt = radians(23.439 - 0.0000004 * D)                                                  # Obliquity of the ecliptic, The tilt of the axis the sun and earth lies on

    RA = atan2(cos(eclipticTilt) * sin(eclipticLong), cos(eclipticLong))                            # Right Ascension, angle between longitude 0 on the equator to the suns longitude on the equator
    DEC = asin(sin(eclipticTilt) * sin(eclipticLong))                                               # declination

    GMST = 280.46061837 + 360.98564736629 * D                                                       # Greenwich Mean Sidereal Time (suntime at Greenwich) in hours
    LHA = radians(GMST + long - degrees(RA))                                                        # Local Hour Angle (LST - Right Ascention)
    
    return degrees(asin(sin(DEC) * sin(radians(lat)) + cos(DEC) * cos(radians(lat)) * cos(LHA)))    # Altitude of the sun on the sky from given coordinates

dayoffset = 0
def dial(e):
    global dayoffset
    if e == "2R": dayoffset+=1
    elif e == "2L": dayoffset-=1

def get(fn):
    global oldim, fn_last, dayoffset
    
    if (fn - fn_last) < 10: return PIL2frame(oldim)
    fn_last = fn
    
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)
    now = datetime.datetime.now() + datetime.timedelta(days=dayoffset) # Scrub through the year
    modified = now.replace(hour=0,minute=0,second=0,microsecond=0,tzinfo=datetime.timezone.utc)

    xyValues = [(t, 15-(int((getSunAltitude(modified + datetime.timedelta(hours=t/2))/90)*15.5))) for t in range(0,64)]

    im.paste(Image.fromarray(np.array(moonPhases[((astral.moon.phase(modified)/27.99)*8)//1], dtype=np.uint8), mode="L"), (54, 0))

    try:
        s = astral.sun.sun(astral.Observer(latitude=lat, longitude=long), modified, tzinfo=modified.tzinfo)
        sunriseDT = s["sunrise"].astimezone().strftime("%H:%M")
        sunsetDT = s["sunset"].astimezone().strftime("%H:%M")
    except: sunriseDT, sunsetDT = "None", "None"

    d.line(((0,16), (64,16)), "#444")                                                   # Horizonline
    d.line(xyValues, "#fff")                                                            # Graph of sun possitions
    d.point(xyValues[round((now.hour + now.minute/60)*2)], color["yellow"])             # The sun curently

    d.text((0,0), str(now.strftime("%b %d")), color["yellow"], small05)                         # Date
    d.text((0, 27), str(sunriseDT), color["orange"], small05)                                   # Sunrise Time
    d.text((65-small05.getlength(sunsetDT), 27), str(sunsetDT), color["purple"], small05)       # Sunset Time

    oldim = im

    return PIL2frame(im)