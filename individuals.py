import json
import openpyxl
from tqdm import tqdm

list_of_excel_items=[]
list_of_definitions_required=[]
list_of_properties_required=[]
list_of_headers_definitions_required=[]

with open("files/items/individuals.txt", "r") as txt_file:
    list_of_excel_items=txt_file.read().splitlines() 
with open("files/properties/individuals.txt", "r") as txt_file:
    list_of_properties_required=txt_file.read().splitlines() 
with open('files/dictionaries/individuals.json') as json_file:
    dict_properties = json.load(json_file)

def commas(prova):
    length_iter=0
    array_of_newdicts=[]
    for key, value in prova.items():
        if isinstance(value, str):
            valuesplitted = value.split(',')
            length_iter=len(valuesplitted)
    if length_iter > 0:
        i=0
        while i < length_iter:
            newdict={}
            for key, value in prova.items():
                if isinstance(value, str):
                    valuesplitted = value.split(',')
                    newdict[key]=valuesplitted[i]
                elif isinstance(value, int):
                    valuesplitted = value.split(',')
                    newdict[key]=valuesplitted[i]
                elif isinstance(value, dict):
                    newdict[key]={}
                    for k, v in value.items():
                        if isinstance(v, str):
                            vsplitted = v.split(',')
                            newdict[key][k]=vsplitted[i]
                        elif isinstance(v, int):
                            newdict[key][k]=v
                        elif isinstance(v, dict):
                            newdict[key][k]={}
                            for k1, v1 in v.items():
                                if isinstance(v1, str):
                                    v1splitted = v1.split(',')
                                    newdict[key][k][k1]=v1splitted[i]

            array_of_newdicts.append(newdict)
            i+=1
    else:
        array_of_newdicts.append(prova)
    return(array_of_newdicts)

