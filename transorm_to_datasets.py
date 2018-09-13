import io
import os
import csv
import datetime
import helpers
import numpy as np
import pandas as pd
from pathlib import Path

def transform(university, quantify):
    dataset_path =  Path('datasets', university+'.csv')
    bdays_path =  'bdays_'+university+'.csv'
    
    input_file = csv.DictReader(open(dataset_path, newline=''),delimiter=';')
    bdays_file = csv.DictReader(open(bdays_path, encoding='utf-8', newline=''))
    bdays_file = list(bdays_file)

    result = list()
    for row in input_file:
        date = row['bdate']
        ids = row['id']
        print(ids)
        age = helpers.datetime_parse(date)
        
        for r in bdays_file:
            if r['id'] == ids:
                val = r
                val.update({'age':age})
                result.append(val)
                break
    helpers.save_file('ages_'+university,result)
    
    empty = list()
    nonempty = list()
    for row in result:
        row.pop('total')
        row.pop('avg')
        if row['age'] == '':
            empty.append(row)
        else:
            nonempty.append(row)
    if quantify == True:
        quantified_test = quantify_ages(university)
        helpers.save_file('test_'+university, quantified_test)
    else:
        helpers.save_file('test_'+university, nonempty)
    helpers.save_file('validate_'+university, empty)

def quantify_ages(test_dataset):
    result = list()
    
    df = pd.DataFrame(test_dataset)
    persons = df.loc[:,['age']].values
    
    min_val = persons.min()
    max_val = persons.max()
    step = 1

    ranges = (range(max_val+step))[min_val:max_val+step:step] 
    print(len(ranges))

    for item in persons:
        for i, val in enumerate(ranges):
            if item <= val:
                result.append(i)
                break
    if len(persons) == len(result):
        print('Success')
    
    df.update({'age':result})
    return df.to_dict('records')

transform('narfu',True)