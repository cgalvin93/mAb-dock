
from pyrosetta import *
init()
from pyrosetta.teaching import *


ogp = pose_from_pdb('start.pdb')

switch = SwitchResidueTypeSetMover("centroid")
switch.apply(ogp)

setup_foldtree(ogp,'LH_C',Vector1([1]))

scorefxn_low = create_score_function("interchain_cen")

'''
FOR GLOBAL DOCKING

import pyrosetta.rosetta.protocols.rigid as rigid_moves
from pyrosetta.rosetta.protocols.docking import *
randomize1=rigid_moves.RigidBodyRandomizeMover(p,jump_num,rigid_moves.partner_upstream)
randomize2=rigid_moves.RigidBodyRandomizeMover(p,jump_num,rigid_moves.partner_downstream)
slide = DockingSlideIntoContact(1)
movemap = MoveMap()
movemap.set_jump(1, True)
min_mover = MinMover()
min_mover.movemap(movemap)
min_mover.score_function(scorefxn_low)
'''

#FOR DOCKING WITH FAB BINDING SITE FIXED BUT RANDOMLY GENERATED LIG ORIENTATION

jd = PyJobDistributor('ran', 100, scorefxn_low)
jd.native_pose = ogp

import pyrosetta.rosetta.protocols.rigid as rigid_moves
from pyrosetta.rosetta.protocols.docking import *
slide = DockingSlideIntoContact(1)

movemap = MoveMap()
movemap.set_jump(1, True)
min_mover = MinMover()
min_mover.movemap(movemap)
min_mover.score_function(scorefxn_low)

dock_lowres = DockingLowRes(scorefxn_low, 1)

def run_protocol():			#running trials independently on the same starting structure is the way to go
	p = Pose()
	p.assign(ogp)
	#randomize1=rigid_moves.RigidBodyRandomizeMover(p,1,rigid_moves.partner_upstream)
	randomize2=rigid_moves.RigidBodyRandomizeMover(p,1,rigid_moves.partner_downstream)
	#randomize1.apply(p)
	randomize2.apply(p)
	slide.apply(p)
	min_mover.apply(p)
	dock_lowres.apply(p)
	jd.output_decoy(p)

while not jd.job_complete:
	run_protocol()

##################################################
#dock_lowres.set_rot_magnitude(15.0)
#dock_lowres.set_trans_magnitude(0.1)	

'''	
#FOR GENERATING STARTING STRC BY ROTATING LIGAND

jd = PyJobDistributor('spin_trials', 50, scorefxn_low)
jd.native_pose = ogp

import pyrosetta.rosetta.protocols.rigid as rigid_moves
#spin_mover = rigid_moves.RigidBodySpinMover(1)
movemap = MoveMap()
movemap.set_jump(1, True)
min_mover = MinMover()
min_mover.movemap(movemap)
min_mover.score_function(scorefxn_low)

def run_protocol():			#running trials independently on the same starting structure is the way to go
	p = Pose()
	p.assign(ogp)
	#spin_mover.apply(p)
	#randomize1=rigid_moves.RigidBodyRandomizeMover(p,1,rigid_moves.partner_upstream)
	#randomize2=rigid_moves.RigidBodyRandomizeMover(p,1,rigid_moves.partner_downstream)
	#randomize1.apply(p)
	#randomize2.apply(p)
	#slide.apply(p)
	min_mover.apply(p)
	dock_lowres.apply(p)
	jd.output_decoy(p)
	

while not jd.job_complete:
	run_protocol()	
'''
	
	
'''
real	7m2.678s to run the protocol 10 times

--------------------------------------------------------------------------------------------------------------------------------------

set_rot_magnitude(self: pyrosetta.rosetta.protocols.docking.DockingLowRes, rot_magnitude: float) → None
C++: protocols::docking::DockingLowRes::set_rot_magnitude(double) –> void

set_scorefxn(self: pyrosetta.rosetta.protocols.docking.DockingLowRes, scorefxn: pyrosetta.rosetta.core.scoring.ScoreFunction) → None
C++: protocols::docking::DockingLowRes::set_scorefxn(class std::shared_ptr<const class core::scoring::ScoreFunction>) –> void

set_trans_magnitude(self: pyrosetta.rosetta.protocols.docking.DockingLowRes, trans_magnitude: float) → None
C++: protocols::docking::DockingLowRes::set_trans_magnitude(double) –> void	

pyrosetta.rosetta.protocols.rigid.RigidBodySpinMover

pert_mover = rigid_moves.RigidBodyPerturbMover(jump_num,
8, 3)	 

spin_mover = rigid_moves.RigidBodySpinMover(1, 12)
--------------------------------------------------------------------------------------------------------------------------------------

HAD TO DELETE TWO RESIDUES IN THE PDB FILE THAT ROSETTA DIDNT RECOGNIZE AND THUS COULDNT CONVERT TO CENTROID

--------------------------------------------------------------------------------------------------------------------------------------

In [25]: print p.fold_tree()
FOLD_TREE  EDGE 1 212 -1  EDGE 1 213 1  EDGE 213 434 -1  EDGE 1 435 2  EDGE 435 458 -1 

In [26]: print p.pdb_info().chain(434)
H

In [27]: print p.pdb_info().chain(435)
C

In [28]: from pyrosetta.teaching import*

In [29]: setup_foldtree(p,'LH_C',Vector1([1]))

In [30]: print p.pdb_info().chain(435)
C

In [31]: print p.fold_tree()
FOLD_TREE  EDGE 1 39 -1  EDGE 39 212 -1  EDGE 39 442 1  EDGE 212 213 2  EDGE 442 435 -1  EDGE 442 458 -1  EDGE 213 434 -1 

In [32]: print p.jump(1)
RT 0.885303 -0.329052 0.328577 -0.457005 -0.485089 0.745544 -0.0859335 -0.810194 -0.579829 -5.315 -7.98309 32.7561  

In [33]: print p.jump(2)
RT -0.617704 0.750698 -0.234298 0.758606 0.647327 0.0740646 0.207267 -0.13199 -0.969339 39.2526 37.428 -5.88651  

In [34]: scorefxn_low = create_score_function("interchain_cen")

In [36]: switch = SwitchResidueTypeSetMover("centroid")
'''