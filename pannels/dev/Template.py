import functions

small05 = functions.font["small05"]

def get():
    im, d = functions.getBlankIM()
    d.multiline_text((0,0), "Nothing to see \nhere", font=small05)

    return im