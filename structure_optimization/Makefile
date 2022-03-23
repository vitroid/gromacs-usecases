GMX = /Users/matto/gromacs/2022/bin/gmx_d  #double precision but too slow
GMX = gmx                                  #homebrew

all:
	for str in TS1x222 HS1x222 CS1x222 CS2x222 C14x222 C36x222 mux222 Tx111 px222 psigmax222 10qc6 12qc1; do echo $$str.all; done | xargs make -k
%.all: 
	make $*.gro
	make $*.0.q.gro
	make $*.0.q.xvg
	make $*.1.q.gro
	make $*.1.q.xvg
	echo done.
10qc6.gro:
	genice2 cockayne[6] -w ice > $@
12qc1.gro:
	genice2 stampfli[1] -w ice > $@
%x444.gro:
	genice2 $* -r 4 4 4 -w ice > $@
%x222.gro:
	genice2 $* -r 2 2 2 -w ice > $@
%x111.gro:
	genice2 $* -w ice > $@
%.gro.top: %.gro
	awk 'BEGIN{getline;getline;print "#include \"optim.top\""; print "[ molecules ]";print "ICE ",$$0/4}' $< > $@
%.0.tpr: %.gro optim.top optim.mdp %.gro.top
	$(GMX) grompp -f optim.mdp -p $*.gro.top -c $*.gro -o $*.0.tpr # >& $*.0.gentpr.log
# extract potential energy and volume
%.0.q.xvg: %.0.q.gro.edr
	echo 10 15 0 | $(GMX) energy -f $< -o $@
%.1.q.xvg: %.1.q.gro.edr Makefile
	echo 5 0 | $(GMX) energy -f $< -o $@
%.q.gro: %.tpr
	$(GMX) mdrun -s $*.tpr -o $*.trr -g $@.log -e $@.edr -c $*.q.gro
%.1.tpr: %.0.q.gro optim.top steep.mdp %.gro.top
	$(GMX) grompp -f steep.mdp -p $*.gro.top -c $*.0.q.gro -o $*.1.tpr # >& $*.1.gentpr.log
# %.q.gro: %.trr
# 	echo 0 | $(GMX) trjconv -s $*.tpr -f $*.trr -o $@ -ndec 12
# %.vol: %.gro volume.py
# 	python volume.py < $< > $@

clean:
	-rm '#'* mdout.mdp *.cpt
distclean: clean
	-rm *.gro *.tpr *.trr *.edr *.log *.xvg