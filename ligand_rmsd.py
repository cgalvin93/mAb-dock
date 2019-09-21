'''
PSEUDOCODE

load native structure

for model pdb files:
	load file
	align native, model
	select native ligand
	select model ligand
	save native ligand
	save model ligand
	del model
	load natlig
	load modlig
	alter numbering
	rms
	rms ca
	write rms
	del natlig
	del modlig
	os.del ligs

for natlig[i],modlig[i]:
	load natlig
	load modlig
	alter the numberings to match
	rms 
	rms ca
	write rms/rms ca to outfile
'''	
#time ipython ligand_rmsd.py *.pdb

import __main__
__main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
from time import sleep
import pymol
pymol.finish_launching()
from pymol import cmd
import sys
import os

ofile = open('lig_rmsd_rel.txt','w')

native_complex = 'nat_relaxed.pdb'


for file in sys.argv[2:]:
	if file != native_complex and file != 'natlig.pdb' and file != 'modlig.pdb':
		print file
		cmd.load(native_complex,'native_complex')
		cmd.load(file, 'model_complex')
		cmd.align('native_complex', 'model_complex')
		cmd.select('natlig','native_complex and chain P')
		cmd.select('modlig','model_complex and chain C')
		cmd.save('natlig.pdb','natlig')
		cmd.save('modlig.pdb','modlig')
		cmd.delete('model_complex')
		cmd.delete('native_complex')
		cmd.load('natlig.pdb','native_ligand')
		cmd.load('modlig.pdb','model_ligand')
		cmd.alter('all','chain=""')
		cmd.alter('all','segi=""')
		cmd.select('natligca','native_ligand and name ca')
		cmd.select('modligca','model_ligand and name ca')
		rms_ca = cmd.rms_cur('natligca','modligca')
		ofile.write(file + ': ' + str(rms_ca) + '\n')
		cmd.delete('native_ligand')
		cmd.delete('model_ligand')
		os.remove('natlig.pdb')
		os.remove('modlig.pdb')
		
ofile.close()		

	



