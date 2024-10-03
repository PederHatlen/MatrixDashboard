import datetime, functions
from PIL import Image, ImageFont, ImageDraw
from math import radians, sin, cos, atan2, asin, degrees

small05 = ImageFont.truetype(f"{functions.PATH}/fonts/small05.ttf", 5)

fn_last = 0
oldim = Image.new("RGB", size=(64,32))

lat, long = 63.42236123297012, 10.431957133973581

def getSunAltitude(t:datetime.datetime, lat = lat, long = long):  # Tyholttårnet, Trondheim Norway
    # Souces: 
    # https://en.wikipedia.org/wiki/Position_of_the_Sun
    # https://sceweb.sce.uhcl.edu/helm/WEB-Positional%20Astronomy/Tutorial/Conversion/Conversion.html
    # https://aa.usno.navy.mil/faq/GAST

    D = (t.timestamp() / 86400.0) -10957.5                                                          # Days since 1st of January 2000 with julian calendar
    L = (280.460 + 0.9856474 * D)                                                                   # Mean longitude of sun (corrected for aberration of light)
    g = radians(357.528 + 0.9856003 * D)                                                            # Mean anomaly of the earth, angle from periapsis in an orbit (from the earths perspective)
    eclipticLong = radians(L + 1.9148 * sin(g) + 0.02 * sin(2 * g))                                 # Ecliptic Longitude of sun
    eclipticTilt = radians(23.439 - 0.0000004 * D)                                                  # Obliquity of the ecliptic, The tilt of the axis the sun and earth lies on

    RA = atan2(cos(eclipticTilt) * sin(eclipticLong), cos(eclipticLong))                            # Right Ascension, angle between longitude 0 on the equator to the suns longitude on the equator
    DEC = asin(sin(eclipticTilt) * sin(eclipticLong))                                               # declination

    GMST = 280.46061837 + 360.98564736629 * D                                                       # Greenwich Mean Sidereal Time (suntime at Greenwich) in hours
    LHA = radians(GMST + long - degrees(RA))                                                        # Local Hour Angle (LST - Right Ascention)

    return degrees(asin(sin(DEC) * sin(radians(lat)) + cos(DEC) * cos(radians(lat)) * cos(LHA)))    # Returns altitude

def get(fn):
    global oldim, fn_last
    
    if (fn - fn_last) < 10: return functions.PIL2frame(oldim)
    fn_last = fn
    
    im = Image.new(mode="RGB", size=(64, 32))
    d = ImageDraw.Draw(im)
    now = datetime.datetime.now() #+ datetime.timedelta(days=fn) # Scrub through the year
    modified = now.replace(hour=0, minute=0,second=0,microsecond=0, tzinfo=datetime.timezone.utc)

    xyValues = [(t, 16-int(0.25*getSunAltitude(modified + datetime.timedelta(hours=t/2)))) for t in range(0, 64)]


    d.line(((0,16), (64,16)), "#444")                                       # Horizonline
    d.point(xyValues, "#fff")                                               # Graph of sun possitions
    d.point(xyValues[round((now.hour + now.minute/60)*2)], "#FFDF22")       # The sun curently
    d.text((0,0), str(now.strftime("%b %d")), "#FFDF22", small05)           # Date

    oldim = im

    return functions.PIL2frame(im)