Chimera_version : 1.16

Python_version : 3.12

-To run the code, you have to edit main.py to input your correct path for chimera and the different files of this repo.

-For new variant analysis, you have to input your mutation in the mutation.xlsx file with the format 1LetterResidue1Letter in the first row of each columns starting from B1.

-The 29 lines of results correspond to the following :

mutation: what mutation is being studied at the 1 letter format
criteriaA: a score of importance for the change of size of the mutation (see matrix)
criteriaB: a score of importance for the change of hydrophobicity of the mutation (see matrix)
criteriaC: a score of importance for the change of charge of the mutation (see matrix)
clash: a list of the number of clashes found for each rotamer we consider of interest
minimisation: a list of the number of clashes remaining after a few steps of structural simulation to try to resolve the clashes
criteriaD: a score of clashes that is 0 when no clashes are found, 0.5 when minimised and 1 when not minimised. weighted by the probability of the rotamer
total: sum of criteriaA,B and C
contactAA: list of residues considered in contact with the mutated amino acid
number of contact AA: number of residues considered in contact with the mutated amino acid
important contact AA: list of residues known for being important for the protein considered in contact with any of the considered rotamers
number of important contact AA: number of residues known for being important for the protein considered in contact with any of the considered rotamers
rotaX proba: probability of the Xth rotamer
number of rotaX contact: number of residues considered in contact with the Xth rotamer
number of important rotaX contact: number of residues known for being important for the protein considered in contact with the Xth rotamer
criteriaE: number of important rotaX contact/number of rotaX contact * rotaX proba  
final score : sum of criteria A to E
Structural Pathogenicity Score: simplified score of pathogenicity of the mutation ranging from 1 (not pathogenic) to 5(very pathogenic)
