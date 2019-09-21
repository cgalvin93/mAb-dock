#time ipython compare_models.py *.pdb
from pyrosetta import*
init()
import sys
import __main__
__main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
from time import sleep
import pymol
pymol.finish_launching()
from pymol import cmd

ofile = open('zdock_models.sc','w')

#construction of high resolution docking scorefunction
sf_dock = ScoreFunction()
from pyrosetta.rosetta.core.scoring import fa_atr, fa_rep, fa_sol, hbond_sr_bb, hbond_lr_bb, hbond_bb_sc, hbond_sc, fa_elec, dslf_ss_dst,dslf_cs_ang,dslf_ss_dih,dslf_ca_dih, dslf_fa13,rama, omega,ref
#fa_dun,

sf_dock.set_weight(fa_atr, 0.423)
sf_dock.set_weight(fa_rep, 0.100)
sf_dock.set_weight(fa_sol, 0.372)	
#sf_dock.set_weight(fa_dun, 0.064)    		 Could not get rotamer specification for ASN:AcetylatedNtermProteinFull.
sf_dock.set_weight(hbond_sr_bb, 0.245)
sf_dock.set_weight(hbond_lr_bb, 0.245)
sf_dock.set_weight(hbond_bb_sc, 0.245)
sf_dock.set_weight(hbond_sc, 0.245)
sf_dock.set_weight(fa_elec, 0.026)
sf_dock.set_weight(dslf_ss_dst,1.0)
sf_dock.set_weight(dslf_cs_ang,1.0)
sf_dock.set_weight(dslf_ss_dih,1.0)
sf_dock.set_weight(dslf_ca_dih, 1.0)
sf_dock.set_weight(dslf_fa13,1.0)
sf_dock.set_weight(rama, 0.2)
sf_dock.set_weight(omega, 0.5)
sf_dock.set_weight(ref, 1.0)	


native_pose = pose_from_pdb('3ixt.clean.pdb')
native_score = str(sf_dock(native_pose))	#load native complex for rmsd comparison


pymol_native_pose = '3ixt.clean.pdb'
cmd.load(pymol_native_pose,"native")

ofile.write("Native Score: " + native_score + '\n')

results = []
for file in sys.argv[2:]:	
	pose = pose_from_pdb(str(file))
	score = str(sf_dock(pose))
	cmd.load(file,"the_model")
	cmd.align("native","the_model")
	cmd.rms_cur('3ixt.clean','cleancomplex.5')
	cmd.delete("the_model")
	result = str(file) + ": " + score + " RMSD: " + str(rms) 
	results.append(result)

for x in range(len(results)):
	ofile.write(results[x] + '\n')	
	
	
	
ofile.close()	

'''
ERROR: Error in core::pack::dunbrack::RotamericSingleResidueDunbrackLibrary::get_bbs_from_rsd():
 Residues with rotamers dependent on a subset of backbone torsions must use NCAARotamerLibrarySpecifactions.  
 Could not get rotamer specification for ASN:AcetylatedNtermProteinFull.
 
I'll guess it's the fa_dun term and get rid of that for now
 
 
NameError: name 'CA_rmsd' is not defined

I'll add from teaching import since that's the nly other import I used during the tutorial when this function worked fine. 
Actually I also imported from rigid moves but that seems less likely to matter.

ERROR: Assertion `subset.size() == pose1.size()` failed.

okay wont work now cus pose lengths are different, lemme just try lrmsd 

NOPE

that doesn't work either, so ill just get the scores for now and try to look at the rmsd using pymol

THAT WORKED

at least, but now to incorporate pymols rmsd function


MYSTERIOUS ERROR WITH PYMOL ALIGN FUNCTION NOW

the error was overcome by changing the model name from 'model' to 'the_model', so i guess using model as a name is off limits



'''