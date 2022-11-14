all:
	cd $(SRC); make -j8 -k

install:
	cd $(SRC); make install

config:
	cd $(SRC); cmake .. $(FLAGS)

prepare:
	-cd $(SRCBASE); wget --no-check-certificate --no-clobber $(SRCURL) && tar zxf gromacs-2022.tar.gz
	-rm -rf $(SRC)
	-mkdir $(SRC)
