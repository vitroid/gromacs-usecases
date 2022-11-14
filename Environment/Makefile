00001.trr: 00001.tpr
	gmx mdrun -deffnm 00001 -nt 8
00001.tpr: ice.gro
	gmx grompp -maxwarn 1 -f relax.mdp -p ice.top -o 00001.tpr -c ice.gro

ice.gro: Makefile
	genice2 1h -r 16 16 16 -w tip4p  > $@
