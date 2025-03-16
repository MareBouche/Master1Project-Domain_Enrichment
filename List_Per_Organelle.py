import pandas as pd

data = pd.read_excel("logvalue1.xlsx")
ER = []
Mitochondria = []
Chloroplast = []
EM = []
EC = []
MC = []

for index, row in data.iterrows():
    if row['Organelle'] == 'ER':
        if row['Protein ID'] not in ER:
            ER.append(row['Protein ID'])
    elif row['Organelle'] == 'Mitochondria':
        if row['Protein ID'] not in Mitochondria:
            Mitochondria.append(row['Protein ID'])
    else:
        if row['Protein ID'] not in Chloroplast:
            Chloroplast.append(row['Protein ID'])

for protein in ER:
    if protein in Mitochondria:
        EM.append(protein)
    elif protein in Chloroplast:
        EC.append(protein)

for protein in Mitochondria:
    if protein in Chloroplast:
        MC.append(protein)

with open('Proteins_ER.txt', 'w') as file:
    for protein in ER:
        file.write(protein + '\n')

with open('Proteins_Mitochondria.txt', 'w') as file:
    for protein in Mitochondria:
        file.write(protein + '\n')

with open('Proteins_Chloroplast.txt', 'w') as file:
    for protein in Chloroplast:
        file.write(protein + '\n')

with open('Proteins_ER_Mitochondria.txt', 'w') as file:
    for protein in EM:
        file.write(protein + '\n')

with open('Proteins_ER_Chloroplast.txt', 'w') as file:
    for protein in EC:
        file.write(protein + '\n')

with open('Proteins_Mitochondria_Chloroplast.txt', 'w') as file:
    for protein in MC:
        file.write(protein + '\n')