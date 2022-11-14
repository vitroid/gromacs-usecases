GMX=gmx

00001.trr: 00001.tpr
	# $(GMX) mdrun -deffnm 00001 -nt 8 -nb gpu -pme gpu -bonded gpu -update gpu
	$(GMX) mdrun -deffnm 00001 -nt 8 -nb gpu -pme gpu -update gpu
00001.tpr: ice.gro
	$(GMX) grompp -maxwarn 1 -f relax.mdp -p ice.top -o 00001.tpr -c ice.gro

ice.gro: Makefile
	genice2 1h -r 16 16 16 -w tip4p  > $@
