import os
import tkinter 
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import fichier as fi
import subprocess

#Variable global
env=os.getcwd()

#Definition des chemins


pathchi="C:/Program Files/Chimera 1.16/bin/chimera.exe"
PDBFILE = "C:/Users/Guillaume/Desktop/hERG/hERG_test.pdb"



#Etude du score 1
#Dictionnaire traduisant le critère 1
table1={"Ala":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":1,"Glu":1,"Gly":0,"His":1,"Ile":1,"Leu":0,"Lys":1,"Met":1,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":2,"Tyr":1,"Val":0},
        "Arg":{"Ala":1,"Arg":0,"Asn":1,"Asp":1,"Cys":1,"Gln":0,"Glu":0,"Gly":2,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":0,"Val":1},
        "Asn":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":0},
        "Asp":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":0},
        "Cys":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":0},
        "Gln":{"Ala":1,"Arg":0,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":2,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":0,"Val":0},
        "Glu":{"Ala":1,"Arg":0,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":0,"Val":0},
        "Gly":{"Ala":0,"Arg":2,"Asn":1,"Asp":1,"Cys":1,"Gln":2,"Glu":1,"Gly":0,"His":2,"Ile":1,"Leu":1,"Lys":2,"Met":2,"Phe":2,"Pro":1,"Ser":1,"Thr":1,"Trp":2,"Tyr":2,"Val":1},
        "His":{"Ala":1,"Arg":0,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":2,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":1,"Thr":0,"Trp":0,"Tyr":0,"Val":0},
        "Ile":{"Ala":1,"Arg":0,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":0,"Val":0},
        "Leu":{"Ala":0,"Arg":0,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":0,"Val":0},
        "Lys":{"Ala":1,"Arg":0,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":2,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":1,"Thr":0,"Trp":0,"Tyr":0,"Val":0},
        "Met":{"Ala":1,"Arg":0,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":2,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":1,"Thr":0,"Trp":0,"Tyr":0,"Val":0},
        "Phe":{"Ala":1,"Arg":0,"Asn":0,"Asp":0,"Cys":1,"Gln":0,"Glu":0,"Gly":2,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":1,"Thr":1,"Trp":0,"Tyr":0,"Val":0},
        "Pro":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":0},
        "Ser":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":1,"Ile":0,"Leu":0,"Lys":1,"Met":1,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":0},
        "Thr":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":0},
        "Trp":{"Ala":2,"Arg":0,"Asn":1,"Asp":1,"Cys":1,"Gln":1,"Glu":1,"Gly":2,"His":0,"Ile":1,"Leu":1,"Lys":0,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":0,"Val":1},
        "Tyr":{"Ala":1,"Arg":0,"Asn":1,"Asp":1,"Cys":1,"Gln":0,"Glu":0,"Gly":2,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":0,"Val":0},
        "Val":{"Ala":0,"Arg":1,"Asn":0,"Asp":0,"Cys":0,"Gln":0,"Glu":0,"Gly":1,"His":0,"Ile":0,"Leu":0,"Lys":0,"Met":0,"Phe":0,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":0,"Val":0}} 


#Dictionnaire traduisant le critère 2
table2 = {"Ala":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":2,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":1,"Val":0},
         "Arg":{"Ala":2,"Arg":0,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":2,"His":1,"Ile":2,"Leu":2,"Lys":0,"Met":2,"Phe":2,"Pro":1,"Ser":1,"Thr":1,"Trp":2,"Tyr":2,"Val":2},
         "Asn":{"Ala":1,"Arg":1,"Asn":0,"Asp":1,"Cys":0,"Gln":0,"Glu":1,"Gly":1,"His":1,"Ile":1,"Leu":1,"Lys":1,"Met":1,"Phe":1,"Pro":1,"Ser":1,"Thr":1,"Trp":1,"Tyr":1,"Val":1},
         "Asp":{"Ala":2,"Arg":2,"Asn":1,"Asp":0,"Cys":1,"Gln":1,"Glu":0,"Gly":2,"His":1,"Ile":2,"Leu":2,"Lys":2,"Met":2,"Phe":2,"Pro":1,"Ser":1,"Thr":1,"Trp":2,"Tyr":2,"Val":2},
         "Cys":{"Ala":1,"Arg":1,"Asn":0,"Asp":1,"Cys":0,"Gln":0,"Glu":1,"Gly":1,"His":1,"Ile":1,"Leu":1,"Lys":1,"Met":1,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":1},
         "Gln":{"Ala":1,"Arg":1,"Asn":0,"Asp":1,"Cys":0,"Gln":0,"Glu":1,"Gly":1,"His":1,"Ile":1,"Leu":1,"Lys":1,"Met":1,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":1},
         "Glu":{"Ala":2,"Arg":2,"Asn":1,"Asp":0,"Cys":1,"Gln":1,"Glu":0,"Gly":2,"His":1,"Ile":2,"Leu":2,"Lys":2,"Met":2,"Phe":2,"Pro":1,"Ser":1,"Thr":1,"Trp":2,"Tyr":2,"Val":2},
         "Gly":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":2,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":1,"Val":0},
         "His":{"Ala":2,"Arg":1,"Asn":1,"Asp":1,"Cys":1,"Gln":1,"Glu":1,"Gly":2,"His":0,"Ile":2,"Leu":2,"Lys":1,"Met":2,"Phe":1,"Pro":1,"Ser":1,"Thr":1,"Trp":1,"Tyr":1,"Val":2},
         "Ile":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":2,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":1,"Val":0},
         "Leu":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":2,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":1,"Val":0},
         "Lys":{"Ala":2,"Arg":0,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":2,"His":1,"Ile":2,"Leu":2,"Lys":0,"Met":2,"Phe":2,"Pro":1,"Ser":1,"Thr":1,"Trp":2,"Tyr":2,"Val":2},
         "Met":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":2,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":1,"Val":0},
         "Phe":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":1,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":1,"Val":0},
         "Pro":{"Ala":1,"Arg":1,"Asn":0,"Asp":1,"Cys":0,"Gln":0,"Glu":1,"Gly":1,"His":1,"Ile":1,"Leu":1,"Lys":1,"Met":1,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":1},
         "Ser":{"Ala":1,"Arg":1,"Asn":0,"Asp":1,"Cys":0,"Gln":0,"Glu":1,"Gly":1,"His":1,"Ile":1,"Leu":1,"Lys":1,"Met":1,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":1},
         "Thr":{"Ala":1,"Arg":1,"Asn":0,"Asp":1,"Cys":0,"Gln":0,"Glu":1,"Gly":1,"His":1,"Ile":1,"Leu":1,"Lys":1,"Met":1,"Phe":1,"Pro":0,"Ser":0,"Thr":0,"Trp":1,"Tyr":1,"Val":1},
         "Trp":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":1,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":0,"Tyr":0,"Val":0},
         "Tyr":{"Ala":1,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":1,"His":1,"Ile":1,"Leu":1,"Lys":2,"Met":1,"Phe":1,"Pro":1,"Ser":1,"Thr":1,"Trp":1,"Tyr":0,"Val":1},
         "Val":{"Ala":0,"Arg":2,"Asn":1,"Asp":2,"Cys":1,"Gln":1,"Glu":2,"Gly":0,"His":2,"Ile":0,"Leu":0,"Lys":2,"Met":0,"Phe":0,"Pro":1,"Ser":1,"Thr":1,"Trp":1,"Tyr":0,"Val":0}}

def stop():
    global running
    running = False

def accueil(titre):
    root = tkinter.Tk ()  
    root.title('Acceuil')
    label=tkinter.Label(root,text = titre)
    label.pack() 
    root.geometry('600x450')    
    myFont = tkFont.Font(family="Arial", size=15, weight="bold")
    label.configure(font=myFont,bg="red")
    mon_image = tkinter.PhotoImage(file = "C:/Users/Guillaume/Desktop/hERG/Code/hERG.pgm")				
	#Les pixels de l'image se trouvent alors stockés dans la variable mon_image.
    #détermination des dimensions de l'image :
    largeur = mon_image.width()  # dimensions en nombre de pixels
    hauteur = mon_image.height()				
	#création d'un widget ( canevas, étiquette ) dans lequel l'image sera affichée :
    zone_image =Canvas(root, width = largeur, height = hauteur) # crée un canevas de dimensions ajustées à celles de l'image
    zone_image.create_image(0,0,image = mon_image, anchor = tkinter.NW) # association image/widget
    zone_image.pack() # placement du widget	
    tkinter.Button(root,text="Lancez l'application", command=root.destroy, bg="lightgreen",font=("Courrier",10),fg="black").pack()  
    root.protocol("WM_DELETE_WINDOW", lambda: [stop(), root.destroy()])
    root.mainloop() 
    
def erreur(titre1):
    root = tkinter.Tk ()  
    root.title('Erreur')
    root.geometry('400x100') 
    # configure the grid
    titre=tkinter.Label(root,text="Erreur")
    myFont = tkFont.Font(family="Arial", size=15, weight="bold")
    titre.configure(font=myFont,bg="red")
    titre.grid(column=0,row=1)
    label=tkinter.Label(root,text=titre1)
    label.grid(column=0, row=2)

    
    
def paramètre():
    root = tkinter.Tk ()  
    root.title('Initialisation')
    root.geometry('600x200') 
    # configure the grid
    titre=tkinter.Label(root,text=" Choix de paramètres")
    myFont = tkFont.Font(family="Arial", size=15, weight="bold")
    titre.configure(font=myFont,bg="red")
    titre.grid(column=0,row=1)
    label=tkinter.Label(root,text="Chemin menant à chimera.exe:")
    label.grid(column=0, row=2)
    chi=tkinter.StringVar()
    tkinter.Entry(root,textvariable=chi).grid(column=1, row=2)
    tkinter.Label(root,text="Chemin menant au fichier PDB hERG:").grid(column=0, row=3)
    pdb=tkinter.StringVar()
    tkinter.Entry(root,textvariable=pdb).grid(column=1, row=3)
    ordi = tkinter.IntVar()
    tkinter.Label(root,text="Votre ordinateur est un:").grid(column=0, row=4)
    tkinter.Radiobutton(root, text="Mac/Linux",variable=ordi,value=1).grid(column=1, row=4)
    tkinter.Radiobutton(root, text="Windows",variable=ordi,value=0).grid(column=2, row=4)
    tkinter.Button(root,text="Ok", command=root.destroy).grid(column=1,row=5)  
    root.mainloop() 
    return (ordi.get(),pdb.get(),chi.get())

    
def recuperation_mutation():
    def on_mouse_wheel(event):
        menu = option_menu["menu"]
        menu.yview_scroll(int(-1 * (event.delta / 120)), "units")
    root = tkinter.Tk ()
    root.title('Choix Mutation de hERG')
    root.geometry('500x150') 
    # configure the grid
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=2)
    titre=tkinter.Label(root,text=" Mutation de hERG")
    myFont = tkFont.Font(family="Arial", size=15, weight="bold")
    titre.configure(font=myFont,bg="red")
    titre.grid(column=0,row=1)
    tkinter.Label(root,text="L'acide aminé:").grid(column=0, row=3)
    seq = sequence()
    aa=["Choix"]+seq
    aam=tkinter.StringVar()
    option_menu = ttk.OptionMenu(root, aam, *aa)
    option_menu.grid(column=2, row=3)
    aam.set(seq[0])
    root.bind("<MouseWheel>", on_mouse_wheel)
    tkinter.Label(root,text="Est transformé en:").grid(column=0, row=4)
    aam2=tkinter.StringVar()
    aa=["Choix","Ala","Arg","Asn","Asp","Cys","Gln","Glu","Gly","His","Ile","Leu","Lys","Met","Phe","Pro","Ser","Thr","Trp","Tyr","Val"]
    ttk.OptionMenu(root,aam2,*aa).grid(column=2, row=4)
    aam2.set("Ala")
    tkinter.Button(root,text="Ok", command=root.destroy).grid(column=1,row=5)  
    root.mainloop() 
    return (aam.get()[3:],aam.get()[:3],aam2.get())

def recuperation_mutation():
    root = tkinter.Tk ()  
    root.title('Choix Mutation de hERG')
    root.geometry('500x150') 
    # configure the grid
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=2)
    titre=tkinter.Label(root,text=" Mutation de hERG")
    myFont = tkFont.Font(family="Arial", size=15, weight="bold")
    titre.configure(font=myFont,bg="red")
    titre.grid(column=0,row=1)
    label=tkinter.Label(root,text="Position de l'a.a muté:")
    #label.pack() 
    label.grid(column=0, row=2)
    pos=tkinter.IntVar()
    tkinter.Entry(root,textvariable=pos).grid(column=2, row=2)
    tkinter.Label(root,text="L'acide aminé:").grid(column=0, row=3)
    aa=["Choix","Ala","Arg","Asn","Asp","Cys","Gln","Glu","Gly","His","Ile","Leu","Lys","Met","Phe","Pro","Ser","Thr","Trp","Tyr","Val"]
    aam=tkinter.StringVar()
    ttk.OptionMenu(root, aam, *aa).grid(column=2, row=3)
    aam.set("Ala")
    tkinter.Label(root,text="Est transformé en:").grid(column=0, row=4)
    aam2=tkinter.StringVar()
    ttk.OptionMenu(root,aam2,*aa).grid(column=2, row=4)
    aam2.set("Ala")
    tkinter.Button(root,text="Ok", command=root.destroy).grid(column=1,row=5)  
    root.mainloop() 
    return (pos.get(),aam.get(),aam2.get())


  
def affichagescore12(cri1,cri2,dcri1,dcri2):
    root = tkinter.Tk()
    root.title('Choix Mutation de hERG')
    root.geometry('500x150') 
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    label2=tkinter.Label(root,text="Evaluation Score 1 & 2  ")
    label2.grid(column=0,row=1)
    myFont = tkFont.Font(family="Arial", size=15, weight="bold")
    label2.configure(font=myFont,bg="red")
    #label3=tkinter.Label(text="Evaluation du changement de l'espace occupé \n Evaluation du changement de l'hydrophobicité, des charges et de la polarités")
    #label3.grid(column=0,row=1)  
    tkinter.Label(root,text="Valeur du critère 1: ").grid(column=0,row=2)
    tkinter.Label(root,text=str(cri1)).grid(column=1,row=2)
    tkinter.Label(root,text="Signification:").grid(column=0,row=3) 
    tkinter.Label(root,text=dcri1[cri1]).grid(column=1,row=3) 
    tkinter.Label(root,text="Valeur du critère 2: ").grid(column=0,row=4)
    tkinter.Label(root,text=str(cri2)).grid(column=1,row=4)
    tkinter.Label(root,text="Signification:").grid(column=0,row=5) 
    tkinter.Label(root,text=dcri2[cri2]).grid(column=1,row=5) 
    root.mainloop()
    
def score(mut,scoret,fichier,verdict):
    root = tkinter.Tk ()  
    root.title('Score')
    root.geometry('400x200') 
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    myFont = tkFont.Font(family="Arial", size=15, weight="bold")
    label2=tkinter.Label(root,text="Score Final")
    label2.configure(font=myFont,bg="red")
    label2.grid(column=0, row=1)
    tkinter.Label(root,text="Mutation:").grid(column=0, row=2)
    tkinter.Label(root,text=mut).grid(column=1, row=2)
    tkinter.Label(root,text="Score Final:").grid(column=0, row=3)
    tkinter.Label(root,text=scoret).grid(column=1, row=3)
    tkinter.Label(root,text="Verdict:").grid(column=0, row=4)
    tkinter.Label(root,text=verdict).grid(column=1, row=4)
    tkinter.Label(root,text="\n \nPour plus d'information \nregarder le fichier %s"%(fichier)).grid(column=0, row=5)
    #tkinter.Button(root,text="Refaire une mutation", command=root.destroy).grid(column=0,row=6)  
    tkinter.Button(root,text="OK", command=root.destroy).grid(column=1,row=6)
    root.mainloop() 
     
def sequence():
    f = open(PDBFILE,"r")
    seq = []
    line = f.readline()
    while line:
        line = line.split()
        if line[0] == "ATOM":
            if line[3]+line[5] not in seq:
                seq.append(line[3]+line[5])
        line = f.readline()
    f.close()
    return seq    

def display_err(err):
    messagebox.showwarning("Erreur",err)
    

### Logiciel 

ordi=0
running = True
while running:
    #Affichage de l'accueil 
    accueil("Bienvenue sur le pipeline calculant la pathogénicité d'une \n mutation de hERG")
    if not running:
        break

    #Récupération de la mutation
    pos1,aam1,aam2=recuperation_mutation()
    print(pos1,aam1,aam2)
    seq = sequence()
    if aam1.upper()+str(pos1) not in seq:
        display_err("l'acide aminé en position {} n'est pas {}".format(str(pos1),aam1))
        break
    #Critère 1
    dcri1={0 :"pas de changement", 1:"peu de changement", 2:"beaucoup de changements"}
    cri1=table1[aam1][aam2]

    #Critère 2
    cri2=table2[aam1][aam2]
    dcri2={0:"charge/polaritée/hydrophilie identiques", 1:"disparition/apparition de charge/polaritée", 2:"charge/polaritée/hydrophile opposée"}
    affichagescore12(cri1,cri2,dcri1,dcri2)
    mut="{}\t|\t{}\t|\t{}\n".format(pos1,aam1,aam2)
    #mut1=str(pos1)+" "+str(aam1)+" "+str(aam2)

    #Calcul du score tot
    scoretot=cri1+cri2

    #Ecriture des scores
    if os.path.exists(str(pos1)+aam2+'_result.txt'):
        os.remove(str(pos1)+aam2+"_result.txt")  

    if os.path.exists('result.txt'):
        os.remove("result.txt")  

    fi.ecriture(str(pos1)+aam2+"_result.txt",["Pipeline Results\n \n","Mutation\n","Position|\tOld aa\t|\tNew aa\t \n",mut,"\n\n"])
    fi.ecriture("result.txt",[mut+"\n",str(scoretot)])


    mutation=aam1+" en "+aam2+" "+str(pos1)
    fichier=str(pos1)+aam2+"_result.txt"

    if scoretot >=4:
        score(mutation,scoretot,fichier,"Fort Impact")


    cmd = r'"%s" "%s"'%(pathchi,"C:/Users/Guillaume/Desktop/hERG/Code/Essai.py")
    subprocess.run(cmd)

    result=fi.lecture("result.txt")
    scoretot=float(result[len(result)-1][0])

    if scoretot>=4:
        score(mutation,scoretot,fichier,"Fort Impact")
    else:
        score(mutation,scoretot,fichier,"Faible Impact")
    
