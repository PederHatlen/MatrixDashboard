import numpy as np, PIL.Image
def get(): return PIL.Image.fromarray(np.uint8([[[(x*255)//32,(y*255)//64,128] for y in range(64)] for x in range(32)])).convert('RGB')