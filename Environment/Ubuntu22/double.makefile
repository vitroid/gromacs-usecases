
# Install for mac
SRCBASE=~/gromacs
SRCURL=https://ftp.gromacs.org/pub/gromacs/gromacs-2022.tar.gz
SRC=~/gromacs/gromacs-2022/build
DEST=~/gromacs/Ubuntu22/2022_d/
FLAGS=	    -DCMAKE_INSTALL_PREFIX=$(DEST) \
		-DGMX_PREFER_STATIC_LIBS=ON \
		-DGMX_DOUBLE=ON \
		-DGMX_BUILD_OWN_FFTW=ON

include common.makefile


		# -DPython3_EXECUTABLE=/usr/local/bin/python3.10
		# -DGMX_FFT_LIBRARY=fftw3 \
		# -DCMAKE_C_COMPILER=/usr/local/bin/gcc \
		# -DCMAKE_CXX_COMPILER=/usr/local/bin/g++ \
		# -DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-11 \
		# -DCMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-11 \
		# -DCMAKE_OSX_SYSROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX12.3.sdk
