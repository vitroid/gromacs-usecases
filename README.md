

## homebrewを使ったインストール

Macの場合、homebrewでインストールすると楽なのだが、mixed precision(=単精度)になってしまうようだ。

1. `brew edit gromacs`でFormulaを編集。

```ruby
      system "cmake", "..", *std_cmake_args, "-DGROMACS_CXX_COMPILER=#{cxx}",
                                             "-DGMX_VERSION_STRING_OF_FORK=#{tap.user}"
```
を
```ruby
      system "cmake", "..", *std_cmake_args, "-DGROMACS_CXX_COMPILER=#{cxx}",
                                             "-DGMX_VERSION_STRING_OF_FORK=#{tap.user}",
                                             "-DGMX_DOUBLE=on"
```
に修正する。

2. `brew install --build-from-source gromacs`でインストール。

残念。エラーがでる。

## 一般的なインストール

```shell
mkdir gromacs
cd gromacs
wget https://ftp.gromacs.org/pub/gromacs/gromacs-2022.tar.gz
tar zxf gromacs-2022.tar.gz
cd gromacs
mkdir build
cd build
cmake .. -DGROMACS_CXX_COMPILER=/opt/homebrew/opt/gcc/bin/g++-11 -DGMX_VERSION_STRING_OF_FORK=Homebrew -DGMX_DOUBLE=on
MAKEFLAG=-j8 make -k


