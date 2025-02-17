import adafruit_blinka_raspberry_pi5_piomatter as piomatter
import PIL.Image as Image
import numpy as np

geometry = piomatter.Geometry(width=64, height=32, n_addr_lines=4, rotation=piomatter.Orientation.Normal)

framebuffer = np.asarray(Image.new(mode="RGB", size=(64, 32))) + 0

matrix = piomatter.PioMatter(colorspace=piomatter.Colorspace.RGB888Packed,
    pinout=piomatter.Pinout.AdafruitMatrixBonnet,
    framebuffer=framebuffer,
    geometry=geometry)

def render(f):
    framebuffer[:] = np.asarray(f)
    matrix.show()
