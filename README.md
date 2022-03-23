

## homebrewを使ったインストール

### 単精度

```shell
brew install gromacs
```

### 倍精度

Best practiceはMakefileに書いておく。

```shell
make prepare
make config
make
make install
```

実行ファイルは~/gromacs/2022/binにインストールされるので、
```shell
source ~/gromacs/2022/bin/GMXRC.bash 
```
でパスを通しておく。
