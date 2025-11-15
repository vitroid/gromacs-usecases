muR.gro: lattices/muR.py
	# ケージにtip4pを埋め、密度を調節し、格子を拡張 | 本来の水を除去 | 原子数を調整
	genice2 muR -g 12=tip4p -g 14=tip4p -g 15=tip4p -g 16=tip4p --dens 10 -r 6 3 1 | grep -v SOL | awk '(NR==2){$$1=78*4*6*3}{print}' | grep -v '^#' > muR.gro


lattices/muR.py:
	# lattice moduleのためのディレクトリを作る。
	-mkdir lattices
	# cellの形状を直方体にする(muは六方晶、ケージ数39)。倍の大きさになる(ケージ数78)
	genice2 mu -f reshape[1,0,0,1,2,0,0,0,1] --dens 0.8 > lattices/muR.py
