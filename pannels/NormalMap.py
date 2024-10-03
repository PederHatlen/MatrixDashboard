import functions
def get(ts): return [[functions.rgb2hex([(x*255)//32,(y*255)//64,128]) for y in range(64)] for x in range(32)]