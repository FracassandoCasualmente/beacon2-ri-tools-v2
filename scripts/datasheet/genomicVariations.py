import json
import xlwings as xw

collection = 'ref_schemas/genomicVariations'
file_to_open= collection + '.json'
num_registries = 4
# Opening JSON file 
new_file = open(file_to_open,) 
   
# returns JSON object as   
# a dictionary 
data = json.load(new_file) 

   
commonDefinitions = open('ref_schemas/commondefinitions.json')
commonDefinitions = json.load(commonDefinitions)
commonComponents = open('ref_schemas/beaconcommoncomponents.json')
commonComponents = json.load(commonComponents)

dict_definitions={}
dict_properties={}

def oneof_function(oneof_array):
    list_oneof=[]
    for value in oneof_array:
        value1=subtypes(value)
        list_oneof.append(value1)
    for val in list_oneof:
        for k, v in val.items():
            if k == 'oneOf':
                list_oneof2=[]
                for lor in v:
                    lor1=subtypes(lor)
                    list_oneof2.append(lor1)

                nova_llista=[]
                for item in list_oneof2:
                    for clau, valor in item.items():
                        if 'ontologyTerm' in valor:
                            nou_dict={}
                            nou_dict[clau]={}
                            nou_dict[clau]['id']=""
                            nou_dict[clau]['label']=""
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
                        elif '.json' in valor:
                            nou_dict={}
                            nou_dict[clau]=subtypes(valor)
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
                        elif 'number' in valor:
                            nou_dict[clau]=0
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
                        elif 'string' in valor:
                            nou_dict[clau]=""
                            if nou_dict not in nova_llista:
                                nova_llista.append(nou_dict)
            else:
                if isinstance(v, dict):
                    new_dict={}
                    new_dict[k]={}
                    for ki, vi in v.items():
                        new_dict[k][ki]={}
                        if 'ontologyTerm' in vi:
                            new_dict[k][ki]["id"]=""
                            new_dict[k][ki]["label"]=""
                            if new_dict not in nova_llista:
                                nova_llista.append(new_dict)
                        elif '.json' in vi:
                            elementvi=subtypes(vi)
                            new_dict[k][ki]=elementvi
                            if new_dict not in nova_llista:
                                nova_llista.append(new_dict)
    listing=[]
    for item in nova_llista:
        new_dict={}
        for k, v in item.items():
            new_dict[k]={}
            if isinstance(v,dict):
                for key, value in v.items():
                    if 'ontologyTerm' in value:
                        new_dict[k][key]={}
                        new_dict[k][key]["id"]=""
                        new_dict[k][key]["label"]=""
                    elif '.json' in value:
                        valornou=subtypes(value)
                        new_dict[k][key]=valornou
                    elif 'number' in value:
                        new_dict[k][key]=0
                    elif 'string' in value:
                        new_dict[k][key]=""
                    elif key == 'type':
                        pass
                    else:
                        new_dict[k][key]=value
            elif k == 'value':
                new_dict[k]=0

        listing.append(new_dict)
    new_listing=[]
    for item in listing:
        typed_dict={}
        for k, v in item.items():
            if k == 'typedQuantities':
                typed_dict[k]={}
                for key, value in v.items():
                    if key == 'quantity':
                        typed_dict[k][key]={}
                        for clau, valor in value.items():
                            if 'ontologyTerm' in valor:
                                typed_dict[k][key][clau]={}
                                typed_dict[k][key][clau]["id"]=""
                                typed_dict[k][key][clau]["label"]=""
                            elif '.json' in valor:
                                valor_nou=subtypes(valor)
                                typed_dict[k][key][clau]=valor_nou
                            elif 'number' in valor:
                                typed_dict[k][key][clau]=0
                            elif 'string' in valor:
                                typed_dict[k][key][clau]=""
                            elif clau == 'type':
                                pass
                            else:
                                typed_dict[k][key][clau]=valor
        
            else:
                new_listing.append(item)
        new_listing.append(typed_dict)
    nuevalista=[]
    for item in new_listing:
        if item != {}:
            nuevalista.append(item)
    llisteta=[]
    for item in nuevalista:
        typed_dict2={}
        for k, v in item.items():
            if k == 'typedQuantities':
                typed_dict2[k]={}
                for key, value in v.items():
                    if key == 'quantity':
                        typed_dict2[k][key]={}
                        if isinstance(value, dict):
                            for clau, valor in value.items():
                                typed_dict2[k][key][clau]={}
                                if isinstance(valor, dict):
                                    for ki, vi in valor.items():
                                        if 'ontologyTerm' in vi:
                                            typed_dict2[k][key][clau][ki]={}
                                            typed_dict2[k][key][clau][ki]["id"]=""
                                            typed_dict2[k][key][clau][ki]["label"]=""
                                        elif '.json' in vi:
                                            valor_nou=subtypes(vi)
                                            typed_dict2[k][key][clau][ki]=valor_nou
                                        elif 'number' in vi:
                                            typed_dict2[k][key][clau][ki]=0
                                        elif 'string' in vi:
                                            typed_dict2[k][key][clau][ki]=""
                                        elif ki == 'type':
                                            pass
                                        else:
                                            typed_dict2[k][key][clau][ki]=vi
                                elif clau == 'value':
                                        typed_dict2[k][key][clau]=0
            else:
                if item not in llisteta:
                    llisteta.append(item)
        llisteta.append(typed_dict2)
    llista_final=[]
    for item in llisteta:
        if item != {}:
            llista_final.append(item)
    return llista_final

