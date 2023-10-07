import chimera
from chimera import runCommand as rc
from chimera.selection import currentResidues
import numpy as np
from chimera.specifier import evalSpec
from Rotamers import getRotamers
import os

newAA = "ALA"
posAA = "673"
pdb_file = "C:/Users/Guillaume/Desktop/hERG/New_Code/hERG.pdb"
ROTA_PROB_THRESHOLD = 0.1
MIN_NUM_ROTA = 3


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

## get probability of rotamers of amino acid "AA" at position "pos"
def get_rota(AA,pos):
    rc("swapaa "+AA+" :"+pos+".a")
    r = evalSpec(" :"+pos+".a").residues()[0]
    try : 
        (flag,rotamers) = getRotamers(r)
    except :
        return r,[]
    proba_rotamer = []
    for i in range(len(rotamers)):
        proba_rotamer.append(rotamers[i].rotamerProb)
    return r,proba_rotamer
    
def clash(AA,pos,rot):
    #chimera.openModels.open(pdb_file)
    rc("swapaa "+AA+" :"+pos+".a criteria "+rot)
    rc("addh spec sel")
    rc("select :"+pos+".a za<5")
    rc("findclash sel test self ignoreIntraRes true colorClashes true clashColor red saveFile clashes{}.txt namingStyle simple summary true log true".format(rot))



f = open("output.txt","w")
## we open chimera for the first time to get the rotamers and their probabilities of the mutated AA
chimera.openModels.open(pdb_file)
r,proba_rotamer = get_rota(newAA,posAA)


## log

f.write("residue : \n")
f.write(str(r)+"\n")
f.write("proba rota : \n")
f.write(str(proba_rotamer)+"\n")

#if a proba of a rotamer is >= ROTA_PROB_THRESHOLD % it's considered,
#if no rotamers have a probability above ROTA_PROB_THRESHOLD %, we consider only the MIN_NUM_ROTA firsts
nb_of_interest_rot = len([e for e in proba_rotamer if e > ROTA_PROB_THRESHOLD])
if not nb_of_interest_rot:
    nb_of_interest_rot = MIN_NUM_ROTA

if not len(proba_rotamer):
    nb_of_interest_rot = 0
f.write(str(nb_of_interest_rot)+"\n")


# get the numbers of clashes for each intersting rotamers, minimize the structure for each, and get the new number of clashes
clashes_of_rota = []
clashes_of_rota_after = []

rc("close session")
chimera.openModels.open(pdb_file)
for i in range(nb_of_interest_rot):
    clash(newAA,posAA,str(i+1))
    clashes_of_rota.append(clashes("clashes{}.txt".format(i+1),posAA))
f.write(str(clashes_of_rota)+"\n")

rc("close session")
for i in range(nb_of_interest_rot):
    if clashes_of_rota[i]:
        chimera.openModels.open(pdb_file)
        rc("select :"+posAA+".a za<5")
        rc("minimize spec sel nogui True nsteps 10 cgsteps 0 ")
        rc("findclash sel test self ignoreIntraRes true colorClashes true clashColor red saveFile clashes{}.txt namingStyle simple summary true log true".format(i+1))
        clashes_of_rota_after.append(clashes("clashes{}.txt".format(i+1),posAA))

f.write(str(clashes_of_rota_after))

rc("stop")
f.close()



















