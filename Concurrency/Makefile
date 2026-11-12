# =================================================================
# 1. 探索対象 (パラメータ空間) の定義
# ここを書き換えるだけで、計算対象のディレクトリを制御できる
# =================================================================

# 調査したい圧力(P)と温度(T)のリスト
PRESSURES := 6000bar 8000bar 10000bar
TEMPS     := 140K 150K 160K 170K

# 全組み合わせを生成 (Grid search)
ALL_COMBINATIONS := $(foreach p,$(PRESSURES),$(foreach t,$(TEMPS),$(p)/$(t)))

# 特定の組み合わせを除外したい場合 (例: 8000barの150K, 170Kは不要)
EXCLUDES     := 8000bar/150K 8000bar/170K
TARGET_DIRS  := $(filter-out $(EXCLUDES), $(ALL_COMBINATIONS))

# =================================================================
# 2. 生成すべきファイル (ターゲット) の定義
# 各ディレクトリに対して、最終的に得たいファイルの拡張子を指定する
# =================================================================

# 各ディレクトリに 00002.edrと 00002-last.groがある状態を「完成」とする
# ただし、後者は最後の最後に派生するファイルなので、Makefileには含めない
ALL_TARGETS := $(addsuffix /00002.edr, $(TARGET_DIRS)) \
    $(addsuffix /00002.mdinfo, $(TARGET_DIRS)) \
    $(addsuffix /00002.gro, $(TARGET_DIRS))

# =================================================================
# 3. 依存関係のルール (拡張子ベースの共通ルール)
# ディレクトリ構造に依存しない、純粋な「作り方」の定義
# =================================================================

.SECONDARY:
.PHONY: all clean
all: $(ALL_TARGETS)

# --- ステップ1: grompp で実行用ファイル(tpr)を作成 ---
%/00002.tpr: 00001-last.gro %/continue.mdp TraPPE_Vega.top
	gmx grompp -maxwarn 2 -f $*/continue.mdp -p TraPPE_Vega.top -o $@ -c $<

# --- ステップ2: mdrun で計算実行 ---
# 成果物 %00002.edr は 入力 %00002.tpr に依存する
# 成果物 %00002-last.gro は 一番最後に生成される。
# $*/00002 を出力の接頭辞(deffnm)に使う
%/00002.edr: %/00002.tpr
	time gmx mdrun -ntmpi 16 -ntomp 1 -notunepme -deffnm $*/00002 -c $@

%/00002.mdinfo: %/00002.edr
	gmx dump -e $< | python3 ../../common/undump.py > $@

%.gro: %.trr %.tpr
	echo 0 | gmx trjconv -f $< -s $*.tpr -o $@ # -pbc mol -center

# --- (オプション) ステップ3: さらに延長する場合 ---
# edrと-last.groがそろってはじめて完成と言える。
# 実際には継続計算が必要になることは今回はなさそうだ。
%/00003.tpr: %/00002.edr %/00002-last.gro
	gmx convert-tpr -s $*/00002.tpr -extend 30000 -o $@

# 掃除
clean:
	-rm -f *.pdb
	-rm -f "#"*
