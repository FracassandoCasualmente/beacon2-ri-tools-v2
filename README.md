# Beacon 2 RI tools v2.0

This repository contains the new Beacon ri tools v2.0, a software created with the main goal of generating BFF data from .csv or .vcf (and probably more types of datafiles in the future). This is based on the first beacon ri tools, a previous and different version that you can find here: [Beacon ri tools v1](https://github.com/EGA-archive/beacon2-ri-tools). The new features for beacon v2.0 are:

* Code Language is written in [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* The output gain are schemas that suit the very last version of [Beacon v2](https://github.com/ga4gh-beacon/beacon-v2) specifications, and ready to be deployed in a beacon v2 API compliant.
* This version raises exceptions that serve as a guide for users to know how to fill data correctly into the datasheets, so the final datafiles are correct and compliant with specifications.
* All the possible combinations of docs that are compliant with specifications can be generated, like for example, writing a variation either in LegacyVariation, MolecularVariation or SystemicVariation.

## Data conversion process

The main goal of Beacon ri tools v2.0 is to obtain a BFF (json following Beacon v2 official specifications) file that can be injected to a beacon v2 mongoDB database. To obtain a beacon v2 with its mongodb and see how to inject this BFF files, you can check it out and download yours for free at the official repo of [Beacon v2 ri api](https://github.com/EGA-archive/beacon2-ri-api).
To get this json file, you can either convert your data from a .vcf file or from a .csv file. Please, see instruction manual to follow the right steps to do the data conversion. At the end, you will end completing one of the possible conversion processes that is shown in the next diagram:
![Beacon tools v2 diagram](https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/main/files/beacon-ri-tools-v2-figure-new.jpg)

## Installation guide with docker

First of all, clone or download the repository to your computer:
```bash
git clone https://github.com/EGA-archive/beacon2-ri-tools-v2.git
```

To light up the container with beacon ri tools v2, execute the next command inside the root folder:
```bash
docker-compose up -d --build
```

Once the container is up and running you can start using beacon ri tools v2, congratulations!

## Instruction manual

### Setting configuration and csv file

To start using beacon ri tools v2, you have to edit the configuration file [conf.py](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/conf/conf.py) that you will find inside [conf](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/conf). Inside this file you will find the next information:
```bash
#### Input and Output files config parameters ####
csv_folder = './csv/examples/'
output_docs_folder='./output_docs/'

#### VCF Conversion config parameters ####
allele_frequency=1 # introduce float number, leave 1 if you want to convert all the variants
reference_genome='GRCh38' # Choose one between NCBI36, GRCh37, GRCh38
datasetId='coadread_tcga_pan_can_atlas_2018'
```

Please, remember to make the datasetId match the id for your datasets.csv file.

#### Generic config parameters
The **csv_folder** variable sets where is the all .csv files the scripts will write and read data from. All the .csv file need to have the headers written as you can find in the files inside [templates](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/csv/templates). Note that any header that has a different name from the ones that appear inside the files of this folder will not be read by the beacon ri tools v2.
The **output_docs_folder** sets the folder where your final .json files will be saved once execution of beacon tools finishes. This folder is mandatory to be always inside 'output_docs', so only the subdirectory inside output_docs can be modified in this path.

#### VCF conversion config parameters
The **reference_genome** is the genome reference your the tool is using to map the position of the chromosomes.
The **allele_frequency** let's you set a threshold for the allele frequency of the variants you want to convert from the vcf file.

### Converting data from .vcf.gz file

To convert data from .vcf.gz to .json, you will need to copy all the files you want to convert inside the [files_to_read folder](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/files/vcf/files_to_read).
You will need to provide one .vcf.gz file file and save it in this folder.

```bash
docker exec -it ri-tools python genomicVariations_vcf.py
```
After that, if needed, export your documents from mongoDB to a .json file using two possible commands. 
The first one will delete "_id" entries generated by mongoDB:
```bash
docker exec ri-tools-mongo mongoexport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --collection genomicVariations | sed '/"_id":/s/"_id":[^,]*,//g' > genomicVariations.json
```
The second one will keep the "_id" entries generated by mongoDB:
```bash
docker exec ri-tools-mongo mongoexport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --collection genomicVariations > genomicVariations.json
```
This will generate the final .json file that is Beacon Friendly Format. Bear in mind that this time, the file will be saved in the directory you are located, so if you want to save it in the output_docs folder, add it in the path of the mongoexport.

### Creating the .csv file (if metadata or not having a vcf file for genomicVariations)

If you want to convert metadata into BFF or fill a genomicVariations csv to convert to json, you will have to create a .csv file writing the records according to the header columns, which indicate the field of the schema that this data will be placed in. Every new row will be appended to the final output file as a new and independent document. 
Fill in the csv file, following the next rules:
* If you want to write data that needs to be appended in the same document, please write data separated with |, for example if you need to write an id, e.g. HG00001|HG00002 then respect this order for their correlatives in the same document, as for the label of this id, e.g. labelforHG00001|labelforHG00002.
* As the info field for each collection is very generic and can be filled with different data, you will need to fill the column data directly with json type data. For copies and subjects for genomicVariations, json data is also needed.
* Please, respect the columns like the files inside [templates](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/csv/templates), as the script will read only the columns with the "correctly spelled" headers.
* Note that you don't have to write inside all the columns, as some of the columns are optionals and other are part of a possible option of the Beacon specification but incompatible with other columns (an exception will raise in case a column is misfilled).
We have filled an example of a .csv for each collection ready to be converted to BFF with the CINECA dataset. Please, take a look at it if you wish [here](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/csv/examples).

### Getting .json final documents

Before getting the .json final documents, please make sure your [conf.py](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/conf/conf.py) that you will find inside [conf](https://github.com/EGA-archive/beacon2-ri-tools-v2/tree/main/conf) file is reading the right .csv document(s) and execute the next bash script from the root folder in your terminal. All .csv files contained in the specified csv_folder will be transformed into .json:
```bash
docker exec -it ri-tools python convert_csvTObff.py
```

The final generated .json files, which are Beacon Friendly Format, will be in the output_docs folder with the name of the collection followed by .json extension, e.g. genomicVariations.json. 

This file will be able to be used in a mongoDB for beacon usage. To know how to import in a Beacon v2, please do as described in [Beacon v2 ri api](https://github.com/EGA-archive/beacon2-ri-api).

### Version notes

* Other file names and distribution of folder and files is not supported.

### Acknowledgements

Thanks to all the [EGA archive](https://ega-archive.org/) team, and specially: 
* Jordi Rambla, for guiding, supporting, helping and making possible the development of this tool.