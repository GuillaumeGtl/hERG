Avant la 1ere utilisation:

Il faut installer quelques modules python, pour ça ouvrir un 
utilisateur de commande et rentrer les commandes suivantes:

pip install tkinter
pip install os
pip install subprocess


Il faut spécifier différents chemins d'accès :
Dans selection.py

ligne 15	pathchi="chemin d'accès à chimera.exe"
Sur Windows:
ligne 200	ordi=0
ligne 245	cmd = r'"%s" open "%s"'%(pathchi,"chemin d'accès au fichier Essai.py")
Sur Mac:
ligne 200	ordi=1
ligne 243	os.system("%s open %s"%(pathchi,"chemin d'accès au fichier Essai.py")

Dans Essai.py

ligne 33	opened=chimera.openModels.open("chemin d'accès au fichier pdb à utiliser",type="PDB")




Utilisation:

Lancer le script selection.py
Cliquer sur "Lancer l'application"
Rentrer la position de l'AA à muter, son type, et en quoi il va être muté
Cliquer sur "OK"

Une fênetre d'évaluation des scores 1 et 2 apparait
Fermez la fenêtre pour continuer

Si besoin est, Chimera se lancera automatiquement et ouvrira, en plus de son interface classique,
une fenêtre de selection du type de fichier. Cette fenêtre de selection peut être ignorée et 
doit simplement être fermé pour que le script poursuive. Ce processus peut prendre plusieur minutes
puis une fois que Chimera se ferme automatiquement, une fenêtre de résultats s'ouvre et les informations
sont stoquées dans un fichier texte qui porte un nom du type NumAATypeAA_result.tkt qui a été généré 
dans le même dossier que le script.

