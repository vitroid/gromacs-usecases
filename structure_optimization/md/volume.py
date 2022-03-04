import sys
import numpy as np

def getcell(file):
    line = file.readline()
    N = int(file.readline())
    for i in range(N):
        file.readline()
    return N, np.fromstring(file.readline(), sep=" ")


while True:
    # try:
    Natom, cell = getcell(sys.stdin)
    print(np.product(cell) / (Natom//4))
    # except:
        # sys.exit(0)





