import os
import subprocess
from Matrice import *
import math



##### Variables #####
config = {}
## le chemin d'accès au programme chimera
config["path_chimera"] = "C:/Program Files/Chimera 1.16/bin/chimera.exe"

## le chemin d'accès au fichier pdb
config["pdb_file"] = "C:/Users/Guillaume/Desktop/hERG/New_Code/hERG.pdb"

## le chemin d'accès au fichier des mutations à faire
config["mutation_file"] = "C:/Users/Guillaume/Desktop/hERG/New_Code/mutation.xlsx"

## le chemin d'accès au fichier des matrices de score
config["matrix_file"] = "C:/Users/Guillaume/Desktop/hERG/New_Code/matrices.xlsx"

## le chemin d'accès au fichier Chimer.py
config["Chimer_file"] = "C:/Users/Guillaume/Desktop/hERG/New_Code/Chimer.py"

## le pourcentage au dessus duquel on considère le rotamère intéressant
config["ROTA_PROB_THRESHOLD"] = 0.1

## le nombre de rotamère que l'on considère si aucun n'atteind la probabilité qui nous intéresse
config["MIN_NUM_ROTA"] = 3

## le nombre de pas de minimisation
config["NUM_MINIM_STEP"] = 10



d = {'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K',
     'Ile': 'I', 'Pro': 'P', 'Thr': 'T', 'Phe': 'F', 'Asn': 'N', 
     'Gly': 'G', 'His': 'H', 'Leu': 'L', 'Arg': 'R', 'Trp': 'W', 
     'Ala': 'A', 'Val':'V', 'Glu': 'E', 'Tyr': 'Y', 'Met': 'M',
     'C': 'Cys', 'D': 'Asp', 'S': 'Ser', 'Q': 'Gln', 'K': 'Lys',
     'I': 'Ile', 'P': 'Pro', 'T': 'Thr', 'F': 'Phe', 'N': 'Asn', 
     'G': 'Gly', 'H': 'His', 'L': 'Leu', 'R': 'Arg', 'W': 'Trp', 
     'A': 'Ala', 'V': 'Val', 'E': 'Glu', 'Y': 'Tyr', 'M': 'Met'}

cmd = r'"%s" "%s"'%(config["path_chimera"],config["Chimer_file"])

# stockages des variables dans un fichier de configuration
f = open("config.txt","w")
f.write(str(config))
f.close()


#


"""
subprocess.run(cmd)
"""

pre_aa,pos,post_aa,c1,c2,c3,clash,mini,c4,total,AA_imp =  read_xlsx(config["mutation_file"])
M = matrices(config["matrix_file"])
for i in range(len(pre_aa)):
    config["preAA"] = d[pre_aa[i]]
    config["newAA"] = d[post_aa[i]]
    config["posAA"] = pos[i]
    log = open(pre_aa[i]+pos[i]+post_aa[i]+".txt","w")
    log.write("Mutation : "+pre_aa[i]+pos[i]+post_aa[i]+"\n")
    if math.isnan(c1[i]):
        c1[i] = M[0][config["preAA"]][config["newAA"]]
    log.write("Score taille : "+str(c1[i])+"\n")
    if math.isnan(c2[i]):
        c2[i] = M[1][config["preAA"]][config["newAA"]]
    log.write("Score hydrophobicite : "+str(c2[i])+"\n")
    if math.isnan(c3[i]):
        c3[i] = M[2][config["preAA"]][config["newAA"]]
    log.write("Score charge : "+str(c3[i])+"\n")
    print (config["preAA"],config["newAA"],c1[i],c2[i],c3[i])
    if type(clash[0])==float and math.isnan(clash[0]):
        config["minimize"] = math.isnan(mini[i])
        f = open("config.txt","w")
        f.write(str(config))
        f.close()
        subprocess.run(cmd)
        






    
