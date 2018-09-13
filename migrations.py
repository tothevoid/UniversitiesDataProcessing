import helpers
from collections import defaultdict
import pandas as pd
import numpy as np
import json
import math
import io
import csv

with open('cities.json', encoding='utf-8-sig') as fl:
    cities = json.load(fl)

def format_json(string):
    strs = string.replace("'",'"')
    if string == 'nan':
        return ''
    try:
        value = json.loads(strs)
        years = [x.get('year_graduated','') for x in value if x!= '']
        if len(value)==len(years):
            years = np.array(years)
            min_index = np.argmin(years)       
            city = (value[min_index])['city']
        else:
            city = (value[0])['city']
        return(cities[str(city)])
    except:
        return ''

def get_migrations(university):
    before_dict = defaultdict(int)
    after_dict = defaultdict(int)

    df = pd.read_csv(university+'.csv',';',encoding = 'ansi')
    df = df.loc[:,['city','home_town','schools','universities']]

    df[df.columns[[0,3]]] = df.iloc[:,[0,3]].astype(str)
    df['home_town'] = df['home_town'].astype(str)

    df = df[(df['schools']!='[]') & (df['universities']!='[]') & 
        #(df['home_town']!='nan') & (df['city']!="nan") & 
        (df['universities']!="nan") & (df['schools']!="nan")]

    df['schools'] = df['schools'].apply(format_json)
    df['universities'] = df['universities'].apply(format_json)
    #df.to_csv('cities.csv', sep=';', encoding='utf-8')
    for index, row in df.iterrows():
        sch = row['schools']
        uni = row['universities']
        city = row['city']
        if sch != uni and sch != '' and uni != '':
            before = row['schools'] + '-' + row['universities']
            before_dict[before] += 1 
        if uni != city and uni != '' and city != '':
            after = row['universities'] + '-' + row['city']
            after_dict[after] += 1
    sorted_directions = sorted(before_dict.items(), key=lambda x: x[1], reverse=True)
    result = [{'Direction':elm[0],'Quantity':elm[1]} for elm in sorted_directions]
    helpers.save_file('school-to-university-'+university, result)
    return before_dict, after_dict
    
get_migrations('narfu')
