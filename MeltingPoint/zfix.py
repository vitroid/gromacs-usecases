#!/usr/bin/env python

# Z座標が指定の範囲にある原子のみ固定する。

from gromacs import read_gro

import sys

zmin, zmax = [float(x) for x in sys.argv[1:3]]

for frame in read_gro(sys.stdin):
    break

print("[FIX]")
s = ""
for i in range(len(frame["atom"])):
    if zmin < frame["position"][i,2] < zmax:
        s += f"{i+1}  "
        if len(s) > 72:
            print(s)
            s = ""
print(s)
