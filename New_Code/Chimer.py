
##### MODULES #####

import chimera
from chimera import runCommand as rc
from chimera.selection import currentResidues
import numpy as np
from chimera.specifier import evalSpec
from Rotamers import getRotamers
import os


##### CONFIGURATION #####

f = open("config.txt","r")
content = f.readlines()
config = eval(content[0])

preAA = config["preAA"]
newAA = config["newAA"]
posAA = config["posAA"]
pdb_file = config["pdb_file"]
ROTA_PROB_THRESHOLD = config["ROTA_PROB_THRESHOLD"]
MIN_NUM_ROTA = config["MIN_NUM_ROTA"]
NUM_MINIM_STEP = config["NUM_MINIM_STEP"]
minimize = config["minimize"]


##### FONCTIONS #####

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

## get the list of amino acids in contact from findclash output contact file
def contacts(file,residue_index):
    contact_file = open(file,'r')
    content = contact_file.readlines()
    contact_file.close()
    start = content.index("\n")
    nb_of_contact = int(content[start+1].split()[0])
    if not nb_of_contact:
        return []
    involved_residues = []
    for ligne in content[start+3:]:
        l = ligne.split()
        contact = [l[1].split(".")[0],l[4].split(".")[0]]
        if str(residue_index) in contact:
            contact.pop(contact.index(residue_index))
            remaining_residue = contact[0]
            if remaining_residue not in involved_residues:
                involved_residues.append(remaining_residue)
    return involved_residues
            

            
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

## get the list of clashes from a rotamer in a file   
def clash(AA,pos,rot,overlap,allowance,name):
    rc("swapaa "+AA+" :"+pos+".a criteria "+rot)
    rc("addh spec sel")
    rc("select :"+pos+".a za<5")
    rc("findclash sel test self overlapCutoff {} hbondAllowance {} ignoreIntraRes true colorClashes true clashColor red saveFile {}{}.txt namingStyle simple summary true log true".format(overlap,allowance,name,rot))

## minimise and 
def mini(AA,pos,step,rot):
    rc("swapaa "+AA+" :"+pos+".a criteria "+rot)
    rc("addh spec sel")
    rc("select :"+pos+".a za<5")
    rc("minimize spec sel nogui True nsteps {} cgsteps 0 ".format(step))
    rc("findclash sel test self ignoreIntraRes true colorClashes true clashColor red saveFile clash_post{}.txt namingStyle simple summary true log true".format(rot))



d = {'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K',
     'Ile': 'I', 'Pro': 'P', 'Thr': 'T', 'Phe': 'F', 'Asn': 'N', 
     'Gly': 'G', 'His': 'H', 'Leu': 'L', 'Arg': 'R', 'Trp': 'W', 
     'Ala': 'A', 'Val':'V', 'Glu': 'E', 'Tyr': 'Y', 'Met': 'M',
     'C': 'Cys', 'D': 'Asp', 'S': 'Ser', 'Q': 'Gln', 'K': 'Lys',
     'I': 'Ile', 'P': 'Pro', 'T': 'Thr', 'F': 'Phe', 'N': 'Asn', 
     'G': 'Gly', 'H': 'His', 'L': 'Leu', 'R': 'Arg', 'W': 'Trp', 
     'A': 'Ala', 'V': 'Val', 'E': 'Glu', 'Y': 'Tyr', 'M': 'Met'}


##### PRINCIPAL #####

f = open(d[preAA]+posAA+d[newAA]+".txt","w")
## we open chimera for the first time to get the rotamers and their probabilities of the mutated AA
chimera.openModels.open(pdb_file)
r,proba_rotamer = get_rota(newAA,posAA)

## log
f.write("proba rota : ")
f.write(str(proba_rotamer)+"\n")
rc("close session")
#if a proba of a rotamer is >= ROTA_PROB_THRESHOLD % it's considered,
#if no rotamers have a probability above ROTA_PROB_THRESHOLD %, we consider only the MIN_NUM_ROTA firsts
nb_of_interest_rot = len([e for e in proba_rotamer if e > ROTA_PROB_THRESHOLD])
if not nb_of_interest_rot:
    nb_of_interest_rot = MIN_NUM_ROTA

if not len(proba_rotamer):
    nb_of_interest_rot = 0
f.write("Nombre de rotamers interessants : "+str(nb_of_interest_rot)+"\n")


# get the numbers of clashes and contacts for each intersting rotamers
clashes_of_rota = []
contacts_of_rota = []
chimera.openModels.open(pdb_file)
for i in range(nb_of_interest_rot):
    clash(newAA,posAA,str(i+1),0.6,0.4,"clash")
    clashes_of_rota.append(clashes("clash{}.txt".format(i+1),posAA))
    clash(newAA,posAA,str(i+1),-0.4,0,"contact")
    contacts_of_rota.append(contacts("contact{}.txt".format(i+1),posAA))
rc("close session")
f.write("Nombre de clash des rotamers : "+str(clashes_of_rota)+"\n")
f.write("Acide amines en contact avec les rotames : "+str(contacts_of_rota)+"\n")

# create the list of all AA in contact with at least 1 intersting rotamers
fused_contacts_of_rota = []
for i in range(len(contacts_of_rota)):
    l1 = fused_contacts_of_rota
    l2 = contacts_of_rota[i]
    fused_contacts_of_rota = list(set(l1)|set(l2))
f.write("Liste fusionne des contacts : "+str(fused_contacts_of_rota)+"\n")


# if minimize, minimize the structure for each rotamer having clash, and get the new number of clashes
if minimize : 
    clashes_of_rota_after = []
    for i in range(nb_of_interest_rot):
        if clashes_of_rota[i]:
            chimera.openModels.open(pdb_file)
            mini(newAA,posAA,NUM_MINIM_STEP,str(i+1))
            rc("close session")
            clashes_of_rota_after.append(clashes("clash_post{}.txt".format(i+1),posAA))
        else:
            clashes_of_rota_after.append(0)
    f.write("Nombre de clash des rotamers apres minimisation : "+str(clashes_of_rota_after))



rc("stop")
f.close()















