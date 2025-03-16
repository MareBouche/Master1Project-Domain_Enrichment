import pandas as pd
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Logvalue>1"
ws.append(['Protein ID', 'TurboID', 'Log Value', 'Organelle', 'Type'])
organelles = {'Cyt': 'ER', 'CNX': 'ER', 'VAP': 'ER', 'TRB': 'Mitochondria', 'TOM': 'Mitochondria', 'HXK': 'Mitochondria', 'SP1': 'Chloroplast', 'OEP': 'Chloroplast'}
all_data = pd.read_excel("filtered_data1.xlsx")

for index, row in all_data.iterrows():
    for col_name, value in row.items():
             if isinstance(value, float) and value > 1:
                for bait in organelles:
                    if bait in col_name:
                         organelle = organelles[bait]
                         if 'Free_TurboID' in col_name:
                               Type = 'Free TurboID'
                         elif 'WT_culture' in col_name:
                               Type = 'WT'
                         if col_name.count('Dark') == 2:
                                ws.append([row['Protein ID'], col_name, value, organelle, Type])
                         elif col_name.count('LIGHT') == 2:
                                ws.append([row['Protein ID'], col_name, value, organelle, Type])
                              

wb.save("logvalue1.xlsx")