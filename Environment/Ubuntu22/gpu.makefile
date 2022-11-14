
# Install for mac
SRCBASE=~/gromacs
SRCURL=https://ftp.gromacs.org/pub/gromacs/gromacs-2022.tar.gz
SRC=~/gromacs/gromacs-2022/build
DEST=~/gromacs/Ubuntu22/2022_g/
FLAGS=	    -DCMAKE_INSTALL_PREFIX=$(DEST) \
		-DGMX_PREFER_STATIC_LIBS=ON \
		-DGMX_DOUBLE=OFF \
		-DGMX_BUILD_OWN_FFTW=ON \
        -DGMX_GPU=OpenCL

include common.makefile
