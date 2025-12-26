# 大量計算のための手順

鉄則は「同一のファイルのコピーを作らない」ことです。

ここでは一例としてCO2の結晶化の設定を行う。内容の詳細は述べない。

```shell
gmx insert-molecules -f box.gro -ci co2-single.gro -nmol 1000 -o co2.gro
gmx grompp -maxwarn 2 -f initial.mdp -p TraPPE_Vega.top -o 00001.tpr -c co2.gro
```


## 1. 初期配置の生成

対象とする系に依存しない書きかたをしたいので、具体的な初期配置の生成方法は述べない。

`initial.mdp`や`.top`や`initial.gro`などを準備し、gmx mdrunで初期計算を行う。

この作業を行うディレクトリのことをベースディレクトリと呼ぶことにしよう。

温度制御には`v-rescale`を、圧力制御には`berendsen`を指定する。
これらは物理的に正しくないアンサンブルを生じるが、計算が破綻しにくいので、いびつな初期配置でもなんとか平衡化してくれる。

そんなに長い計算は必要ないはずなので、この時点で`-ntmpi`や`ntomp`オプションの値をいろいろ変え、計算機と計算内容に最も適した並列数と分配方法を決める。

例えば16並列が使える計算機ならこんな感じで5通りを試し、一番速いものを採用する。
```shell
time gmx mdrun -ntmpi 1 -ntomp 16 -notunepme -deffnm 00001 -c 00001-last.gro
time gmx mdrun -ntmpi 2 -ntomp 8 -notunepme -deffnm 00001 -c 00001-last.gro
time gmx mdrun -ntmpi 4 -ntomp 4 -notunepme -deffnm 00001 -c 00001-last.gro
time gmx mdrun -ntmpi 8 -ntomp 2 -notunepme -deffnm 00001 -c 00001-last.gro
time gmx mdrun -ntmpi 16 -ntomp 1 -notunepme -deffnm 00001 -c 00001-last.gro
```

## 2. 作業ディレクトリの準備

ここでは`pressure/temperature`の形でディレクトリを多数作成し、それぞれで異なる条件で計算することにする。

ディレクトリ階層は以下のようなシェルコマンドで一括作成できる。
```shell
for pressure in 4000bar 6000bar 8000bar 10000bar 16000bar; do
    for temperature in 140K 150K 160K 170K 190K 210K 230K; do
        mkdir -p ${pressure}/${temperature}
    done
done
```
## 3. ディレクトリごとの設定ファイルの準備

ディレクトリごとに異なるのは、gromacsの設定ファイル`.mdp`の中の温度と圧力の部分のみ。

そこで、ベースディレクトリに、各ディレクトリに配布するための`.mdp`ファイルのひながた`template.mdp`を準備する。

`initial.mdp`から`template.mdp`への変更点はおおよそ以下の通り。

1. 計算時間を長くする。
2. それに応じて、スナップショットを出力する間隔を多少調整し、巨大すぎる出力にならないようにする。
3. 温度制御が必要な場合は`nose-hoover`にする。
4. 圧力制御が必要な場合は`c-rescale`または`parrinello-rahman`にする。(前者はisotropicセルにしか使えない)
5. 温度と圧力の部分は`{{T}}`, `{{P}}`と書いておく。あとで差し替える。

## 4. 自動処理

Gromacsで分子動力学シミュレーション計算を行う場合の一般的な手順は4段階あります。

1. 入力ファイル(テキストファイル)を準備する。
2. `gmx grompp`で`.tpr`ファイル(バイナリ)を作成する。
3. `gmx mdrun`で`.trr`ファイルや.edrファイル(バイナリ)を作成する。
4. バイナリファイルを`.gro`や`.mdinfo`ファイル(テキスト)に変換する。

この手順はすべての子ディレクトリで共通なので、1つのシェルスクリプトで実行できます。

具体例として、ベースディレクトリにある`template.mdp`の温度圧力を書きかえて子ディレクトリの`continue.mdp`を作成し、それを使って子ディレクトリ内で継続計算を行う方法を順番に書きます。

### 4.1 continue.mdpの生成

ここでは、pythonのjinja2を使ってパターンの置きかえを行うことにします。

温度と圧力に関しては、実際に作られた子ディレクトリのディレクトリ名から取得することにしました。

`prepare-childs.py`の中身です。
```python
#!/usr/bin/env python3
import os
import re
from glob import glob
from jinja2 import Template

def main():
    # テンプレートの読み込み
    with open('template.mdp', 'r') as f:
        template_str = f.read()
    template = Template(template_str)

    # *bar/*K という形式のディレクトリをすべて探す
    target_dirs = glob("*bar/*K")

    for d in target_dirs:
        # パスから温度(T)と圧力(P)を抽出
        # 例: 8000bar/160K -> P=8000, T=160
        match_p = re.search(r'(\d+)bar', d)
        match_t = re.search(r'(\d+)K', d)
        
        # ディレクトリ名が異常でなければ
        if match_p and match_t:
            p_val = match_p.group(1)
            t_val = match_t.group(1)
            
            output_path = os.path.join(d, 'continue.mdp')
            
            # もしすでにあれば上書きはしない。(日付が変わるとmakeがまた動いてしまう)
            if os.path.exists(output_path):
                print(f"Skipped (P={p_val}, T={t_val})")
                continue

            # レンダリング
            rendered_content = template.render(T=t_val, P=p_val)
            
            # ファイル書き出し
            with open(output_path, 'w') as f:
                f.write(rendered_content)
            print(f"Generated {output_path} (P={p_val}, T={t_val})")

if __name__ == "__main__":
    main()

```

### 4.2 `grompp`の実行

`.top`ファイル等はベースディレクトリにあるものを使えるので、子ディレクトリにコピーする必要はありません。

ベースディレクトリにいながら、子ディレクトリ内に00002.tprファイルを生成するコマンドはこんな感じになります。
```shell
CHILD=10000bar/140K
gmx grompp -maxwarn 2 -f $CHILD/continue.mdp -p TraPPE_Vega.top -o $CHILD/00002.tpr -c 00001-last.gro
```

`TraPPE_Vega.top`と`00001-last.gro`はベースディレクトリ(いまいるディレクトリ)にあるのでディレクトリの指示はありません。

### 4.3 `mdrun`の実行

これも同様です。
```shell
CHILD=10000bar/140K
time gmx mdrun -ntmpi 16 -ntomp 1 -notunepme -deffnm $CHILD/00002 -c $CHILD/00002-last.gro
```

計算結果は`$CHILD`ディレクトリに書かれるので、同時に異なる条件での計算を平行に実行しても、ファイルを上書きする心配はありません。

### 4.4 テキストファイルの生成

`mdrun`の実行中も、アニメーションのための`00002.gro`ファイルや、プロットのための`.mdinfo`ファイルは随時生成することができます。
これも子ディレクトリに移動せず、ベースディレクトリで作業することにしましょう。

```shell
echo 0 | gmx trjconv -f $(CHILD)/00002.trr -s $(CHILD)/00002.tpr -o $(CHILD)/00002.gro
```

```shell
gmx dump -e $(CHILD)/00002.edr | python3 undump.py > $@
```





