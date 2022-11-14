


# 単精度

## homebrewでインストールする。

```shell
brew install gromacs
```

GPUには対応しない。速度はあまり出ないかも。

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

# Benchmark

* M1/`-nt 8`: 2.44 ns/day
* M1/`-nt 4`: 2.22 ns/day

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

# Benchmark

* M1/`-nt 8`: 3.026 ns/day (?? 倍精度になってないかも)
* M1/`-nt 4`: ns/day


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

LYNCがOpenCLに対応していないため実質使えない。
