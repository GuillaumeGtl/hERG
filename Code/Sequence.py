#ligne 6
from tkinter import messagebox

# ligne 16
PDBFILE = "C:/Users/Guillaume/Desktop/hERG/hERG_test.pdb"


# ligne 200
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

"""
#ligne 215
seq = sequence()
if aam1.upper()+str(pos1) not in seq:
    break
"""


----

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

