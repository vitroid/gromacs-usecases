
# Install for mac
SRCBASE=~/Unison/gromacs
SRCURL=https://ftp.gromacs.org/pub/gromacs/gromacs-2022.tar.gz
SRC=~/Unison/gromacs/gromacs-2022/build
DEST=~/gromacs/2022/

all:
	cd $(SRC); make -j8 -k

install:
	cd $(SRC); make install

config:
	cd $(SRC); cmake .. \
	    -DCMAKE_INSTALL_PREFIX=$(DEST) \
		-DGMX_PREFER_STATIC_LIBS=ON \
		-DGMX_DOUBLE=ON  \
		-DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-11 \
		-DCMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-11

prepare:
	-cd $(SRCBASE); wget --no-clobber $(SRCURL) && tar zxf gromacs-2022.tar.gz
	-mkdir $(SRC)
