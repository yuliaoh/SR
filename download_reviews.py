import os
from Bio import Entrez


#Entrez requires personal API key if you make more than 3 requests per second
Entrez.email = 'yotmakhova@student.unimelb.edu.au'
Entrez.api_key = "540f16191cb1909f0ff299a325b1b135c208"

target_folder = "/Users/yotmakhova/Research/Test/Cochrane/"

# retrieving a list of PMCIDs from PubMed Central OA where the publication type = systematic review
# and publisher = Cochrane
search_term = "Cochrane Database Syst Rev[TA]&Systematic review[PT]"
handle = Entrez.esearch(db="pmc", term=search_term, idtype="pmcid")
record = Entrez.read(handle)

# by default only 20 ids are retrieved; to retrieve all you need to get and specify the count of available records
count = record['Count']
handle = Entrez.esearch(db="pmc", term=search_term, idtype="pmcid", retmax=count)
record = Entrez.read(handle)
handle.close()

pmcids = record['IdList']

# reconstruct the PMCID format from the numeric ids we retrieve
pmcids = ['PMC'+pmcid for pmcid in pmcids]

# fetch the full text articles and write them to files
for pmcid in pmcids:
    fetch = Entrez.efetch(db="pmc",
                          id=pmcid,
                          rettype="full",
                          retmode="xml")
    filename = pmcid + '.xml'
    with open(os.path.join(target_folder, filename), 'w') as f:
        f.write(fetch.read())
