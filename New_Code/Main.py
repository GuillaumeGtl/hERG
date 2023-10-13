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

## le chemin d'accès au dossier de sortie des mutations
config["output_folder"] = "C:/Users/Guillaume/Desktop/hERG/New_Code/output"

## le chemin d'accès au fichier de la liste des AA importants
AA_important = [16, 20, 26, 28, 29, 30, 31, 32, 33, 41, 42, 43, 44, 45, 47, 49, 53, 53, 54, 55, 56, 58, 58, 58, 64, 64, 66, 68, 71, 72, 74, 74, 74, 78, 86, 86, 94, 96, 98, 99, 100, 101, 106, 108, 114, 124, 148, 176, 215, 306, 312, 320, 328, 400, 402, 410, 413, 420, 421, 422, 426, 427, 427, 427, 431, 451, 456, 460, 463, 466, 470, 473, 474, 475, 490, 492, 493, 493, 501, 501, 525, 528, 531, 531, 534, 534, 552, 558, 558, 559, 561, 561, 561, 562, 562, 564, 565, 566, 568, 568, 569, 571, 571, 572, 572, 572, 572, 572, 575, 582, 582, 584, 585, 593, 593, 593, 597, 601, 604, 605, 609, 611, 613, 614, 615, 615, 616, 621, 621, 622, 623, 625, 626, 626, 626, 626, 627, 628, 628, 629, 629, 629, 629, 629, 630, 630, 632, 633, 634, 635, 635, 637, 637, 637, 638, 638, 640, 640, 641, 644, 644, 645, 645, 645, 648, 649, 656, 657, 657, 660, 662, 687, 693, 696, 696, 706, 706, 711, 721, 728, 744, 749, 752, 752, 757, 767, 770, 774, 784, 785, 788, 788, 791, 800, 805, 805, 806, 818, 818, 820, 822, 823, 835, 837, 861, 861, 885, 894, 1049, 1066, 1157]

## le pourcentage au dessus duquel on considère le rotamère intéressant
config["ROTA_PROB_THRESHOLD"] = 0.1

## le nombre de rotamère que l'on considère si aucun n'atteind la probabilité qui nous intéresse
config["MIN_NUM_ROTA"] = 3

## le nombre de pas de minimisation
config["NUM_MINIM_STEP"] = 0



d = {'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K',
     'Ile': 'I', 'Pro': 'P', 'Thr': 'T', 'Phe': 'F', 'Asn': 'N', 
     'Gly': 'G', 'His': 'H', 'Leu': 'L', 'Arg': 'R', 'Trp': 'W', 
     'Ala': 'A', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y', 'Met': 'M',
     'C': 'Cys', 'D': 'Asp', 'S': 'Ser', 'Q': 'Gln', 'K': 'Lys',
     'I': 'Ile', 'P': 'Pro', 'T': 'Thr', 'F': 'Phe', 'N': 'Asn', 
     'G': 'Gly', 'H': 'His', 'L': 'Leu', 'R': 'Arg', 'W': 'Trp', 
     'A': 'Ala', 'V': 'Val', 'E': 'Glu', 'Y': 'Tyr', 'M': 'Met'}

cmd = r'"%s" "%s"'%(config["path_chimera"],config["Chimer_file"])

# stockages des variables dans un fichier de configuration
"""
f = open("config.txt","w")
f.write(str(config))
f.close()
"""

def crit4(file):
    file = open(file,"r")
    content = file.readlines()
    file.close()
    proba_rota = []
    clash = []
    clash_post = []
    for ligne in content:
        L = ligne.split(" : ")
        if L[0] == 'proba rota':
            proba_rota = L[1].strip()
            if proba_rota == "[]":
                return 0
            proba_rota = proba_rota.strip('][').split(", ")
        if L[0] == 'Nombre de clash des rotamers':
            
            clash = L[1].strip()
            clash = clash.strip('][').split(", ")
        if L[0] == 'Nombre de clash des rotamers apres minimisation':
            clash_post = L[1].strip()
            clash_post = clash_post.strip('][').split(", ")
    protot = 0
    for i in range(len(clash)):
        protot += float(proba_rota[i])
    score = 0
    for i in range(len(clash)):
        score += (int(float(clash[i])>0) + int(float(clash_post[i])>0))*float(proba_rota[i])
    score = score/protot
    return score
        
