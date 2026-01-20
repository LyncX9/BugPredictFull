import os

def dangerous():
    os.remove("/important/file")
    return 1 / 0

while True:
    dangerous()
