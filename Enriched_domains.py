import csv

def domains_TurboID(potential_MCS_file, TAIR_all_domains_file):
    domain_dict = {}
    with open(TAIR_all_domains_file) as f:
        with open(potential_MCS_file) as f2:
            accession_list = [line.strip() for line in f2]
            reader = csv.reader(f, delimiter="\t")  # assuming the file is tab-delimited    
            for line in reader:
                interpro_id = line[-2]
                gene_name = line[0][:11]
                if gene_name in accession_list and interpro_id != "Null":
                    if gene_name not in domain_dict:
                        domain_dict[gene_name] = [interpro_id]
                    elif interpro_id not in domain_dict[gene_name]:
                        domain_dict[gene_name].append(interpro_id)
    return domain_dict

def enriched_domains(domain_dict, enriched_domains_file, found_domains_file):
    enriched = {}
    enriched_domains = []
    with open(enriched_domains_file, 'r') as file:
        for line in file:
            enriched_domains.append(line.rstrip())
    for protein in domain_dict:
        for domain in domain_dict[protein]:
            if domain in enriched_domains:
                if protein not in enriched:
                    enriched[protein] = [domain]
                else:
                    enriched[protein].append(domain)
    with open(found_domains_file, 'w') as file:
        for protein in enriched:
            file.write(protein + '\t' + '\t'.join(enriched[protein]) + '\n')

domain_dict = domains_TurboID("Proteins_Chloroplast.txt", "all.domains.txt")
enriched_domains(domain_dict, "Enriched_Domains.txt", "Found_Domains_cp.txt")