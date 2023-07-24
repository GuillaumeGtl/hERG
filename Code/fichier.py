#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 21:48:22 2023

@author: audreypiraud
"""

#Fonction concernant la lecture / écriture de fichier

def lecture(nomFichier):
    fichier=open(nomFichier,"r")  #On ouvre le fichier donné en argument et on l'atribut à la variable fichier
    data=[]
    ligne=fichier.readline()
    while len(ligne)!=0: 
        ligne=ligne.replace("|", "")
        ligne1=ligne.split()
        data.append(ligne1)
        ligne=fichier.readline()
    fichier.close() 
    return(data)

def ecriture(nomFichier,ecrit):
    f=open(nomFichier,"a")  #On ouvre le fichier donné en argument et on l'atribut à la variable fichier
    for j in ecrit:
        f.write(j)    
    f.close() 
