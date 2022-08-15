from asyncore import read
from gettext import find
from hashlib import new
from importlib.resources import path
from os import remove
from unicodedata import name
import pandas as pd
import pathlib

def get_path_xlsx():
    file = pathlib.Path('./').glob('./output_files/*.xlsx').__next__()
    return './' + str(file.relative_to('./'))


def to_lower(data):
    return str(data).lower()


# Verifica se existe algum item na lista sem informações e os remove
def remove_empty_items(colection):
    for item in colection:
        if(item == ',' or item == ''):
            colection.remove(item)

    return colection

def unameless():
    table = pd.read_excel(get_path_xlsx())
    col1 = list(map(to_lower, table[table.columns[1]].to_list()))
    new_col1 = []

    for i in range(0,len(col1)):
        # Caso encontre uma célula da coluna com um valor diferente de 'NaN'
        # remove o '\n' se houver e adiciona na nova coluna
        if(col1[i] != 'nan'):
            new_cel = col1[i].replace('\n',',') if (col1[i].find('\n') > 0) else col1[i]
            new_col1.append(new_cel)
        # Caso o indice esteja dentro do intervalo, verifica se
        # o conteúdo da célula é igual a 'NaN' e se a célula anterior ou posterior
        # é diferente de 'NaN'. Se sim, adiciona na nova coluna o '||'
        elif( i > 0 and i < len(col1)-1):
            if(col1[i] =='nan' and col1[i-1] != 'nan' or col1[i+1] != 'nan'):
                new_col1.append('||')

    # transforma a lista 'new_col1' em string para 'splitar' cada refeição
    # em uma lista diferente
    colection = str(',').join(new_col1).split('||')
    colection = remove_empty_items(colection)
    meals = []

    for item in colection:
        meals.append(item.split(','))

    for item in meals:
        item = remove_empty_items(item)
    print(meals)

unameless()


