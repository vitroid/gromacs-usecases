#!/usr/bin/env python

"""
.groファイルを読みこみ、ある瞬間のHB(分子対)が、何フレーム前にも出現していたかの統計をとる。
水分子の再配向がない氷のなかでは、同じ水素結合がずっと前から存在する一方、液体のなかでは同じ結合が持続する時間はごく短い。
"""

import sys

import numpy as np
import pairlist as pl
from gromacs import decompose, read_gro
from yaplotlib import Yaplot

history = []
yp = Yaplot()
for ifile, frame in enumerate(read_gro(sys.stdin)):
    cell = frame["cell"]
    celli = np.linalg.inv(cell)
    oxygens = np.array([frame["position"][i] for i in range(len(frame["atom"])) if frame["atom"][i] == "OW"])
    hydrogens = np.array([frame["position"][i] for i in range(len(frame["atom"])) if frame["atom"][i][:2] == "HW"])

    # in a fractional coordinate
    oxygens = oxygens @ celli
    hydrogens = hydrogens @ celli

    HBs = dict()
    # O-H間距離が0.25 nm以下のペアを列挙する。
    for i,j,d in pl.pairs_iter(oxygens, 0.25, cell, pos2=hydrogens):
        # 0.1 nm 以下の場合は分子内なので省く。
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

    history.append(HBs)
    offset = 10
    yp.RainbowPalette(100, offset=offset)

    # 過去のHBと照合する。これはけっこう時間がかかるはず。
    for hb in HBs:
        # 古い順に調べる。
        for i, h in enumerate(history):
            if hb in h:
                # 初出はiフレーム目
                # つまり、寿命は
                lifetime = len(history) - i
                # 統計をとる前に、まずそのまま表示してやろう。
                j, k = hb
                o1 = oxygens[j]
                o2 = oxygens[k]
                d = o2 - o1
                d -= np.floor(d+0.5)
                yp.Palette(lifetime+offset)
                yp.Line(o1@cell, (o1+d)@cell)
    yp.NewPage()

print(yp.dumps())
