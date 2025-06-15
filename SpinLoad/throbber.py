import sys
import time

chars = ['-', '\\', '|', '/']

while True:
    for i in chars:
        sys.stdout.write('\r' + i)
        sys.stdout.flush()
        time.sleep(0.1)
