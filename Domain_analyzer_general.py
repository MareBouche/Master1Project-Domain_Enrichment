import csv
import openpyxl

def read_gene_accessions(mcs_file):
    '''
    Get all gene accessions from a file downloaded at MCSdb
    by Wander 
    ~ edited by Mare; can be edited based on the species, here mouse is used~
    '''
    gene_accessions = []
    
    with open(mcs_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        for row in reader:
            parts = row[1].split(";")
            gene_accessions.append(parts[0])
    print(gene_accessions)
    return gene_accessions

def proteome_domain_counter(all_domains_file):
    """
    Counts all domains specific species and remembers in how many proteins a certain domain is found (not counting alternative spliced froms) and per domain what genes have the domain.
    by Wander.
    ~ edited by Mare; can be edited based on the species ~
    """
    count_dict = {}
    gene_dict = {}
    with open(all_domains_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            interpro_id  = line[0]
            gene_name = line[-1]
            if gene_name in gene_dict:
                gene_dict[gene_name].append(interpro_id)
            else:
                gene_dict[gene_name] = [interpro_id]
            if interpro_id in count_dict:
                count_dict[interpro_id] += 1
            else:
                count_dict[interpro_id] = 1
    return count_dict, gene_dict

def count_MCS_domains(gene_accessions, gene_dict):
    """
    Count the domains in the MCS proteins by Mare. Can be edited based on the species.
    """
    mcs_count_dict = {}
    for accession in gene_accessions:
        if accession in gene_dict:
            for domain in gene_dict[str(accession)]:
                if domain in mcs_count_dict:
                    mcs_count_dict[domain] += 1
                else:
                    mcs_count_dict[domain] = 1
        else: 
             print(f"Warning: {accession} not found in gene_dict")
    return mcs_count_dict

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

def domains_to_csv(types_dict, id_to_name_dict, MCS_count_dict, proteome_count_dict, parents_dict, saved_exel):
    """
    function that writes the data to a csv so it can be used in exel in a more visual way
    by Wander and Mare
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Domain_counts_MCS"
    ws.append(['Domain ID', 'Subdomain ID', 'Subdomain Name', 'Type', 'Count_Genome', 'MCS_Count'])

    for interpro_id, type in types_dict.items():
        subdomain_name = id_to_name_dict[interpro_id]
        if interpro_id in MCS_count_dict:
            MCS_count = MCS_count_dict[interpro_id]
        else:
            MCS_count = None
        if interpro_id in proteome_count_dict:
            count_genome = proteome_count_dict[interpro_id]
        else:
            count_genome = None
        if interpro_id in parents_dict:
            parent_id = parents_dict[interpro_id]
        else:
            parent_id = None
        
        ws.append([parent_id, interpro_id, subdomain_name, type, count_genome, MCS_count])
    wb.save(saved_exel)
    print("Wrote to exel")


if __name__ == "__main__":
    gene_accession = read_gene_accessions("Mouse_mcs_file.txt")
    count_dict, gene_dict = proteome_domain_counter("MGI_InterProDomains.csv")
    MCS_count_dict = count_MCS_domains(gene_accession, gene_dict)
    types_dict, id_to_name_dict = domain_type("entry.list.txt")
    parents_dict = parent_id("ParentChildTreeFile.txt")
    domains_to_csv(types_dict, id_to_name_dict, MCS_count_dict, count_dict, parents_dict, "Domain_counts_MCS.xlsx")