def get_clash(file):
    file = open(file,"r")
    content = file.readlines()
    file.close()
    clash = []
    clash_post = []
    for ligne in content:
        L = ligne.split(" : ")
        if L[0] == 'Nombre de clash des rotamers':
            clash = L[1].strip()
            clash = clash.strip('][').split(", ")
        if L[0] == 'Nombre de clash des rotamers apres minimisation':
            clash_post = L[1].strip()
            clash_post = clash_post.strip('][').split(", ")
    return clash,clash_post

def get_contactAA(file):
    file = open(file,"r")
    content = file.readlines()
    file.close()
    AA = []
    for ligne in content:
        L = ligne.split(" : ")
        if L[0] == 'Liste fusionne des contacts':
            AA = L[1].strip()
            if AA == "[]":
                return AA
            AA = AA.strip("][").split(", ")
            AA = [int(j) for j in [i.strip("'") for i in AA]]
    return AA
"""
subprocess.run(cmd)
"""

pre_aa,pos,post_aa,c1,c2,c3,clash,mini,c4,total,AA_imp =  read_xlsx(config["mutation_file"])
M = matrices(config["matrix_file"])
for i in range(len(pre_aa)):
    config["preAA"] = d[pre_aa[i]]
    config["newAA"] = d[post_aa[i]]
    config["posAA"] = pos[i]
    mutation = pre_aa[i]+pos[i]+post_aa[i]
    print(mutation)
    log = open(config["output_folder"]+"/"+mutation+".txt","w")
    log.write("Mutation : "+pre_aa[i]+pos[i]+post_aa[i]+"\n")
    if type(c1[i])==float and math.isnan(c1[i]):
        c1[i] = M[0][config["preAA"]][config["newAA"]]
        write_xlsx(config["mutation_file"],mutation,"critère1",c1[i])
    log.write("Score taille : "+str(c1[i])+"\n")
    if type(c2[i])==float and math.isnan(c2[i]):
        c2[i] = M[1][config["preAA"]][config["newAA"]]
        write_xlsx(config["mutation_file"],mutation,"critère2",c2[i])
    log.write("Score hydrophobicite : "+str(c2[i])+"\n")
    if type(c3[i])==float and math.isnan(c3[i]):
        c3[i] = M[2][config["preAA"]][config["newAA"]]
        write_xlsx(config["mutation_file"],mutation,"critère3",c3[i])
    log.write("Score charge : "+str(c3[i])+"\n")
    log.close()
    if type(clash[i])==float and math.isnan(clash[i]):
        config["minimize"] = math.isnan(mini[i])
        f = open("config.txt","w")
        f.write(str(config))
        f.close()
        subprocess.run(cmd)
        clash[i],mini[i] = get_clash(config["output_folder"]+"/"+mutation+".txt")
        if clash[i] == [""]:
            clash[i] = "no rotamers"
        else :
            clash[i] = [int(j) for j in clash[i]]
        if mini[i] == [""]:
            mini[i] = "no rotamers"
        else :
            mini[i] = [int(j) for j in mini[i]]
        write_xlsx(config["mutation_file"],mutation,"clash",clash[i])
        write_xlsx(config["mutation_file"],mutation,"minimisation",mini[i])
    log = open(config["output_folder"]+"/"+mutation+".txt","a")
    if type(c4[i])==float and math.isnan(c4[i]):
        c4[i] = crit4(config["output_folder"]+"/"+mutation+".txt")
        write_xlsx(config["mutation_file"],mutation,"critère4",c4[i])
    log.write("Score mutagenese :"+str(c4[i])+"\n")
    if type(total[i])==float and math.isnan(total[i]):
        total[i] = c1[i]+c2[i]+c3[i]+c4[i]
        write_xlsx(config["mutation_file"],mutation,"total",total[i])
    log.write("Score total :"+str(total[i])+"\n")
    if type(AA_imp[i])==float and math.isnan(AA_imp[i]):
        AA_imp[i] = [aa for aa in get_contactAA(config["output_folder"]+"/"+mutation+".txt") if aa in AA_important]
        write_xlsx(config["mutation_file"],mutation,"AA_important en contact",AA_imp[i])
    log.write("Liste des AA importants en contact avec au moins un rotamere : "+str(AA_imp[i])+"\n")
    log.close()




    
