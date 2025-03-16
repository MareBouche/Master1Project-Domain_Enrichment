import pandas as pd
import openpyxl

all_data = pd.read_excel("logvalue1.xlsx")
filtered_data_ER = {}
filtered_data_Mitochondria = {}
filtered_data_Chloroplast = {}

for index, row in all_data.iterrows():
    if row[3] == 'ER':
        if row[0] not in filtered_data_ER:
            filtered_data_ER[row[0]] = [0, 0]
        if row[4] == 'Free TurboID':
            filtered_data_ER[row[0]][0] += 1
        elif row[4] == 'WT':
            filtered_data_ER[row[0]][1] += 1
    elif row[3] == 'Mitochondria':
        if row[0] not in filtered_data_Mitochondria:
            filtered_data_Mitochondria[row[0]] = [0, 0]
        if row[4] == 'Free TurboID':
            filtered_data_Mitochondria[row[0]][0] += 1  
        elif row[4] == 'WT':
            filtered_data_Mitochondria[row[0]][1]+= 1  
    elif row[3] == 'Chloroplast':
        if row[0] not in filtered_data_Chloroplast:
            filtered_data_Chloroplast[row[0]] = [0, 0]
        if row[4] == 'Free TurboID':
            filtered_data_Chloroplast[row[0]][0] += 1
        elif row[4] == 'WT':
            filtered_data_Chloroplast[row[0]][1] += 1

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "ER"
ws.append(['Protein ID', '#Baits_Free', '#Baits_WT'])

for protein in filtered_data_Chloroplast:
    ws.append([protein, filtered_data_Chloroplast[protein][0], filtered_data_Chloroplast[protein][1]])


wb.save("Organized_cp.xlsx")