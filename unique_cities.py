import numpy as np
import pandas as pd
import json
from pathlib import Path
from collections import defaultdict
import ast

def find_cities(uni):
    path = Path('datasets') / (uni+'.csv')
    df = pd.read_csv(path,';',encoding='ansi')
   
    schools = df.schools.astype(str).values
    universities = df.universities.astype(str).values
    container =  np.concatenate((schools, universities), axis=0)
    
    res_dict = defaultdict(int)

    for row in container:
        if row == 'nan':
            continue             
        items = ast.literal_eval(row) 
        for item in items:
            city = item['city']
            res_dict[city] +=1
    return [*res_dict]

def get_cities(universities):
    total = defaultdict(int)
    
    for uni in universities:
        new_cities = find_cities(uni)
        for k,v in new_cities.items():
            total[k] += v
    
    with open('res.txt','w') as output:
        for i in total:
            output.write(str(i)+'\n')
    

