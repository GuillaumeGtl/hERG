import os
import subprocess
from Matrice import *
import math



##### Variables #####
config = {}
## path to chimera executable
config["path_chimera"] = "C:/Program Files/Chimera 1.16/bin/chimera.exe"

## path to the pdb file
config["pdb_file"] = "C:/Users/Guillaume/Desktop/Nouveau dossier/hERG/hERG.pdb"

## mutation to be studied path (xlsx file)
config["mutation_file"] = "C:/Users/Guillaume/Desktop/Nouveau dossier/hERG/mutation.xlsx"

## scoring matrices path (xlsx file)
config["matrix_file"] = "C:/Users/Guillaume/Desktop/Nouveau dossier/hERG/matrices.xlsx"

## chimer.py pth
config["Chimer_file"] = "C:/Users/Guillaume/Desktop/Nouveau dossier/hERG/Chimer.py"

## output folder
config["output_folder"] = "C:/Users/Guillaume/Desktop/Nouveau dossier/hERG/output"

## AA index file path
config["res_index"] = "C:/Users/Guillaume/Desktop/Nouveau dossier/hERG/res_index.txt"

## important AA list of hERG
AA_important = [1, 15, 19, 20, 26, 28, 29, 30, 31, 32, 33, 41, 42, 43, 44, 45, 47, 49,
51, 53, 54, 55, 56, 58, 59, 64, 65, 66, 68, 69, 70, 71, 72, 74, 78, 79,
80, 82, 85, 86, 87, 92, 96, 98, 99, 100, 101, 102, 106, 108, 111, 114,
124, 306, 342, 400, 402, 410, 412, 413, 420, 421, 422, 427, 428, 429,
430, 463, 470, 472, 473, 474, 475, 483, 488, 490, 492, 493, 501, 528,
531, 534, 535, 537, 546, 551, 552, 553, 554, 555, 558, 559, 561, 562,
563, 564, 565, 566, 568, 570, 571, 572, 575, 582, 584, 585, 588, 591,
593, 594, 595, 596, 597, 601, 604, 605, 609, 610, 611, 613, 614, 615,
616, 617, 618, 620, 621, 622, 623, 625, 626, 627, 628, 629, 630, 631,
632, 633, 634, 635, 637, 638, 640, 641, 642, 644, 645, 649, 651, 657,
658, 660, 662, 696, 721, 732, 752, 783, 784, 788, 805, 806, 818, 822,
823, 828, 833, 835, 837, 845, 846, 996]

## probabilty threshold for rotamers selection
config["ROTA_PROB_THRESHOLD"] = 0.1

## number of rotamers to consider at least
config["MIN_NUM_ROTA"] = 3

## minimization steps number (if minimization is True, by far highest time consuming)
config["NUM_MINIM_STEP"] = 20


## traduction dictionnary
d = {'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K',
     'Ile': 'I', 'Pro': 'P', 'Thr': 'T', 'Phe': 'F', 'Asn': 'N', 
     'Gly': 'G', 'His': 'H', 'Leu': 'L', 'Arg': 'R', 'Trp': 'W', 
     'Ala': 'A', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y', 'Met': 'M',
     'C': 'Cys', 'D': 'Asp', 'S': 'Ser', 'Q': 'Gln', 'K': 'Lys',
     'I': 'Ile', 'P': 'Pro', 'T': 'Thr', 'F': 'Phe', 'N': 'Asn', 
     'G': 'Gly', 'H': 'His', 'L': 'Leu', 'R': 'Arg', 'W': 'Trp', 
     'A': 'Ala', 'V': 'Val', 'E': 'Glu', 'Y': 'Tyr', 'M': 'Met'}

## Chimera launch command
cmd = r'"%s" "%s"'%(config["path_chimera"],config["Chimer_file"])


def crit4(file):
    """
    compute the score of mutagenesis based on rotamer clash before and after minimization
    """
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
        if L[0] == 'Number of clashes of rotamers':
            
            clash = L[1].strip()
            clash = clash.strip('][').split(", ")
        if L[0] == 'Number of clashes of rotamers after minimisation':
            clash_post = L[1].strip()
            clash_post = clash_post.strip('][').split(", ")
    protot = 0
    for i in range(len(clash)):
        protot += float(proba_rota[i])
    score = 0
    for i in range(len(clash)):
        score += (int(float(clash[i])>0) + int(float(clash_post[i])>0))*float(proba_rota[i])
    score = score/protot if protot else 0
    return score/2
        
