import os
def get(ts): return [["#"+"".join(["000000",os.urandom(3).hex()])[-6:] for y in range(64)] for x in range(32)]