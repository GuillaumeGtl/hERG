import chimera
from chimera import runCommand as rc
from chimera.selection import currentResidues
import numpy as np
from chimera.specifier import evalSpec
from Rotamers import getRotamers
import os

newAA = "TYR"
posAA = "673"

## get the list of residues in the 5 angstom zone around selected residue
def zone(res):
    rc("select :"+str(res)+".a za<5")
    residues_in_zone = currentResidues()
    residues_index = []
    for residue in residues_in_zone:
        residues_index.append(residue.id.position)
    return residues_index

## get the number of clashes from findclash file
def clashes(file,residue_index):
    clash_file = open(file,'r')
    content = clash_file.readlines()
    clash_file.close()
    start = content.index("\n")
    nb_of_clashes = int(content[start+1].split()[0])
    if not nb_of_clashes:
        return nb_of_clashes
    for ligne in content[start+3:]:
        l = ligne.split()
        involved_residues = [l[1].split(".")[0],l[4].split(".")[0]]
        if str(residue_index) not in involved_residues:
            nb_of_clashes -= 1
    return nb_of_clashes

## we open chimera for the first time to get the rotamers and their probabilities of the mutated AA
chimera.openModels.open("C:/Users/Guillaume/Desktop/hERG/New_Code/hERG.pdb")
f = open("output.txt","w")
rc("swapaa "+newAA+" :"+posAA+".a") #mutate the residue
r = evalSpec(" :"+posAA+".a").residues()[0] #get the AA object at the position
f.write(str(r)+"\n")
rotamers = getRotamers(r) #get the rotamers of the AA
proba_rotamer = []
for i in range(len(rotamers[1])): #get the probability of the rotamers
    proba_rotamer.append(rotamers[1][i].rotamerProb) 
f.write(str(proba_rotamer)+"\n")
rc("close session")
#if a proba of a rotamer is >= 10% it's considered,
#if no rotamers have a probability above 10%, we consider only the 3 firsts
nb_of_interest_rot = 0
for e in proba_rotamer :
    if e >= 0.1:
        nb_of_interest_rot += 1
if not nb_of_interest_rot:
    nb_of_interest_rot = 3
f.write(str(nb_of_interest_rot)+"\n")

# get the numbers of clashes for each intersting rotamers, minimize the structure for each, and get the new number of clashes
clashes_of_rota = []
clashes_of_rota_after = []
for i in range(nb_of_interest_rot):
    chimera.openModels.open("C:/Users/Guillaume/Desktop/hERG/New_Code/hERG.pdb")
    rc("swapaa "+newAA+" :"+posAA+".a criteria {}".format(i+1))
    rc("addh spec sel")
    rc("select :"+posAA+".a za<5")
    rc("findclash sel test self ignoreIntraRes true colorClashes true clashColor red saveFile clashes{}.txt namingStyle simple summary true log true".format(i+1))
    clashes_of_rota.append(clashes("clashes{}.txt".format(i+1),posAA))
    rc("close session")
f.write(str(clashes_of_rota)+"\n")

for i in range(nb_of_interest_rot):
    if clashes_of_rota[i]:
        chimera.openModels.open("C:/Users/Guillaume/Desktop/hERG/New_Code/hERG.pdb")
        rc("select :"+posAA+".a za<5")
        rc("minimize spec sel nogui True nsteps 10 cgsteps 0 ")
        rc("findclash sel test self ignoreIntraRes true colorClashes true clashColor red saveFile clashes{}.txt namingStyle simple summary true log true".format(i+1))
        clashes_of_rota_after.append(clashes("clashes{}.txt".format(i+1),posAA))
        rc("close session")

f.write(str(clashes_of_rota_after))

rc("stop")
f.close()



#test