def get_clash(file):
    """
    get the number of rotamer clash before and after minimization
    """
    file = open(file,"r")
    content = file.readlines()
    file.close()
    clash = []
    clash_post = []
    for ligne in content:
        L = ligne.split(" : ")
        if L[0] == 'Number of clashes of rotamers':
            clash = L[1].strip()
            clash = clash.strip('][').split(", ")
        if L[0] == 'Number of clashes of rotamers after minimisation':
            clash_post = L[1].strip()
            clash_post = clash_post.strip('][').split(", ")
    return clash,clash_post

def get_contactAA(file):
    """
    get the list of AA in contact with at least one rotamer
    """
    file = open(file,"r")
    content = file.readlines()
    file.close()
    AA = []
    for ligne in content:
        L = ligne.split(" : ")
        if L[0] == 'Merged list of contacts':
            AA = L[1].strip()
            if AA == "[]":
                return []
            AA = AA.strip("][").split(", ")
            AA = [d[res_index_dict[str(j)].title()]+str(j) for j in [i.strip("'") for i in AA]]
    return AA

def get_contactAA_proba(file):
    """
    get the list of AA in contact with at least one rotamer with their contact probability
    """
    file = open(file,"r")
    content = file.readlines()
    file.close()
    for ligne in content:
        L = ligne.split(" : ")
        if L[0] == 'Amino acids in contact with rotamers':
            AA_r = eval(L[1])
        elif L[0] == 'proba rota':
            proba = eval(L[1])
        elif L[0] == 'Merged list of contacts':
            contacts = {}
            for AA in eval(L[1]):
                contacts[d[res_index_dict[AA].title()]+AA] = 0
    for num_rota in range(len(AA_r)):
        for AA in AA_r[num_rota]:
            contacts[d[res_index_dict[AA].title()]+AA] += proba[num_rota]
    return contacts
            
def initialise_res_index(pdb_file):
    f = open(pdb_file,'r')
    lignes = f.readlines()
    f.close()
    result = {}
    for l in lignes :
        if l[0:6].strip() == "ATOM" and l[22:26].strip() not in result:
            result[l[22:26].strip()] = l[17:20].strip()
    f = open(config["res_index"],'w')
    f.write(str(result))
    f.close()

def get_res_index(res_index):
    f = open(res_index,'r')
    file = f.readline()
    f.close()
    return eval(file)

def get_rota_info(file):
    f = open(file,"r")
    content = f.readlines()
    f.close()
    proba,AA_contact = "",""
    for ligne in content:
        L = ligne.split(" : ")
        if L[0] == "proba rota":
            proba = eval(L[1])
        elif L[0] == "Amino acids in contact with rotamers":
            AA_contact = eval(L[1])
    return proba,AA_contact
"""
subprocess.run(cmd)
"""
## suppression des espaces au debut et à la fin des mutations
clean_xlsx(config["mutation_file"])

## si le fichier de correspondance entre les indices des AA et les AA correspondant n'est pas créé, on le créé
if not os.path.isfile(config["res_index"]):
    initialise_res_index(config["pdb_file"])

## récupération du fichier de correspondance entre les indices des AA et les AA
res_index_dict = get_res_index(config["res_index"])

## récupérattion des mutations et résulats correspondants de l'excel
pre_aa,pos,post_aa,c1,c2,c3,clash,mini,c4,total,AA_con,nb_AA_con,AA_imp,nb_AA_imp,pr1,ncr1,ncir1,pr2,ncr2,ncir2,pr3,ncr3,ncir3,pr4,ncr4,ncir4,pr5,ncr5,ncir5,c5,final_score,sps = read_xlsx(config["mutation_file"])

## récupération des matrices de score 
M = matrices(config["matrix_file"])

