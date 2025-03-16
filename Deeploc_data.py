import pandas as pd

def extract_protein_data(file_path):
    df = pd.read_csv(file_path, dtype=str)
    protein_data = []
    for index, row in df.iterrows():
        protein_id = row.iloc[0]
        location = row.iloc[1]
        protein_data.append((protein_id, location))
    return protein_data

file_path = "Deeploc_cp.csv"
protein_data = extract_protein_data(file_path)
protein_df = pd.DataFrame(protein_data, columns=['Protein ID', 'Location'])
protein_df.to_excel("Localisation_deeploc_cp.xlsx", index=False)
print("Data is written to excel file")