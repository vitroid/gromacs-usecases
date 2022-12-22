#!/usr/bin/env python

"""
.groファイルを読みこみ、六員環の種を分類するとともに、環の位置を特定する。
geniceの_ringstatのコードを流用する。
将来は_ringstat+analiceに組みこむかもしれない。
"""

import sys
from collections import defaultdict

import networkx as nx
import numpy as np
import pairlist as pl
from cycless.cycles import cycles_iter
from genice2.formats._ringstat import encode, orientations, probabilities
from gromacs import decompose, read_gro

for ifile, frame in enumerate(read_gro(sys.stdin)):
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

    graph = nx.Graph(g)  # undirected
    stat = defaultdict(int)
    # Ideal distributions
    prob = probabilities(6)

    for ring in cycles_iter(graph, 6, pos=oxygens):
        if len(ring) == 6:
            ori = orientations(ring, g)
            typ = encode(ori)
            stat[typ] += 1
            # find the center of the cycle
            # delta = oxygens[ring, :] - oxygens[ring[0]]
            # delta -= np.floor(delta+0.5)
            # dc = np.average(delta, axis=0)
            # center = (oxygens[ring[0]]+dc) @ cell
            # print(typ, *center)
    # total_cycles = sum([stat[y] for y in stat])
    # for y in stat:
    #     stat[y] /= total_cycles
    with open(f"{ifile}.cyc.txt", "w") as fh:
        print("# types0 1 3 5 7 9 11 21", file=fh)
        print(*[stat[y] for y in sorted(stat)], file=fh)
