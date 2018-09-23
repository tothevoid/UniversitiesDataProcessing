import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import json
import io
import helpers
import ast

with open('cities.json', encoding='utf-8-sig') as fl:
    cities = json.load(fl)

def format_json(string):
    if string == 'nan':
        return ''
    value = ast.literal_eval(string)
    years = [x.get('year_graduated','') for x in value if x!= '']
    if len(value)!=len(years):
        years = [x.get('year_to','') for x in value if x!= '']
    if len(value)==len(years):
        years = np.array(years)
        min_index = np.argmin(years)       
        city = (value[min_index])['city']
    else:
        city = (value[0])['city']
    if city <= 0:
        return ''
    res_str = (cities[str(city)])
    return(res_str)

def get_migrations(university, univercity_city, is_schools):
    result_dict = defaultdict(int)
    path = Path('datasets') / (university+'.csv')

    df = pd.read_csv(path,';',encoding = 'ansi', low_memory=False)
    df = df.loc[:,['city','home_town','schools','universities']]

    cols = len(df.columns) - 1
    df[df.columns[[0,cols]]] = df.iloc[:,[0,cols]].astype(str)
   
    from_before = len(df.schools.values) if is_schools else len(df.universities.values)
    to_before = len(df.universities.values) if is_schools else len(df.city.values)

    if is_schools:
        df = df[(df['schools']!='[]') & (df['schools']!="nan") & (df['universities']!="nan") & (df['universities']!='[]')]
        df['schools'] = df['schools'].apply(format_json)
        df['universities'] = df['universities'].apply(format_json)
        from_after = len(df[df.schools != ''].schools.values)
        to_after = len(df[df.universities != ''].universities.values)
    else:
        df = df[(df['city']!="nan") & (df['universities']!="nan") & (df['universities']!='[]')]
        df['universities'] = df['universities'].apply(format_json)
        from_after = len(df[df.universities != ''].universities.values)
        to_after = len(df[df.city != ''].city.values)

    stayed = income = size = 0

    for index, row in df.iterrows():
        sch = row['schools']
        uni = row['universities']
        city = row['city']
        if (is_schools and sch == uni) or (not is_schools and uni == city):
            stayed+=1
            size+=1
            continue
        if is_schools and sch != uni and sch != '' and uni != '' and univercity_city == uni:
            result_dict[sch] += 1 
            income +=1
            size+=1
        elif not is_schools and uni != city and uni != '' and city != '' and city!='nan' and uni == univercity_city:
            result_dict[city] += 1
            income +=1
            size+=1
    
    sorted_directions = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    result = [{'from':elm[0],
            'quantity':elm[1],
            'rate_all':round(elm[1]*1.0/size,5),
            'rate_migrated':round(elm[1]*1.0/income,5)} 
            for elm in sorted_directions]
    
    print('Местные/приехавшие: %s/%s. Кол-во населённых пунктов %s. Всего %s' % (stayed, income, len(result_dict), stayed+income))
    print('Фильтрация. До %s/%s. После %s/%s' % (from_before,to_before, from_after, to_after)) 
   
    if is_schools:
        res_type = 'schools'
    else:
        res_type = 'universities'

    if (len(result) > 0):
        helpers.save_file(university+'_mirgrations_'+res_type, result)
    else:
        print('Результат отсутствует')