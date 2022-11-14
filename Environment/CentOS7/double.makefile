
# Install for mac
SRCBASE=~/Unison/gromacs
SRCURL=https://ftp.gromacs.org/pub/gromacs/gromacs-2022.tar.gz
SRC=~/Unison/gromacs/gromacs-2022/build
DEST=~/gromacs/2022_d/
FLAGS=	    -DCMAKE_INSTALL_PREFIX=$(DEST) \
		-DGMX_PREFER_STATIC_LIBS=ON \
		-DGMX_DOUBLE=ON  \
		-DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-11 \
		-DCMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-11 \
		-DCMAKE_OSX_SYSROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX12.3.sdk

include common.makefile
