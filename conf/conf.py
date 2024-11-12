import os
#### Input and Output files config parameters ####
csv_folder = './csv/examples/'
output_docs_folder='./output_docs/'

#### VCF Conversion config parameters ####
allele_counts=True
reference_genome='GRCh37' # Choose one between NCBI36, GRCh37, GRCh38
datasetId='COVID_pop12_ita_1'
case_level_data=False
num_rows=7000000

### MongoDB parameters ###
database_host = 'mongo'
database_port = 27017
database_user = 'root'
database_password = os.getenv("DB_PASSWD","example")
database_name = 'beacon'
database_auth_source = 'admin'
