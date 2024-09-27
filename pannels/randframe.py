import os
def get(): return [["#"+"".join(["000000",os.urandom(3).hex()])[-6:] for y in range(32)] for x in range(64)]