def oneofunc(array):
    new_array=[]
    for item in array:
        if 'ontologyTerm' in item:
            new_item={}
            new_item['id']=""
            new_item['label']=""
        elif 'Timestamp' in item:
            new_item=""
        else:
            new_item = subtypes(item)
        new_array.append(new_item)
    new_array2=[]
    for item in new_array:
        dict_2={}
        if isinstance(item, dict):
            for k,v in item.items():
                if 'string' in v:
                    dict_2[k]=""
                elif 'ontologyTerm' in v:
                    dict_2[k]={}
                    dict_2[k]["id"]=""
                    dict_2[k]["label"]=""
                elif '.json' in v:
                    element=subtypes(v)
                    dict_2[k]=element
                elif 'integer' in v:
                    dict_2[k]=0
                elif 'type' in k:
                    pass
                else:
                    dict_2[k]=v
        new_array2.append(dict_2)
    new_array3=[]
    for item in new_array2:
        dict_3={}
        if isinstance(item, dict):
            for k,v in item.items():
                dict_3[k]={}
                if isinstance(v, dict):
                    for key, value in v.items():
                        if 'string' in value:
                            dict_3[k][key]=""
                else:
                    dict_3[k]=v
        new_array3.append(dict_3)
    new_array4=[]
    for item in new_array3:
        if item == {}:
            new_array4.append("")
        else:
            new_array4.append(item)   

    return new_array4    

def overtypes(element):
    overtypes={}
    if isinstance(element, dict):
        for key, value in element.items():
            if isinstance(value, bool):
                overtypes[key]=value
            elif '.json' in value:
                new_value=subtypes(value)
                overtypes[key]=new_value
            elif 'string' in value:
                new_value=""
                overtypes[key]=new_value
            elif 'CURIE' in value:
                new_value=""
                overtypes[key]=new_value
            elif 'boolean' in value:
                new_value=True
                overtypes[key]=new_value
            elif isinstance(value, dict):
                new_value=""
                for k, v in value.items():
                    if k == 'oneOf':
                        if 'complexValue.json' in v:
                            new_value=oneof_function(v)
                        else:
                            new_value=oneofunc(v)
                if new_value != "":
                    overtypes[key]=new_value
                else:
                    overtypes[key]=value
            elif isinstance(value, list):
                overtypes[key]=value   
            elif value=='':
                overtypes[key]=value                
    return overtypes

def ontologyTerm():
    element=subtypes('ontologyTerm.json')
    element=overtypes(element)
    return element

