まだどれも確認できていない。


# 単精度

## homebrewでインストールする。

```shell
brew install gromacs
```

GPU対応。

## コンパイルしてインストールする。

```shell
make -f single.makefile prepare
make -f single.makefile config
make -f single.makefile
make -f single.makefile install
```

実行ファイルは~/gromacs/2022_s/binにインストールされるので、
```shell
source ~/gromacs/2022_s/bin/GMXRC.bash
```
でパスを通しておく。



# 倍精度

```shell
make -f double.makefile prepare
make -f double.makefile config
make -f double.makefile
make -f double.makefile install
```

実行ファイルは~/gromacs/2022_d/binにインストールされるので、
```shell
source ~/gromacs/2022_d/bin/GMXRC.bash
```
でパスを通しておく。

# 単精度+GPU

```shell
make -f gpu.makefile prepare
make -f gpu.makefile config
make -f gpu.makefile
make -f gpu.makefile install
```

実行ファイルは~/gromacs/2022_g/binにインストールされるので、
```shell
source ~/gromacs/2022_g/bin/GMXRC.bash
```
でパスを通しておく。
