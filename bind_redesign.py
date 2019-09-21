from pyrosetta import *
init()

ogpose = pose_from_pdb("fab.pdb")		#########INPUT
pose = Pose()
pose.assign(ogpose)

from pyrosetta.rosetta.protocols.simple_moves import *
sf = get_fa_scorefxn()

outfilename = 'results.txt'
ofile = open(outfilename, 'w')	

Ei = "Original energy:" + str(sf(pose))
ofile.write(Ei)		

binding_site_residues = [38,29,30,31,65,66,67,68,69,90,91,92,93,94,242, 243, 244, 245, 265,266,267,268,269,312,313,314,315,316]		######INPUT
#H 30-34, 53-57, 100-105 = 242, 243, 244, 245, 265,266,267,268,269,312,313,314,315,316
# L 28-31, 65-69, 90-94 = 38,29,30,31,65,66,67,68,69,90,91,92,93,94


task = standard_packer_task(p)
task.temporarily_fix_everything()

for i in binding_site_residues:					#allows design on the res in the list
	task.temporarily_set_pack_residue(i, True)

########### STEP 1 ################ repack native rotamers and minimize sc of binding site residues
#packer for repack binding site/substrate sc
from pyrosetta.rosetta.core.pack.task import *
task_design = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_design, "1kjg_repack_sc.resfile")
packmover = PackRotamersMover(sf, task_design)


############### minmover for minimizing relevant sidechains
min_mover = MinMover() 
minmap = MoveMap()	
minmap.set_bb(False)
minmap.set_chi(False)	
for i in binding_site_residues:	
	minmap.set_chi(i, True) 
min_mover.movemap(minmap)
min_mover.score_function(sf)

#10 decoys from sc repacking/minimization
for i in range(10):
	pose.assign(ogpose)
	packmover.apply(pose)
	min_mover.apply(pose)
	Escmin = "\nreference energy:" + str(sf(pose))
	ofile.write(Escmin)		#need to make string????????????????????????

	
########### STEP 2 ################	 allow redesign on res 2-9 in chain p (substrate), one at a time, while sc repacking and
# min is kept the same as in step 1; 10 decoys for each with energies recorded

#residue 2:
pose.assign(ogpose)
task_2 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_2, "design_2.resfile")
p2m = PackRotamersMover(sf, task_2)
OG = "\nThe original residue 2 is:" + str(pose.residue(199).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p2m.apply(pose)
	min_mover.apply(pose)
	E2 = "\nredesign on 2 energy is:" + str(sf(pose)) + "\nres 2 id is:" + str(pose.residue(199).name())				
	ofile.write(E2)
	
#residue 3:
pose.assign(ogpose)
task_3 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_3, "design_3.resfile")
p3m = PackRotamersMover(sf, task_3)
OG = "\nThe original residue 3 is:" + str(pose.residue(200).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p3m.apply(pose)
	min_mover.apply(pose)
	E3 = "\nredesign on 3 energy is:" + str(sf(pose)) + "\nres 3 id is:" + str(pose.residue(200).name())				
	ofile.write(E3)	
	
#residue 4:
pose.assign(ogpose)
task_4 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_4, "design_4.resfile")
p4m = PackRotamersMover(sf, task_4)
OG = "\nThe original residue 4 is:" + str(pose.residue(201).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p4m.apply(pose)
	min_mover.apply(pose)
	E4 = "\nredesign on 4 energy is:" + str(sf(pose)) + "\nres 4 id is:" + str(pose.residue(201).name())				
	ofile.write(E4)		
	
#residue 5:
pose.assign(ogpose)
task_5 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_5, "design_5.resfile")
p5m = PackRotamersMover(sf, task_5)
OG = "\nThe original residue 5 is:" + str(pose.residue(202).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p5m.apply(pose)
	min_mover.apply(pose)
	E5 = "\nredesign on 5 energy is:" + str(sf(pose)) + "\nres 5 id is:" + str(pose.residue(202).name())				
	ofile.write(E5)			

#residue 6:
pose.assign(ogpose)
task_6 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_6, "design_6.resfile")
p6m = PackRotamersMover(sf, task_6)
OG = "\nThe original residue 6 is:" + str(pose.residue(203).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p6m.apply(pose)
	min_mover.apply(pose)
	E6 = "\nredesign on 6 energy is:" + str(sf(pose)) + "\nres 6 id is:" + str(pose.residue(203).name())				
	ofile.write(E6)			
	
#residue 7:
pose.assign(ogpose)
task_7 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_7, "design_7.resfile")
p7m = PackRotamersMover(sf, task_7)
OG = "\nThe original residue 7 is:" + str(pose.residue(204).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p7m.apply(pose)
	min_mover.apply(pose)
	E7 = "\nredesign on 7 energy is:" + str(sf(pose)) + "\nres 7 id is:" + str(pose.residue(204).name())				
	ofile.write(E7)		
	
#residue 8:
pose.assign(ogpose)
task_8 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_8, "design_8.resfile")
p8m = PackRotamersMover(sf, task_8)
OG = "\nThe original residue 8 is:" + str(pose.residue(205).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p8m.apply(pose)
	min_mover.apply(pose)
	E8 = "\nredesign on 8 energy is:" + str(sf(pose)) + "\nres 8 id is:" + str(pose.residue(205).name())				
	ofile.write(E8)			
	
#residue 9:
pose.assign(ogpose)
task_9 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_9, "design_9.resfile")
p9m = PackRotamersMover(sf, task_9)
OG = "\nThe original residue 9 is:" + str(pose.residue(206).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p9m.apply(pose)
	min_mover.apply(pose)
	E9 = "\nredesign on 9 energy is:" + str(sf(pose)) + "\nres 9 id is:" + str(pose.residue(206).name())				
	ofile.write(E9)		
	
#residue 10:
pose.assign(ogpose)
task_10 = TaskFactory.create_packer_task(pose)
parse_resfile(pose, task_10, "design_10.resfile")
p10m = PackRotamersMover(sf, task_10)
OG = "\nThe original residue 10 is:" + str(pose.residue(207).name())	
ofile.write(OG)

for i in range(10):
	pose.assign(ogpose)
	p10m.apply(pose)
	min_mover.apply(pose)
	E10 = "\nredesign on 10 energy is:" + str(sf(pose)) + "\nres 10 id is:" + str(pose.residue(207).name())				
	ofile.write(E10)	
	
ofile.close()