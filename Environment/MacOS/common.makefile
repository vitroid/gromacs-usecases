all:
	cd $(SRC); make -j8 -k

install:
	cd $(SRC); make install

config:
	cd $(SRC); cmake .. $(FLAGS)

prepare:
	-cd $(SRCBASE); wget --no-clobber $(SRCURL) && tar zxf gromacs-2022.tar.gz
	-mkdir $(SRC)

clean:
	-rm -rf $(SRC)