def subtypes(file):
    openfile='ref_schemas/'+file
    age = open(openfile) 
    subdict = {}
    data = json.load(age)
    for key, value in data.items():
        if key == 'properties':
            for k,v in value.items():
                if k == 'required':
                    subdict[k]=v
                else:
                    subdict[k]=""
                if isinstance(v, dict):
                    for k1, v1 in v.items():
                        if k1 == 'type':
                            if v1 == 'array':
                                subdict[k]['type']='array'
                            else:
                                subdict[k]=v1
                        elif k1 == '$ref':
                            if 'ontologyTerm' in v1:
                                subdict[k]= 'ontologyTerm.json'
                            elif 'commonDefinitions' in v1:
                                v1_splitted = v1.split('/')
                                for kcd, vcd in commonDefinitions.items():
                                    if kcd == v1_splitted[-1]:
                                        for kcd1, vcd1 in vcd.items():
                                            if 'ontologyTerm' in vcd1:
                                                subdict[k]='ontologyTerm.json'
                                            elif kcd1 == 'type':
                                                subdict[k]={}
                                                subdict[k]=vcd1

                            else:
                                v1_splitted = v1.split('/')
                                subdict[k]=v1_splitted[-1]
                        elif k1 == 'oneOf':
                            subdict[k]={}
                            subdict[k]['oneOf']=[]
                            for valor in v1:
                                for kval, vval in valor.items():
                                    if kval == '$ref':
                                        vval_splitted = vval.split('/')
                                        subdict[k]['oneOf'].append(vval_splitted[-1])
                        elif k1 == 'items':
                            for k2, v2 in v1.items():
                                if k2 == '$ref':
                                    if '.json' in v2:
                                        v2_splitted = v2.split('/')
                                        subdict[k]={}
                                        subdict[k]['items']=v2_splitted[-1]
                                    else:
                                        v2_splitted = v2.split('/')
                                        subdict[k]={}
                                        for keyx, valuex in data.items():
                                            if keyx == 'definitions':
                                                for kx, vx in valuex.items():
                                                    if kx == v2_splitted[-1]:
                                                        for k1x, v1x in vx.items():
                                                            if k1x == 'properties':
                                                                for k2x, v2x in v1x.items():
                                                                    for k3x, v3x in v2x.items():
                                                                        if k3x == '$ref':
                                                                            if 'ontologyTerm' in v3x:
                                                                                subdict[k][k2x]='ontologyTerm.json'
                                                                            else:
                                                                                splitted_v = v3x.split('/')
                                                                                double_split = splitted_v[-1].split('/')
                                                                                subdict[k][k2x]=double_split[-1]
                                                                        elif k3x == 'type':
                                                                            subdict[k][k2x]=v3x
                                                            elif k1x == 'required':
                                                                subdict[k][k1x]=v1x
        elif key == 'type':
            subdict['type']=value
        elif key == 'oneOf':
            subdict['oneOf']=[]
            for valor in value:
                for kval, vval in valor.items():
                    if kval == '$ref':
                        vval_splitted = vval.split('/')
                        subdict['oneOf'].append(vval_splitted[-1])
    return subdict

for key, value in data.items():
    if key == 'definitions':
        definitions_array=value
for key, value in definitions_array.items():
    for k, v in value.items():
        if k == 'properties':
            dict_definitions[key]=v
for key, value in dict_definitions.items():
    for k, v in value.items():
        for k1, v1 in v.items():
            if k1 == '$ref':
                if 'ontologyTerm' in v1:
                    dict_definitions[key][k]=ontologyTerm()
                elif 'definitions' in v1:
                    v1_splitted = v1.split('/')
                    dict_definitions[key][k]=v1_splitted[-1]
            elif k1 == 'type':
                if 'string' in v1:
                    dict_definitions[key][k]=''
                elif 'number' in v1:
                    dict_definitions[key][k]=0
                elif 'object' in v1:
                    dict_definitions[key][k]={}
            elif k1 == 'items':
                for k2, v2 in v1.items():
                    if k2 == '$ref':
                        v2_splitted = v2.split('/')
                        dict_definitions[key][k]=[]
                        dict_definitions[key][k].append(v2_splitted[-1])
                    elif k2 == 'type':
                        if 'string' in v2:
                            dict_definitions[key][k]=[]
                            dict_definitions[key][k].append('')