def generate(list_of_excel_items, list_of_properties_required, dict_properties):




    wb = openpyxl.load_workbook('datasheets/CINECA_synthetic_cohort_EUROPE_UK1.xlsx')

    sheet = wb['individuals']

    list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                    'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                    'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                    'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                    'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
    ]


    dict_of_properties={}
    list_of_filled_items=[]
    total_dict =[]
    num_registries = 6
    k=0
    j=2
    pbar = tqdm(total = num_registries-2)
    while j < num_registries:
        i=0
        while i <(len(list_of_excel_items)+2):
            
            property = list_columns[i]+str(1)
            property_value = sheet[property].value

            number_sheet = list_columns[i]+str(j)
            

            
            valor = sheet[number_sheet].value
            if i > 1:
                if valor != None:
                    list_of_filled_items.append(property_value)
            measures_list_1 = ['measures|measurementValue|referenceRange|high', 'measures|measurementValue|referenceRange|low', 'measures|measurementValue|referenceRange|unit|id', 'measures|measurementValue|referenceRange|unit|label']
            measures_list_2 = ['measures|measurementValue|unit|id', 'measures|measurementValue|unit|label', 'measures|measurementValue|value']
            measures_list_3 = ['measures|measurementValue|typedQuantities|quantity|referenceRange|high', 'measures|measurementValue|typedQuantities|quantity|referenceRange|low', 'measures|measurementValue|typedQuantities|quantity|referenceRange|unit', 'measures|measurementValue|typedQuantities|quantity|unit|id', 'measures|measurementValue|typedQuantities|quantity|unit|label', 'measures|measurementValue|typedQuantities|quantity|value']
            measure_check_1=0
            measure_check_2=0
            measure_check_3=0
            for measure in list_of_filled_items:
                if 'measures' in measure:
                    if measure in measures_list_1:
                        measure_check_1+=1
                    elif measure in measures_list_2:
                        measure_check_2+=1
                    elif measure in measures_list_3:
                        measure_check_3+=1
            if measure_check_1 > 0:
                if measure_check_2>0 or measure_check_3>0:
                    raise Exception(('please, choose only one {} format').format('measurementValue'))
            elif measure_check_2 > 0:
                if measure_check_1>0 or measure_check_3>0:
                    raise Exception(('please, choose only one {} format').format('measurementValue'))
            elif measure_check_3 > 0:
                if measure_check_1>0 or measure_check_2>0:
                    raise Exception(('please, choose only one {} format').format('measurementValue'))



            for filled_item in list_of_filled_items:
                if isinstance(filled_item, str): 
                    if 'sex' in filled_item:
                        try:
                            list_of_properties_required.remove('sex')
                        except Exception:
                            pass
            if valor:
                dict_of_properties[property_value]=valor
            i +=1

        

        for lispro in list_of_properties_required:
            if lispro not in list_of_filled_items:
                raise Exception(('error: you are not filling all the required fields. missing field is: {}').format(lispro))

        definitivedict={}
        for key, value in dict_properties.items():
            if isinstance(value, list):
                definitivedict[key]=[]
                value_list=[]
                for item in value:
                    if isinstance(item, dict):
                        item_dict={}
                        for ki, vi in item.items():
                            if isinstance(vi, list):
                                vi_list=[]
                                for subitem in vi:
                                    if isinstance(subitem, dict):
                                        subitem_dict={}
                                        for k, v in subitem.items():
                                            if isinstance(v, dict):
                                                subitem_dict[k]={}
                                                for k1, v1 in v.items():
                                                    if isinstance(v1, dict):
                                                        subitem_dict[k][k1]={}
                                                        for k2, v2 in v1.items():
                                                            if isinstance(v2, dict): 
                                                                subitem_dict[k][k1][k2]={}
                                                                for k3, v3 in v2.items():
                                                                    new_item = ""
                                                                    new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2 + "|" + k3
                                                                    for propk, propv in dict_of_properties.items():
                                                                        if propk == new_item:
                                                                            subitem_dict[k][k1][k2][k3]=propv
                                                                if subitem_dict[k][k1][k2]=={}:
                                                                    del subitem_dict[k][k1][k2]
                                                            else:
                                                                new_item = ""
                                                                new_item = key + "|" + ki + "|" + k + "|" + k1 + "|" + k2
                                                                for propk, propv in dict_of_properties.items():
                                                                    if propk == new_item:
                                                                        subitem_dict[k][k1][k2]=propv   
                                                        if subitem_dict[k][k1]=={}:
                                                            del subitem_dict[k][k1]
                                                    else:
                                                        new_item = ""
                                                        new_item = key + "|" + ki + "|" + k + "|" + k1
                                                        for propk, propv in dict_of_properties.items():
                                                            if propk == new_item:
                                                                subitem_dict[k][k1]=propv 
                                                if subitem_dict[k]=={}:
                                                    del subitem_dict[k]
                                            else:
                                                new_item = ""
                                                new_item = key + "|" + ki + "|" + k
                                                for propk, propv in dict_of_properties.items():
                                                    if propk == new_item:
                                                        subitem_dict[k]=propv

                                            if subitem_dict != {}:
                                                if subitem_dict not in vi_list:
                                                    vi_list.append(subitem_dict)
                                                    item_dict[ki]=vi_list[0]
                
                            elif isinstance(vi, dict):
                                vi_dict={}
                                for ki1, vi1 in vi.items():
                                    if isinstance(vi1, dict):
                                        vi_dict[ki1]={}
                                        for ki2, vi2 in vi1.items():
                                            new_item = ""
                                            new_item = key + "|" + ki + "|" + ki1 + "|" + ki2
                                            for propk, propv in dict_of_properties.items():
                                                if propk == new_item:
                                                    vi_dict[ki1][ki2]=propv
                                            if vi_dict != {} and vi_dict[ki1] != {}:
                                                item_dict[ki]=vi_dict    
                                    else:
                                        new_item = ""
                                        new_item = key + "|" + ki + "|" + ki1
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                vi_dict[ki1]=propv 
                                                item_dict[ki]=vi_dict
        
                                if item_dict != {} and item_dict != [{}]:
                                    if item_dict not in value_list:
                                        value_list.append(item_dict)
                            else:
                                new_item = ""
                                new_item = key + "|" + ki
                                for propk, propv in dict_of_properties.items():
                                    if propk == new_item:
                                        item_dict[ki]=propv
                            if item_dict != {} and item_dict != [{}]:
                                if item_dict not in value_list:
                                    value_list.append(item_dict)

                        if value_list != []:
                            for itemvl in value_list:
                                list_to_def=commas(itemvl)
                                for itemldf in list_to_def:
                                    if itemldf not in definitivedict[key]:
                                        definitivedict[key].append(itemldf)
                        else:
                            for itemvl in value_list:
                                definitivedict[key].append(itemvl)     
                if definitivedict[key]==[]:
                    del definitivedict[key]
            elif isinstance(value, dict):
                value_dict={}
                for kd, vd in value.items():
                    if isinstance(vd, list):
                        vd_list=[]
                        if isinstance(vd[0], dict):
                            for kd1, vd1 in vd[0].items():
                                if isinstance(vd1, dict):
                                    for kd2, vd2 in vd1.items():
                                        new_item = ""
                                        new_item = key + "|" + kd + "|" + kd1 + "|" + kd2
                                        for propk, propv in dict_of_properties.items():
                                            if propk == new_item:
                                                value_dict[kd]={}
                                                value_dict[kd][kd1]={}
                                                value_dict[kd][kd1][kd2]=propv
                                else:
                                    new_item = ""
                                    new_item = key + "|" + kd + "|" + kd1
                                    for propk, propv in dict_of_properties.items():
                                        if propk == new_item:
                                            if ',' in propv:
                                                propv_splitted = propv.split(',')
                                                for itemsplitted in propv:
                                                    value_dict[kd]={}
                                                    value_dict[kd][kd1]=propv_splitted
                                                    if value_dict not in vd_list:
                                                        vd_list.append(value_dict)
                                            else:
                                                value_dict[kd]={}
                                                value_dict[kd][kd1]=propv
                                
                                if value_dict != {}:
                                    if value_dict not in vd_list:
                                        vd_list.append(value_dict)
                            if vd_list != []:
                                definitivedict[key]=vd_list
                        else:
                            new_item = ""
                            new_item = key + "|" + kd
                            for propk, propv in dict_of_properties.items():
                                if propk == new_item:
                                    value_dict[kd]=propv
                                    definitivedict[key]=value_dict
                    else:
                        new_item = ""
                        new_item = key + "|" + kd
                        for propk, propv in dict_of_properties.items():
                            if propk == new_item:
                                value_dict[kd]=propv
                                definitivedict[key]=value_dict
                if value == {}:
                    new_item = ""
                    new_item = key
                    for propk, propv in dict_of_properties.items():
                        if propk == new_item:
                            try:
                                propvalue={}
                                propvalue_splitted = propv.split(':')
                                propvalue[propvalue_splitted[0]]=propvalue_splitted[1]
                                definitivedict[key]=propvalue
                            except Exception:
                                pass
            else:
                new_item = ""
                new_item = key
                for propk, propv in dict_of_properties.items():
                    if propk == new_item:
                        definitivedict[key]=propv
        total_dict.append(definitivedict)
        j+=1
        pbar.update(1)
    pbar.close()
    return total_dict






    
dict_generado=generate(list_of_excel_items, list_of_properties_required, dict_properties)


with open('output_docs/individuals.json', 'w') as f:
    json.dump(dict_generado, f)

