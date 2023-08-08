import os
import subprocess
import Matrice

path_chimera = "C:/Program Files/Chimera 1.16/bin/chimera.exe"
pdb_file = "C:/Users/Guillaume/Desktop/hERG/hERG_test.pdb"

cmd = r'"%s" "%s"'%(path_chimera,"C:/Users/Guillaume/Desktop/hERG/New_Code/Chimer.py")
subprocess.run(cmd)


