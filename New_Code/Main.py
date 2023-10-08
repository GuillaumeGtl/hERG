import os
import subprocess
import Matrice



##### Variables #####
config = {}
## le chemin d'accès au programme chimera
config["path_chimera"] = "C:/Program Files/Chimera 1.16/bin/chimera.exe"

## le code 3 lettre de l'acide aminé après mutation
config["newAA"] = "GLN"

## la position de la mutation
config["posAA"] = "673"

## le chemin d'accès au fichier pdb
config["pdb_file"] = "C:/Users/Guillaume/Desktop/hERG/New_Code/hERG.pdb"

## le pourcentage au dessus duquel on considère le rotamère intéressant
config["ROTA_PROB_THRESHOLD"] = 0.1

## le nombre de rotamère que l'on considère si aucun n'atteind la probabilité qui nous intéresse
config["MIN_NUM_ROTA"] = 3

## le nombre de pas de minimisation
config["NUM_MINIM_STEP"] = 10

## est-ce qu'on fait la minimisation
config["minimize"] = False



# stockages des variables dans un fichier de configuration

f = open("config.txt","w")
f.write(str(config))
f.close()



#
cmd = r'"%s" "%s"'%(config["path_chimera"],"C:/Users/Guillaume/Desktop/hERG/New_Code/Chimer.py")
subprocess.run(cmd)

print ("ok")



