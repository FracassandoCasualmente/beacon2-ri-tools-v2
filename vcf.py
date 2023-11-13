import vcfpy
import re
import openpyxl

dict_to_xls={}
new_dict_to_xls={}
vcf = vcfpy.Reader.from_path('files/vcf/chr22.Test.1000G.phase3.joint.norm.ann.dbnsfp.clinvar.cosmic.vcf.gz')
i=0
header_list = ['#CHROM', 'POS','ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'] + vcf.header.samples.names


for v in vcf:
    i+=1
    for value in v.ALT:
        ALT = str(value.value)
    line = [v.CHROM, v.POS, v.ID, v.REF, ALT, v.QUAL, v.FILTER, v.INFO, v.FORMAT]
    line += [alt.value for alt in v.ALT]
    line += [call.data.get('GT') or './.' for call in v.calls]
    dict_to_xls['variation_alternateBases'] = line[3]
    dict_to_xls['variation_referenceBases'] = line[4]
    for k,v in line[7].items():
        if k == 'VT':
            dict_to_xls['variation_variantType'] = v[0]
        elif k == 'ANN':
            line7splitted = v[0].split("|")
            dict_to_xls['molecularAttributes_molecularEffects_label'] = line7splitted[1]
            dict_to_xls['molecularAttributes_molecularEffects_id'] = "ENSGLOSSARY:0000174"
            dict_to_xls['molecularAttributes_aminoacidChanges'] = "."
            dict_to_xls['molecularAttributes_geneIds'] = line7splitted[3]
    dict_to_xls['variantInternalId'] = 'chr' + str(line[0]) + '_' + str(line[1]) + '_' + str(line[3]) + '_' + str(line[4])
    zigosity={}
    zigosity['0/1']='GENO_0000458'
    zigosity['1/0']='GENO_0000458'
    zigosity['1/1']='GENO_0000136'
    j=0
    dict_to_xls['caseLevelData_zygosity_id'] =''
    dict_to_xls['caseLevelData_zygosity_label']=''
    for zygo in line[9:-1]:
        num = 9 + j
        if dict_to_xls['caseLevelData_zygosity_id'] == '':
            if zygo == '1/0' or zygo == '0/1' or zygo== '1/1':
                dict_to_xls['caseLevelData_zygosity_id'] = zygo
                dict_to_xls['caseLevelData_zygosity_label'] = zigosity[zygo]
                dict_to_xls['caseLevelData_biosampleId'] = header_list[num]
        else:
            if zygo == '1/0' or zygo == '0/1' or zygo== '1/1':
                dict_to_xls['caseLevelData_zygosity_id'] = dict_to_xls['caseLevelData_zygosity_id'] + ',' + zygo
                dict_to_xls['caseLevelData_zygosity_label'] = dict_to_xls['caseLevelData_zygosity_label'] + ',' + zigosity[zygo]
                dict_to_xls['caseLevelData_biosampleId'] = dict_to_xls['caseLevelData_biosampleId'] + ',' + header_list[num]
        j+=1
    dict_to_xls['identifiers_genomicHGVSId'] = str(line[0]) + ':' + 'g.' + str(line[1]) + line[4] + '>' + line[3]
    dict_to_xls['variation_location_interval_start_value'] = int(line[1]) -1
    dict_to_xls['variation_location_interval_start_type']="Number"
    dict_to_xls['variation_location_interval_end_value'] = int(line[1])
    dict_to_xls['variation_location_interval_end_type']="Number"
    dict_to_xls['variation_location_interval_type']="SequenceInterval"
    dict_to_xls['variation_location_type']="SequenceLocation"
    dict_to_xls['variation_location_sequence_id']="HGVSid:" + str(line[0]) + ":g." + str(line[1]) + line[4] + ">" + line[3]






    xls_Book = 'datasheets/genomicVariations.xlsx'

    wb = openpyxl.load_workbook(xls_Book)

    sheet = wb['Sheet1']

    list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                    'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                    'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                    'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                    'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
    ]

    dict_columns={}
    
    l=0
    while l < len(list_columns):
        property = list_columns[l]+str(1)
        property_value = sheet[property].value
        if property_value is not None:
            dict_columns[property]=property_value
        l+=1

    for key, value in dict_to_xls.items():
        for k, v in dict_columns.items():
            if key == v:
                result = ''.join([i for i in k if not i.isdigit()])
                result = result + str(i+1)
                new_dict_to_xls[result]=value
    print(i)
    if i == 1005:
        break



for key, value in new_dict_to_xls.items():
    sheet[key].value = value

wb.save(xls_Book)

