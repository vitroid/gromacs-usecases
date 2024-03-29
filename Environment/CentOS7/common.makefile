all:
	cd $(SRC); make -j32 -k

install:
	cd $(SRC); make install

config:
	cd $(SRC); cmake3 .. $(FLAGS)

prepare:
	-cd $(SRCBASE); wget --no-check-certificate --no-clobber $(SRCURL) && tar zxf gromacs-2022.tar.gz
	-mkdir $(SRC)

clean:
	-rm -rf $(SRC)
