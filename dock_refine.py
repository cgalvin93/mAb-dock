from pyrosetta import *
init() 
from pyrosetta.teaching import *
 
 
#construction of high resolution docking scorefunction
sf_dock = ScoreFunction()
from pyrosetta.rosetta.core.scoring import fa_atr, fa_rep, fa_sol, hbond_sr_bb, hbond_lr_bb, hbond_bb_sc, hbond_sc, fa_elec, dslf_ss_dst,dslf_cs_ang,dslf_ss_dih,dslf_ca_dih, dslf_fa13,rama, omega,ref

sf_dock.set_weight(fa_atr, 0.423)
sf_dock.set_weight(fa_rep, 0.100)
sf_dock.set_weight(fa_sol, 0.372)	
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
		
				
#setup job distributor for outputting results of refinement protocol runs; for now just use initial 
#for rmsd comparisons so i can see how much different output is
jd = PyJobDistributor("ran_27_refine", 3, sf_dock)
ogp = pose_from_pdb('ran_27.pdb')
jd.native_pose = ogp

#set up the high res docking protocol and give it the scorefunction and chains of ptn/ligand
dock_hires = DockMCMProtocol()
dock_hires.set_scorefxn(sf_dock)
dock_hires.set_scorefxn_pack(sf_dock)		#to get around non dunbrack rotamer problem in packing stage
dock_hires.set_partners("LH_C")

#copy the original pose onto a working pose object
def run_protocol():
	p = Pose()
	p.assign(ogp)
	dock_hires.apply(p)
	jd.output_decoy(p)


#perform the protocol on the working pose and output the result
while not jd.job_complete:
	run_protocol()



'''
cmd.select(string name, string selection)
cmd.save('filename','selection')

cmd.alter('all','chain=""')
cmd.alter('all','segi=""')

print cmd.rms_cur('nativeligand','modelligand')

5 models
real	96m32.176s
user	95m3.191s
sys	0m21.179s

'''




#FIRST STEP IS TO COMPARE SCORES AND RMSD OF ZDOCK MODELS WITH 3IXT SO I CAN PICK THE BEST ONE FOR A REFINEMENT PROTOCOL
#ILL DO THIS IN A SEPARATE SCRIPT CALLED COMPARE_MODELS.PY	


#REFINEMENT PROTOCOL TAKES ABOUT 21m26.234s PER RUN

															
'''
5 continuous runs energy did not change at all
real	96m32.176s
user	95m3.191s
sys	0m21.179s

from pyrosetta.teaching import *
#check chain jump between protein/substrate, might have to setup fold tree manually 
print pose.fold_tree()
p.pdb_info().chain(107)
p.pdb_info().chain(108)
setup_foldtree(pose, "A_B", Vector1([1]))
print pose.fold_tree()

jump_num = 1 #check rotation matrix and translation vector of jump
print pose.jump(jump_num).get_rotation()
print pose.jump(jump_num).get_translation()

In [5]: p = pose_from_pdb('cleancomplex.8.pdb')
In [6]: print p.fold_tree()
FOLD_TREE  EDGE 1 212 -1  EDGE 1 213 1  EDGE 213 434 -1  EDGE 1 435 2  EDGE 435 458 -1 

In [7]: p.pdb_info().chain(212)
Out[7]: u'L'

In [8]: p.pdb_info().chain(213)
Out[8]: u'H'

In [9]: p.pdb_info().chain(434)
Out[9]: u'H'

In [10]: p.pdb_info().chain(435)
Out[10]: u'C'
'''




'''
FOR LOW RESOLUTION GLOBAL DOCKING 

scorefxn_low = create_score_function("interchain_cen")


dock_lowres = DockingLowRes(scorefxn_low, jump_num)
dock_lowres.apply(pc)

import rosetta.protocols.rigid as rigid_moves
pert_mover = rigid_moves.RigidBodyPerturbMover(jump_num,
8, 3)	 

randomize1=rigid_moves.RigidBodyRandomizeMover(p,jump_num,rigid_moves.partner_upstream)
randomize2=rigid_moves.RigidBodyRandomizeMover(p,jump_num,rigid_moves.partner_downstream)

from rosetta.protocols.docking import *
#slide = DockingSlideIntoContact(jump_num) # for centroid mode
slide = FaDockingSlideIntoContact(jump_num) # for fullatom mode
slide.apply(p)

movemap = MoveMap()
movemap.set_jump(jump_num, True)
min_mover = MinMover()
min_mover.movemap(movemap)
min_mover.score_function(scorefxn) # use any scorefxn
scorefxn(p)
min_mover.apply(p)
'''


'''
weights from docking.wts patch file vs talaris2013 stdrd:
fa_atr *= 0.423			( fa_atr; 0.8) 
fa_rep *= 0.100			( fa_rep; 0.44)
fa_sol *= 0.372			( fa_sol; 0.75) 
fa_intra_rep *= 0.000   ( fa_intra_rep; 0.004) 
fa_pair *= 0.000
fa_dun *= 0.064			( fa_dun; 0.56) 
hbond_lr_bb *= 0.245	 ( hbond_lr_bb; 1.17) 
hbond_sr_bb *= 0.245	 ( hbond_sr_bb; 1.17) 
hbond_bb_sc *= 0.245	 ( hbond_bb_sc; 1.17) 
hbond_sc *= 0.245		( hbond_sc; 1.1)  
p_aa_pp *= 0.00			 ( p_aa_pp; 0.32) 
fa_elec = 0.026			( fa_elec; 0.7) 
dslf_ss_dst *= 1.0
dslf_cs_ang *= 1.0
dslf_ss_dih *= 1.0
dslf_ca_dih *= 1.0
pro_close *= 0.000	   ( pro_close; 1) 
						( dslf_fa13; 1)
						 ( rama; 0.2) 
 						( omega; 0.5) 
 						 ( ref; 1) 
so for now I'm going to use the patch weights, plus the weights for the terms not present in the patch. my assumption is that the patch only changes the 
weights of the specified terms, but the other terms in talaris13 stay as they are
''' 	