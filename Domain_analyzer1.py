import requests
import time
import csv
import pickle
import openpyxl
import re


def read_plant_gene_accessions(mcs_file):
    '''
    Get all TAIR gene accessions from a file downloaded at MCSdb
    by Wander
    '''
    tair_accessions = []
    
    with open(mcs_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        pattern = re.compile("At\dg\d{5}")
        for row in reader:
            m = re.search(pattern, row[1])
            if m:
                tair_accessions.append(m.group(0).upper())
    print(tair_accessions, len(tair_accessions))
    return tair_accessions


def read_yeast_gene_accessions(mcs_file):
    '''
    Get all yeast gene IDs accessions from a file downloaded at MCSdb
    by Wander
    '''
    yeast_id_accessions = []
    
    with open(mcs_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        pattern = re.compile("\w{3}\d{3}\w")
        for row in reader:
            m = re.search(pattern, row[1])
            if m:
                yeast_id_accessions.append(m.group(0))
    print(yeast_id_accessions, len(yeast_id_accessions))
    return yeast_id_accessions


def read_human_gene_accessions(mcs_file):
    '''
    Get all human gene IDs (HGNC symbol) accessions from a file downloaded at MCSdb
    by Wander
    '''
    human_id_accessions = []
    
    with open(mcs_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        for row in reader:
            synonyms = row[1]
            if ";" in synonyms:
                HGNC = synonyms.split(";")[0]
            else:
                HGNC = synonyms
            human_id_accessions.append(HGNC)
    print(human_id_accessions, len(human_id_accessions))
    return human_id_accessions
    
    
def pickle_save(filename, dict):
    """
    efficiently save the information as a dictionary so all the accesions dont have to get retrieved from the API
    by Wander
    """
    with open(filename, "wb") as f:
        pickle.dump(dict, f)

    print(f"Dictionary named {dict} Saved in  {filename}")


def pickle_retrieve(filename):
    """
    Short function to retrieve stored info from a pickled file
    by Wander
    """
    with open(filename, "rb") as f:
        dict = pickle.load(f)
    
    return dict


def get_interpro_data(accession_list):
    '''
    A now redundant function
    From a list of Uniprot_accessions, get domain information of each protein via interpro API.
    by Wander made with help of GTP4o
    '''
    domains = []

    for accession in accession_list:
        url = f"https://www.ebi.ac.uk/interpro/api/entry/interpro/protein/uniprot/{accession}/"
        response = requests.get(url, headers={"Accept": "application/json"})
        
        if response.status_code == 200:  # means that it found the protein
            data = response.json()
            domain_names = []

            if "results" in data:
                # data item is a very complicated dict, can go to a url of an accession to see how it is structured
                for hit in data["results"]:
                    metadata_dict = hit["metadata"]
                    domain_names.append([metadata_dict["accession"], metadata_dict["name"]])
            
            domains.append([accession, list(domain_names)])
        else:
            print(f"Failed to retrieve data for {accession}, status code: {response.status_code}")

        # Sleep to avoid rate limits
        # time.sleep(1)

    return domains


def count_interpro_domains(domains:list):
    '''
    A now redundant function

    Works with the interpro list made in get_interpro_data() and counts the amount of time a IPR domain is found in the protein list.
    Returns a IPR: count dictionairy and a dictonairy with Uniprot_id: set(IPRs)
    by Wander
    '''
    count_dict = {}
    protein_dict = {}
    for accession in domains:
        accession_id, entries = accession
        for domain in entries:
            interpro_id = domain[0]
            if accession_id not in protein_dict.get(interpro_id, set()):  # make sure the gene is not counted already if duplicate domains are present (or splice vars)
                count_dict[interpro_id] = count_dict.get(interpro_id, 0) + 1
                protein_dict[interpro_id] = protein_dict.get(interpro_id, set()) | {accession_id}

    return count_dict, protein_dict

def count_plant_MCS(accession_list, TAIR_all_domains_file):
    """Get MCS counts from an all domains file of TAIR, using an tair_id accession list
    by Wander
    """
    count_dict = {}
    gene_dict = {}
    with open(TAIR_all_domains_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id = line[-2]
            gene_name = line[0][:9]
            if gene_name in accession_list and interpro_id != "Null":
                if gene_name not in gene_dict.get(interpro_id, set()):  # make sure the gene is not counted already if duplicate domains are present (or splice vars)
                    count_dict[interpro_id] = count_dict.get(interpro_id, 0) + 1
                    gene_dict[interpro_id] = gene_dict.get(interpro_id, set()) | {gene_name}
    return count_dict, gene_dict

def count_yeast_MCS(accession_list, yeast_all_domains_file):
    """Get MCS counts from an all domains file of yeast
    by Wander
    """
    count_dict = {}
    gene_dict = {}
    with open(yeast_all_domains_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id  = line[-4]
            gene_name = line[0]
            if gene_name in accession_list and interpro_id != '-':
                if gene_name not in gene_dict.get(interpro_id, set()):  # make sure the gene is not counted already if duplicate domains are present (or splice vars)
                    count_dict[interpro_id] = count_dict.get(interpro_id, 0) + 1
                    gene_dict[interpro_id] = gene_dict.get(interpro_id, set()) | {gene_name}
    return count_dict, gene_dict


def count_human_MCS(accession_list, human_all_domains_file):
    """
    Get MCS counts from an all domains file of yeast using HGNC id accesion list
    by Wander
    """
    count_dict = {}
    HGNC_dict = {}
    with open(human_all_domains_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id  = line[1]
            gene_name = line[0]
            if gene_name in accession_list and interpro_id != '' and gene_name != '':
                if gene_name not in HGNC_dict.get(interpro_id, set()):  # make sure the gene is not counted already if duplicate domains are present (or splice vars)
                    count_dict[interpro_id] = count_dict.get(interpro_id, 0) + 1
                    HGNC_dict[interpro_id] = HGNC_dict.get(interpro_id, set()) | {gene_name}
    return count_dict, HGNC_dict


def TAIR_domain_counter(all_domains_file):
    """
    Counts all domains from TAIR domain document and remembers in how many proteins a certain domain is found (not counting alternative spliced froms) and per domain what genes have the domain.
    by Wander.
    """
    count_dict = {}
    gene_dict = {}
    with open(all_domains_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id  = line[-2]
            gene_name = line[0][:9]  # gene name only, not the splice variant
            if interpro_id != 'Null':
                if gene_name not in gene_dict.get(interpro_id, set()):  # make sure the gene is not counted already if duplicate domains are present (or splice vars)
                    count_dict[interpro_id] = count_dict.get(interpro_id, 0) + 1
                    gene_dict[interpro_id] = gene_dict.get(interpro_id, set()) | {gene_name}
        return count_dict, gene_dict


def SGD_domain_counter(all_domains_file):
    """
    Counts all domains from SGD domain document and remembers in how many proteins a certain domain is found (not counting alternative spliced froms) and per domain what genes have the domain.
    by Wander
    """
    count_dict = {}
    gene_dict = {}
    with open(all_domains_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id  = line[-4]
            gene_name = line[0]
            if interpro_id != '-':
                if gene_name not in gene_dict.get(interpro_id, set()):  # make sure the gene is not counted already if duplicate domains are present (or splice vars)
                    count_dict[interpro_id] = count_dict.get(interpro_id, 0) + 1
                    gene_dict[interpro_id] = gene_dict.get(interpro_id, set()) | {gene_name}

        return count_dict, gene_dict


def human_domain_counter(all_domains_file):
    """
    Counts all domains from TAIR domain document and remembers in how many proteins a certain domain is found (not counting alternative spliced froms) and per domain what genes have the domain.
    by Wander.
    """
    count_dict = {}
    HGNC_dict = {}
    with open(all_domains_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id  = line[1]
            gene_name = line[0]
            if interpro_id != '' and gene_name != '':
                if gene_name not in HGNC_dict.get(interpro_id, set()):  # make sure the gene is not counted already if duplicate domains are present (or splice vars)
                    count_dict[interpro_id] = count_dict.get(interpro_id, 0) + 1
                    HGNC_dict[interpro_id] = HGNC_dict.get(interpro_id, set()) | {gene_name}

        return count_dict, HGNC_dict


def domain_type(entry_file):
    """
    takes the domain types from the entry file and adds them to the types dict 
    by Mare
    """
    types_dict = {}
    id_to_name = {}
    with open(entry_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id  = line[0]
            domain_type = line[1]
            description = line[2]
            types_dict[interpro_id] = domain_type
            id_to_name[interpro_id] = description
    return types_dict, id_to_name


def parent_id(parent_file):
    """
    Takes the id of the "parent" domain based on the ParentChildTree.txt file and links it to the subdomains 
    by Mare
    """
    parents_dict = {}
    domains = []
    with open(parent_file, 'r') as file:
        data = file.read()
    reader = data.strip().split('\n')
    for line in reader:
        id = line.split('::')[0]
        domains.append(id)
    for domain in domains:
        if domain.startswith('IPR'):
            parent = domain
        else:
            subdomain = domain.lstrip('--')
            parents_dict[subdomain] = parent
    return parents_dict


def domains_to_csv(types_dict, id_to_name_dict, TAIR_counts, interpro_counts_plant, yeast_count_dict, interpro_counts_yeast, human_count_dict, interpro_counts_human, parents_dict, saved_exel):
    """
    function that writes the data to a csv so it can be used in exel in a more visual way
    by Wander and Mare
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Domain_counts_MCS_Ath"
    ws.append(['Domain ID', 'Subdomain ID', 'Subdomain Name', 'Type', 'Count_Ath_Genome', "Count_MCS_Ath", "Count_Yeast_Genome", "Count_MCS_yeast", "Count_Human_genome", "Count_MCS_human"])

    for interpro_id, type in types_dict.items():
        subdomain_name = id_to_name_dict[interpro_id]
        # plants
        if interpro_id in interpro_counts_plant:
            MCS_count_ath = interpro_counts_plant[interpro_id]
        else:
            MCS_count_ath = None
        if interpro_id in TAIR_counts:
            count_Ath_genome = TAIR_counts[interpro_id]
        else:
            count_Ath_genome = None
        # yeast
        if interpro_id in interpro_counts_yeast:
            MCS_count_yeast = interpro_counts_yeast[interpro_id]
        else:
            MCS_count_yeast = None
        if interpro_id in yeast_count_dict:
            count_yeast_genome = yeast_count_dict[interpro_id]
        else:
            count_yeast_genome = None
        # human
        if interpro_id in interpro_counts_human:
            MCS_count_human = interpro_counts_human[interpro_id]
        else:
            MCS_count_human = None
        if interpro_id in human_count_dict:
            count_human_genome = human_count_dict[interpro_id]
        else:
            count_human_genome = None

        if interpro_id in parents_dict:
            parent_id = parents_dict[interpro_id]
        else:
            parent_id = None
        
        ws.append([parent_id, interpro_id, subdomain_name, type, count_Ath_genome, MCS_count_ath, count_yeast_genome, MCS_count_yeast, count_human_genome, MCS_count_human])

    wb.save(saved_exel)
    print("Wrote to exel")


if __name__ == "__main__":

    plant_MCS_counts, plant_MCS_protein_dict = count_plant_MCS(read_plant_gene_accessions("Arabidopsis thaliana_mcs_file.txt"), "all.domains.txt")
    yeast_MCS_counts, yeast_MCS_protein_dict = count_yeast_MCS(read_yeast_gene_accessions("Yeast_mcs_file.txt"), "yeast_domains.tab")
    human_MCS_counts, human_MCS_protein_dict = count_human_MCS(read_human_gene_accessions("Human_mcs_file.txt"), "human_domains.txt")

    plant_genome_count, plant_gene_dict = TAIR_domain_counter("all.domains.txt")
    yeast_genome_counts, yeast_gene_dict = SGD_domain_counter("yeast_domains.tab")
    human_genome_counts, human_gene_dict = human_domain_counter("human_domains.txt")

    types, id_to_name = domain_type("entry.list.txt")
    parents_dict = parent_id("ParentChildTreeFile.txt")

    domains_to_csv(types, id_to_name, plant_genome_count, plant_MCS_counts, yeast_genome_counts, yeast_MCS_counts, human_genome_counts, human_MCS_counts, parents_dict, "HAY_domain_counts.xlsx")
