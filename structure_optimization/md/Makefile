GMX = /Users/matto/gromacs/2022/bin/gmx_d  #double precision but too slow
GMX = gmx                                  #homebrew

all:
	for str in TS1x222 HS1x222 CS1x222 CS2x222 C14x222; do echo $$str.0.q.gro; done | xargs make -k
%x444.0.gro:
	genice2 $* -r 4 4 4 -w ice > $@
%x222.0.gro:
	genice2 $* -r 2 2 2 -w ice > $@
%x111.0.gro: Makefile
	genice2 $* -w ice > $@
%.gro.top: %.gro
	awk 'BEGIN{getline;getline;print "#include \"optim.top\""; print "[ molecules ]";print "ICE ",$$0/4}' $< > $@
%.tpr: %.gro optim.top optim.mdp %.gro.top
	$(GMX) grompp -f optim.mdp -p $*.gro.top -c $*.gro -o $*.tpr # >& $*.gentpr.log
%.q.gro: %.tpr Makefile
	$(GMX) mdrun -s $*.tpr -o $*.trr -g $@.log -e $@.edr -c $*.q.gro
# %.q.gro: %.trr
# 	echo 0 | $(GMX) trjconv -s $*.tpr -f $*.trr -o $@ -ndec 12
# %.vol: %.gro volume.py
# 	python volume.py < $< > $@

clean:
	-rm '#'* mdout.mdp *.cpt
distclean: clean
	-rm *.gro *.tpr *.trr *.edr *.log