for key, value in dict_definitions.items():
    for k, v in value.items():
        if isinstance(v, str):
            if v != '':
                for kd, vd in dict_definitions.items():
                    if kd == v:
                        dict_definitions[key][k]=vd
        elif isinstance(v, list):
            if v != ['']:
                if 'ontologyTerm' in v[0]:
                    new_list=[]
                    new_list.append(ontologyTerm())
                    dict_definitions[key][k]=new_list
                else:
                    for kl, vl in dict_definitions.items():
                        if kl == v[0]:
                            new_list=[]
                            new_list.append(vl)
                            dict_definitions[key][k]=new_list


for key, value in data.items():
    if key == 'properties':
        properties_array=value

for key, value in properties_array.items():
    for k, v in value.items():
        if k == '$ref':
            if 'ontologyTerm' in v:
                dict_properties[key]=ontologyTerm()
            elif 'definitions' in v:
                v_splitted = v.split('/')
                dict_properties[key]=v_splitted[-1]
        elif k == 'type':
            if 'string' in v:
                dict_properties[key]=''
            elif 'number' in v:
                dict_properties[key]=0
            elif 'object' in v:
                dict_properties[key]={}
        elif k == 'items':
            for k2, v2 in v.items():
                if k2 == '$ref':
                    v2_splitted = v2.split('/')
                    dict_properties[key]=[]
                    dict_properties[key].append(v2_splitted[-1])
                elif k2 == 'type':
                    if 'string' in v2:
                        dict_properties[key]=[]
                        dict_properties[key].append('')
        elif k == 'oneOf':
            list_elements=[]
            for element in v:
                for ke, ve in element.items():
                    ve_splitted = ve.split('/')
                    list_elements.append(ve_splitted[-1])
            dict_properties[key]={}
            dict_properties[key]['oneOf']=list_elements
    
for k, v in dict_properties.items():
    if isinstance(v, str):
        if v != '':
            for kd, vd in dict_definitions.items():
                if kd == v:
                    dict_properties[k]=vd
    elif isinstance(v, list):
        if v != ['']:
            if 'ontologyTerm' in v[0]:
                new_list=[]
                new_list.append(ontologyTerm())
                dict_properties[k]=new_list
            elif '.json' in v[0]:
                print(v)
                new_list=[]
                new_list.append(subtypes(v[0]))
                dict_properties[k]=new_list
            else:
                for kl, vl in dict_definitions.items():
                    if kl == v[0]:
                        new_list=[]
                        new_list.append(vl)
                        dict_properties[k]=new_list
    elif isinstance(v, dict):
        new_list=[]
        for k1, v1 in v.items():
            for item in v1:
                for kl, vl in dict_definitions.items():
                    if kl == item:
                        new_list.append(vl)
            dict_properties[k]=new_list[0]

#print(dict_properties)


for key, value in dict_properties.items():
    if isinstance(value, dict):
        for k, v in value.items():
            if isinstance(v, str):
                if v != '':
                    if v == 'Location':
                        dict_properties[key][k]=''
                    else:
                        for kd, vd in dict_definitions.items():
                            if kd == v:
                                dict_properties[key][k]=vd
            elif isinstance(v, list):
                if v != ['']:
                    if '.json' in v[0]:
                        new_list=[]
                        new_list.append(subtypes(v[0]))
                        dict_properties[key][k]=new_list
                    else:
                        for kl, vl in dict_definitions.items():
                            if kl == v[0]:
                                new_list=[]
                                new_list.append(vl)
                                dict_properties[key][k]=new_list


list_of_definitions_required=[]
list_of_properties_required=[]
list_of_headers_definitions_required=[]


for key, value in definitions_array.items():
    for k, v in value.items():
        if k == 'required':
            for item in v:
                all_name = key + '_' + item
                list_of_headers_definitions_required.append(key)
                list_of_definitions_required.append(all_name)

for key, value in data.items():
        if key == 'required':
            for item in value:
                list_of_properties_required.append(item)

