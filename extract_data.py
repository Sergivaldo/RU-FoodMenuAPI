from hashlib import new
import pandas as pd
import pathlib
from pandas import DataFrame
import json

def get_path_xlsx():
    file = pathlib.Path('./').glob('./input_files/xlsx/*.xlsx').__next__()
    return './' + str(file.relative_to('./'))


def to_lower(table):
    for i in range(0,len(table.columns)):
        table[table.columns[i]] = table[table.columns[i]].str.lower()
    
    return table
        
# Verifica se existe algum item na lista sem informações e os remove
def remove_empty_items(colection):
    for item in colection:

        if(item == ',' or item == '' or len(item) == 0):
            colection.remove(item)

    return colection

def extract_column(table, name_col,value_init_row):
    index_init_row = table.index[table[name_col].str.find(value_init_row) >= 0].to_list()[0]
    col = table[name_col].to_list()
    new_col = []

    for i in range(index_init_row,len(col)):
        if(type(col[i] != 'str')):
            col[i] = str(col[i])

        if(col[i] != 'nan'):
            new_col.append(col[i])
        elif(col[i] == 'nan' and col[i-1] != 'nan'):
            new_col.append('|')       

    new_col = (',').join(new_col).split('|')
    
    for i in range(0,len(new_col)):
        new_col[i] = new_col[i].split(',')
        new_col[i] = remove_empty_items(new_col[i])
    
    return new_col
    
    

def create_json():

    def slice_list(list,start,end):
        slc = slice(start,len(list))
        new_list =  list[slc]
        return new_list

    def create_dict(keys, values):
        dic = {}
        values = slice_list(values,len(values) - len(keys),len(values))   
        
        for i in range(0,len(keys)):
            dic[keys[i]] = values[i]

        return dic


    table = pd.read_excel(get_path_xlsx())
    table = to_lower(table)
    categories = extract_column(table,table.columns[1],'bebida')
    days = ['segunda','terça','quarta','quinta','sexta','sábado','domingo']
    json_data ={}
    days_index = 0
    for i in range(2,9):  
        col = extract_column(table,table.columns[i],days[days_index])
        list_coffe = create_dict(categories[0],col[0])
        list_lunch = create_dict(categories[1],col[1])
        list_dinner = create_dict(categories[2],col[2])

        json_data[col[0][0]] = {   
            'cafe_da_manha':list_coffe,
            'almoco':list_lunch,
            'jantar':list_dinner
        }
        days_index+=1

    with open('./output_files/data.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    
create_json()