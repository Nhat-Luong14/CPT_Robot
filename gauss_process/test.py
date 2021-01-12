from getkey import getkey
import time
import sys

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

while True:
    try:
        key = getkey()
        if key == 'g':
            while True:
                print("heloo")
                time.sleep(1)
        if key == 's': #stop
            sys.exit()
    except KeyboardInterrupt:
        print('halt now')
        pass