def generate(dict_properties):
    list_of_excel_items=[]
    for key, value in dict_properties.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for ki, vi in item.items():
                        if isinstance(vi, list):
                            for subitem in vi:
                                if isinstance(subitem, dict):
                                    for k, v in subitem.items():
                                        if isinstance(v, dict):
                                            for k1, v1 in v.items():
                                                if isinstance(v1, dict):
                                                    for k2, v2 in v1.items():
                                                        if isinstance(v2, dict):
                                                            for k3, v3 in v2.items():
                                                                new_item = ""
                                                                new_item = key + "_" + ki + "_" + k + "_" + k1 + "_" + k2 + "_" + k3
                                                                list_of_excel_items.append(new_item)            
                                                        else:
                                                            new_item = ""
                                                            new_item = key + "_" + ki + "_" + k + "_" + k1 + "_" + k2
                                                            list_of_excel_items.append(new_item)                                        
                                                else:
                                                    new_item = ""
                                                    new_item = key + "_" + ki + "_" + k + "_" + k1
                                                    list_of_excel_items.append(new_item)
                                        else:
                                            new_item = ""
                                            new_item = key + "_" + ki + "_" + k
                                            list_of_excel_items.append(new_item)
                        elif isinstance(vi, dict):
                            for ki1, vi1 in vi.items():
                                if isinstance(vi1, dict):
                                    for ki2, vi2 in vi1.items():
                                        new_item = ""
                                        new_item = key + "_" + ki + "_" + ki1 + "_" + ki2
                                        list_of_excel_items.append(new_item)     
                                else:
                                    new_item = ""
                                    new_item = key + "_" + ki + "_" + ki1
                                    list_of_excel_items.append(new_item)      
                        else:
                            new_item = ""
                            new_item = key + "_" + ki
                            list_of_excel_items.append(new_item) 
        elif isinstance(value, dict):
            for kd, vd in value.items():
                if isinstance(vd, list):
                    if isinstance(vd[0], dict):
                        for kd1, vd1 in vd[0].items():
                            if isinstance(vd1, dict):
                                for kd2, vd2 in vd1.items():
                                    new_item = ""
                                    new_item = key + "_" + kd + "_" + kd1 + "_" + kd2
                                    list_of_excel_items.append(new_item)
                            else:
                                new_item = ""
                                new_item = key + "_" + kd + "_" + kd1
                                list_of_excel_items.append(new_item)
                    else:
                        new_item = ""
                        new_item = key + "_" + kd
                        list_of_excel_items.append(new_item)  
                else:
                    new_item = ""
                    new_item = key + "_" + kd
                    list_of_excel_items.append(new_item)

        else:
            new_item = ""
            new_item = key
            list_of_excel_items.append(new_item)





    xls_Book = 'datasheets/genomicVariations.xlsx'

    wb = xw.Book(xls_Book)

    sheet = wb.sheets['Sheet1']

    list_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                    'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ',
                    'CA', 'CC', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
                    'DA', 'DD', 'DD', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ',
                    'EA', 'EE', 'EE', 'EE', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
    ]



    print(list_of_excel_items)

    i=0
    for element in list_of_excel_items:
        number_sheet = list_columns[i]+str(1)
        sheet[number_sheet].value = element
        i+=1

    with open("files/items/genomicVariations.txt", "w") as txt_file:
        for line in list_of_excel_items:
            txt_file.write("".join(line) + "\n")

    with open("files/definitions/genomicVariations.txt", "w") as txt_file:
        for line in list_of_definitions_required:
            txt_file.write("".join(line) + "\n")

    with open("files/headers/genomicVariations.txt", "w") as txt_file:
        for line in list_of_headers_definitions_required:
            txt_file.write("".join(line) + "\n")

    with open("files/properties/genomicVariations.txt", "w") as txt_file:
        for line in list_of_properties_required:
            txt_file.write("".join(line) + "\n")

    with open('files/dictionaries/genomicVariations.json', 'w') as f:
        json.dump(dict_properties, f)




dict_generado = generate(dict_properties)