import gromacs as gro
import numpy as np
import sys
import itertools as it
import networkx as nx
import pairlist as pl
import simplex
import yaplotlib as yap
from cycless import cycles


def draw_cycle(rpos, cell):
    # 環を描画。
    # 周期境界をまたぐ可能性があるのでちょっと面倒。
    rr = rpos - rpos[0]
    rr -= np.floor(rr+0.5)
    rr += rpos[0]
    return yap.Polygon(rr @ cell)


def draw_tetra(rpos, cell):
    # 四面体を描画。
    # 周期境界をまたぐ可能性があるのでちょっと面倒。
    rr = rpos - rpos[0]
    rr -= np.floor(rr+0.5)
    rr += rpos[0]
    pos = rr @ cell
    y = ""
    for p,q,r in it.combinations(pos, 3):
        y += yap.Polygon([p,q,r])
    return y


def com(rpos):
    # center-of-mass
    rr = rpos - rpos[0]
    rr -= np.floor(rr+0.5)
    return rr.mean(axis=0) + rpos[0]


def main():
    for frame in gro.read_gro(sys.stdin):
        cell = frame["cell"]
        celli = np.linalg.inv(cell)
        oxygens = np.array([pos for i, pos in enumerate(frame["position"]) if frame["atom"][i][0] == "O"]) @ celli
        # 隣接関係をグラフで表現する。
        g = nx.Graph()
        # 近接ペアについてループ
        for i, j, d in pl.pairs_iter(oxygens, 0.36, cell):
            g.add_edge(i,j)

        # layer 1: 四面体を描く
        s = yap.RandomPalettes(10, offset=3)
        s += yap.Layer(1)
        s += yap.Color(3)
        for ijkl in simplex.tetrahedra_iter(g):
            s+= draw_tetra(oxygens[ijkl, :], cell)

        # 重心を記録
        coms = []
        tet_memb = []
        for id, ijkl in enumerate(simplex.tetrahedra_iter(g)):
            coms.append(com(oxygens[ijkl, :]))
            tet_memb.append(ijkl)
        coms = np.array(coms)

        # あとで扱いやすいように、四面体に通し番号を付ける
        tet_id = {memb:id for id, memb in enumerate(tet_memb)}

        # 四面体の隣接グラフを作る
        triangles = dict()
        gtet = nx.Graph()
        for ijkl in tet_memb:
            i,j,k,l = ijkl
            for tri in [(i,j,k), (i,j,l), (i,k,l), (j,k,l)]:
                if tri in triangles:
                    nei = triangles[tri]
                    gtet.add_edge(tet_id[ijkl], tet_id[nei])
                triangles[tri] = ijkl

        # layer 2: 四面体の隣接ネットワークを描く
        s += yap.Layer(2)
        s += yap.Color(4)
        for i, j in gtet.edges():
            d = coms[i] - coms[j]
            d -= np.floor(d+0.5)
            tail = coms[j] @ cell
            head = tail + d @ cell
            s += yap.Line(head, tail)

        # layer 3: 四面体の隣接ネットワークの環を描く
        for cycle in cycles.cycles_iter(gtet, maxsize=6):
            nmemb = len(cycle)
            s += yap.Layer(nmemb)   # 3..6
            s += yap.Color(nmemb+2) # 5..8
            s += draw_cycle(coms[cycle, :], cell)

        print(s)


if __name__=="__main__":
    main()
