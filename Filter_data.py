import pandas as pd

# Lees de CSV-bestand in
all_data = pd.read_csv("DE_results(All.vs.All).csv", delimiter=";")

# Selecteer de kolommen die 'Free_TurboID', 'WT_culture', 'dark vs dark' of 'light vs light' bevatten
WT_and_FreeTurbo = [column for column in all_data.columns if 'Free_TurboID' in column or 'WT_culture' in column]
columns_to_keep = list(all_data.columns[:2]) + WT_and_FreeTurbo 

# Filter de data om alleen de geselecteerde kolommen te behouden
filtered_data = all_data[columns_to_keep]

# Transformeer de kolommen die beginnen met 'Free_TurboID' of 'WT_culture'
transform = [column for column in all_data.columns if column.startswith('Free_TurboID') or column.startswith('WT_culture')]
filtered_data.loc[:, transform] *= -1

# Schrijf de gefilterde data naar een Excel-bestand
filtered_data.to_excel('filtered_data1.xlsx', index=False)