## boucle dans les mutations
for i in range(len(pre_aa)):

    # définition de la mutation
    config["preAA"] = d[pre_aa[i]]
    config["newAA"] = d[post_aa[i]]
    config["posAA"] = pos[i]
    mutation = pre_aa[i]+pos[i]+post_aa[i]
    print(mutation)

    # initialisation du log
    log = open(config["output_folder"]+"/"+mutation+".txt","w")
    log.write("Mutation : "+pre_aa[i]+pos[i]+post_aa[i]+"\n")

    # si le critère 1 est vide, on le complete 
    if type(c1[i])==float and math.isnan(c1[i]):
        c1[i] = M[0][config["preAA"]][config["newAA"]]
        write_xlsx(config["mutation_file"],mutation,"criteriaA",c1[i])
    log.write("Size score : "+str(c1[i])+"\n")

    # idem critère 2
    if type(c2[i])==float and math.isnan(c2[i]):
        c2[i] = M[1][config["preAA"]][config["newAA"]]
        write_xlsx(config["mutation_file"],mutation,"criteriaB",c2[i])
    log.write("Hydrophobicity score : "+str(c2[i])+"\n")

    # idem critère 3
    if type(c3[i])==float and math.isnan(c3[i]):
        c3[i] = M[2][config["preAA"]][config["newAA"]]
        write_xlsx(config["mutation_file"],mutation,"criteriaC",c3[i])
    log.write("Charge score : "+str(c3[i])+"\n")

    
    ## Si le résidu n'existe pas dans la structure, on ne fait rien d'autre
    if pos[i] not in res_index_dict:
        if type(total[i])==float and math.isnan(total[i]):
            total[i] = c1[i]+c2[i]+c3[i]
            write_xlsx(config["mutation_file"],mutation,"total",total[i])
        log.write("Total score:"+str(total[i])+"\n")
        if type(final_score[i])==float and math.isnan(final_score[i]):
            final_score[i] = total[i]
            write_xlsx(config["mutation_file"],mutation,"final score",final_score[i])
        log.write("Final score:"+str(final_score[i])+"\n")
        log.close()
    else :
        log.close()
        # si on a pas d'informations sur les clash, on les calcule
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
            clash[i] = str(clash[i])
        # réouverture du log
        log = open(config["output_folder"]+"/"+mutation+".txt","a")

        # idem critère 4
        if type(c4[i])==float and math.isnan(c4[i]):
            c4[i] = crit4(config["output_folder"]+"/"+mutation+".txt")
            write_xlsx(config["mutation_file"],mutation,"criteriaD",c4[i])
        log.write("Mutagenesis score :"+str(c4[i])+"\n")

        # idem score total
        if type(total[i])==float and math.isnan(total[i]):
            total[i] = c1[i]+c2[i]+c3[i]+c4[i]
            write_xlsx(config["mutation_file"],mutation,"total",total[i])
        log.write("Total score:"+str(total[i])+"\n")

        if type(AA_con[i])==float and math.isnan(AA_con[i]):
            AA_con[i] = get_contactAA_proba(config["output_folder"]+"/"+mutation+".txt")
            write_xlsx(config["mutation_file"],mutation,"contact AA",AA_con[i])
            AA_con[i] = str(AA_con[i])
        log.write("List of AA in contact with at least one of the rotamers: "+AA_con[i]+"\n")
        
        # idem nombre d'AA en contact avec la mutation 
        if type(nb_AA_con[i]) == float and math.isnan(nb_AA_con[i]):
            nb_AA_con[i] = len(eval(AA_con[i]))
            write_xlsx(config["mutation_file"],mutation,"number of contact AA",nb_AA_con[i])
        log.write("Number of AA in contact with at least one of the rotamers: "+str(nb_AA_con[i])+"\n")


        if type(AA_imp[i])==float and math.isnan(AA_imp[i]):
            AA_imp[i] = {}
            for AA,proba in eval(AA_con[i]).items():
                if int(AA[1:]) in AA_important:
                    AA_imp[i][AA]=proba
            write_xlsx(config["mutation_file"],mutation,"important contact AA",AA_imp[i])
            AA_imp[i] = str(AA_imp[i])
        log.write("List of important AA in contact with at least one of the rotamers : "+AA_imp[i]+"\n")
        
        # idem nombre d'AA important en contact avec la mutation 
        if type(nb_AA_imp[i]) == float and math.isnan(nb_AA_imp[i]):
            nb_AA_imp[i] = len(eval(AA_imp[i]))
            write_xlsx(config["mutation_file"],mutation,"number of important contact AA",nb_AA_imp[i])
        log.write("Number of important AA in contact with at least one of the rotamers : "+str(nb_AA_imp[i])+"\n")
        
        if clash[i] == 'no rotamers':
            nb_of_rotamers = 0
        else : 
            nb_of_rotamers = len(eval(clash[i]))
        flags = [0]*5
        for j in range(nb_of_rotamers):
            flags[j] = 1
        
        if flags[0]:
            proba,AA_contact = get_rota_info(config["output_folder"]+"/"+mutation+".txt")
            if type(pr1[i]) == float and math.isnan(pr1[i]):
                pr1[i] = proba[0]
                write_xlsx(config["mutation_file"],mutation,"rota1 proba",pr1[i])
            if type(ncr1[i]) == float and math.isnan(ncr1[i]):
                ncr1[i] = len(AA_contact[0])
                write_xlsx(config["mutation_file"],mutation,"number of rota1 contact",ncr1[i])
            if type(ncir1[i]) == float and math.isnan(ncir1[i]):
                c = 0
                for AA in AA_contact[0]:
                    if int(AA) in AA_important:
                        c+=1
                ncir1[i] = c
                write_xlsx(config["mutation_file"],mutation,"number of important rota1 contact",ncir1[i])
        if flags[1]:
            if type(pr2[i]) == float and math.isnan(pr2[i]):
                pr2[i] = proba[1]
                write_xlsx(config["mutation_file"],mutation,"rota2 proba",pr2[i])
            if type(ncr2[i]) == float and math.isnan(ncr2[i]):
                ncr2[i] = len(AA_contact[1])
                write_xlsx(config["mutation_file"],mutation,"number of rota2 contact",ncr2[i])
            if type(ncir2[i]) == float and math.isnan(ncir2[i]):
                c = 0
                for AA in AA_contact[1]:
                    if int(AA) in AA_important:
                        c+=1
                ncir2[i] = c
                write_xlsx(config["mutation_file"],mutation,"number of important rota2 contact",ncir2[i])
        if flags[2]:
            if type(pr3[i]) == float and math.isnan(pr3[i]):
                pr3[i] = proba[2]
                write_xlsx(config["mutation_file"],mutation,"rota3 proba",pr3[i])
            if type(ncr3[i]) == float and math.isnan(ncr3[i]):
                ncr3[i] = len(AA_contact[2])
                write_xlsx(config["mutation_file"],mutation,"number of rota3 contact",ncr3[i])
            if type(ncir3[i]) == float and math.isnan(ncir3[i]):
                c = 0
                for AA in AA_contact[2]:
                    if int(AA) in AA_important:
                        c+=1
                ncir3[i] = c
                write_xlsx(config["mutation_file"],mutation,"number of important rota3 contact",ncir3[i])
        if flags[3]:
            if type(pr4[i]) == float and math.isnan(pr4[i]):
                pr4[i] = proba[3]
                write_xlsx(config["mutation_file"],mutation,"rota4 proba",pr4[i])
            if type(ncr4[i]) == float and math.isnan(ncr4[i]):
                ncr4[i] = len(AA_contact[3])
                write_xlsx(config["mutation_file"],mutation,"number of rota4 contact",ncr4[i])
            if type(ncir4[i]) == float and math.isnan(ncir4[i]):
                c = 0
                for AA in AA_contact[3]:
                    if int(AA) in AA_important:
                        c+=1
                ncir4[i] = c
                write_xlsx(config["mutation_file"],mutation,"number of important rota4 contact",ncir4[i])
        if flags[4]:
            if type(pr5[i]) == float and math.isnan(pr5[i]):
                pr5[i] = proba[4]
                write_xlsx(config["mutation_file"],mutation,"rota5 proba",pr5[i])
            if type(ncr5[i]) == float and math.isnan(ncr5[i]):
                ncr5[i] = len(AA_contact[4])
                write_xlsx(config["mutation_file"],mutation,"number of rota5 contact",ncr5[i])
            if type(ncir5[i]) == float and math.isnan(ncir5[i]):
                c = 0
                for AA in AA_contact[4]:
                    if int(AA) in AA_important:
                        c+=1
                ncir5[i] = c
                write_xlsx(config["mutation_file"],mutation,"number of important rota5 contact",ncir5[i])   
        if type(c5[i]) == float and math.isnan(c5[i]):
            c5[i] = 0
            if flags[0]:
                c5[i] += (int(ncir1[i])/max(1,int(ncr1[i])))*float(pr1[i])
            if flags[1]:
                c5[i] += (int(ncir2[i])/max(1,int(ncr2[i])))*float(pr2[i])
            if flags[2]:
                c5[i] += (int(ncir3[i])/max(1,int(ncr3[i])))*float(pr3[i])
            if flags[3]:
                c5[i] += (int(ncir4[i])/max(1,int(ncr4[i])))*float(pr4[i])
            if flags[4]:
                c5[i] += (int(ncir5[i])/max(1,int(ncr5[i])))*float(pr5[i])
            c5[i] = c5[i]
            write_xlsx(config["mutation_file"],mutation,"criteriaE",c5[i])
        if type(final_score[i])==float and math.isnan(final_score[i]):
            final_score[i] = total[i] + c4[i] +c5[i]
            write_xlsx(config["mutation_file"],mutation,"final score",final_score[i])
        log.write("Final score:"+str(final_score[i])+"\n")
        log.close()
    if type(sps[i])==float and math.isnan(sps[i]):
        sps[i] = 1 + round(final_score[i] / 3.29882895 * 4 * 4, 0) / 4
        write_xlsx(config["mutation_file"],mutation,"Structural Pathogenicity Score",sps[i])