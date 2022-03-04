GMX = /Users/matto/gromacs/2022/bin/gmx_d  #double precision but too slow
GMX = gmx                                  #homebrew

1h.gro:
	genice2 1h -r 4 4 4 -w ice > $@
%.tpr: %.gro optim.top optim.mdp
	$(GMX) grompp -f optim.mdp -p optim.top -c $*.gro -o $*.tpr # >& $*.gentpr.log
%.trr: %.tpr
	$(GMX) mdrun -s $*.tpr -o $@
%-last.gro: %.trr
	echo 0 | $(GMX) trjconv -s $*.tpr -f $*.trr -o $@ -ndec 12

clean:
	-rm '#'* mdout.mdp *.cpt
distclean: clean
	-rm *.gro *.tpr *.trr *.edr *.log