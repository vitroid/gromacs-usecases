#!/usr/bin/env python

# Z座標が指定の範囲にある原子のみ固定する。

import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pairlist as pl
from gromacs import decompose, read_gro

for frame in read_gro(sys.stdin):
    break

cell = frame["cell"]
celli = np.linalg.inv(cell)
oxygens = np.array([frame["position"][i] for i in range(len(frame["atom"])) if frame["atom"][i] == "OW"])
hydrogens = np.array([frame["position"][i] for i in range(len(frame["atom"])) if frame["atom"][i][:2] == "HW"])

# in a fractional coordinate
oxygens = oxygens @ celli
hydrogens = hydrogens @ celli

HBs = dict()
for i,j,d in pl.pairs_iter(oxygens, 0.25, cell, pos2=hydrogens):
    if d > 0.1:
        # 水素の番号を分子の番号に換算
        jo = j // 2
        # すでに水素結合がある場合は
        if (jo,i) in HBs:
            # 新しいほうが長ければ
            if HBs[jo,i] < d:
                # 見送る
                continue
        # 水素結合を登録
        # 分岐水素結合もできるかもしれないが気にしない。
        HBs[jo,i] = d

g = nx.DiGraph(HBs.keys())

# セルを0.01 nm = 0.1 AA単位できざみ、各binに酸素原子を分配する。
# 0.01 nmは、fractional coordinateでは?
binw = 0.01 / cell[2,2]
bins = (oxygens[:,2] // binw).astype(int)
nbin = int(cell[2,2] / 0.01)+1

#
#   |  bin0  |  bin1  |  bin2  |  bin3  | ...
# memb0    memb1    memb2    memb3    memb4
#   <--- backward     forward --->

memb_forw = np.zeros(nbin)
memb_back = np.zeros(nbin)


for ox, bin in enumerate(bins):
    # oxは分子番号
    # binはその分子の入っているbin
    for nei in g[ox]:
        binto = bins[nei]
        # print(bin, binto)
        if binto > bin:
            # binの右側(z向き)の面を正方向に横切る。
            memb_forw[bin+1:binto+1] += 1
        elif binto < bin:
            memb_back[binto+1:bin+1] += 1

for i, (f, b) in enumerate(zip(memb_forw, memb_back)):
    print(i*0.01, f-b, f, b)

# plt
# plt.plot(np.arange(nbin)*0.01, memb_forw - memb_back)
# plt.show()
