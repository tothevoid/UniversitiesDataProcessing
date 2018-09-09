import helpers
import pandas as pd
import json
import ast
import math
import io
import csv
from collections import defaultdict

def format_json(string):
    strs = string.replace("'",'"')
    if string == 'nan':
        return ''
    try:
        value = json.loads(strs)
        city = (value[0])['city']
        return(cities[str(city)])
    except:
        return ''

def fill_dicts():
  
    df = pd.read_csv('narfu.csv',';',encoding = 'ansi')
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

        if sch != uni and len(sch) != 0 and len(uni)!=0:
            before = row['schools'] + '-' + row['universities']
            before_dict[before] += 1 
        if uni != city and len(uni) != 0 and len(city)!=0:
            after = row['universities'] + '-' + row['city']
            after_dict[after] += 1

    temp = sorted(before_dict.items(), key=lambda x: x[1], reverse=True)

    result = list()
    for elm in temp:
        result.append({'Direction':elm[0],'Quantity':elm[1]})

    helpers.save_file('from-school-to-university', result)

before_dict = defaultdict(int)
after_dict = defaultdict(int)

with open('cities.json', encoding='utf-8-sig') as fl:
    cities = json.load(fl)

fill_dicts()
