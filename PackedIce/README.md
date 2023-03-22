# 高密度氷の生成

mu構造の高密度氷を準備する。

## 1. 初期配置の生成

高密度氷はアイスルールを満たさない場合があり、geniceだけでは構造生成できない。

```
make muR.gro
```

## 2. 焼きなまし

酸素位置を固定し、自由回転だけを許して配向を最適化する。

水分子モデルはTIP4P/2005。

```
gmx make_ndx -f muR.gro -o muR.ndx
> a OW
> q
```

これで、OW原子だけを含む新しい原子群OWが定義された。

## 3. mdpファイルの準備

* 酸素が動けないので、体積は変化できない。
* 原子群OWを固定する。

## 4. コンパイル

```shell
gmx grompp -maxwarn 1 -f fix.mdp -p 4P2005.top -c muR.gro -n muR.ndx   -o fixed.tpr
```

## 5. 実行

```shell
gmx mdrun -deffnm fixed
```

## 6. 確認

```shell
echo 0 | gmx trjconv -f fixed.trr -s fixed.tpr -pbc whole   -o fixed-snapshots.gro
```

## 7. 焼鈍

200 Kに冷やす。

```shell
gmx grompp -maxwarn 1 -f anneal200K.mdp -p 4P2005.top -t fixed.cpt -c fixed.tpr -o anneal200K.tpr
gmx mdrun -deffnm anneal200K
echo 0 | gmx trjconv -f anneal200K.trr -s anneal200K.tpr -pbc whole   -o anneal200K-snapshots.gro
```

## 8. 焼鈍

圧力一定に。

```shell
gmx grompp -maxwarn 1 -f anneal200KNPT.mdp -p 4P2005.top -t anneal200K.cpt -c anneal200K.tpr -o anneal200KNPT.tpr
gmx mdrun -deffnm anneal200KNPT
echo 0 | gmx trjconv -f anneal200KNPT.trr -s anneal200KNPT.tpr -pbc whole   -o anneal200KNPT-snapshots.gro

```
