import helpers
import io
import os
import csv
import json
import datetime
import math
import pandas as pd
from collections import defaultdict
from operator import itemgetter
from collections import OrderedDict
from pathlib import Path

def file_parse_bdays(json_string):
    result_male = list()
    result_female = list()
    persons = json.loads(json_string)
    persons = quantify_ages(persons)
    total = len(persons)
    current_iter = 0
    for item in persons:
        person_id = int(item['id'])
        person_sex = item['sex']
        person_bdate = item['bdate']
        if math.isnan(person_sex):
            continue
        else:
            person_sex = int(person_sex) - 1
        #person_bdate = helpers.datetime_parse(item['bdate'])
        friends_list = item['friends']
        male = list(filter(lambda x: x['sex'] == float(2), friends_list))
        female = list(filter(lambda x: x['sex'] == float(1), friends_list))
        
        male_ages = quantify(male, person_id, person_sex, person_bdate)
        female_ages = quantify(female, person_id, person_sex, person_bdate)
        result_male.append(male_ages)
        result_female.append(female_ages)
        
        print(current_iter*100.0/total,end='\r')
        current_iter += 1
    return result_male, result_female

def create_ranges_dict():
    min_age = 22
    max_age = 82
    step = 5
    dict_range = range(min_age,max_age+1,step)
    ages = dict()
    for elm in dict_range:
        ages[str(elm)] = 0
    return ages

def quantify(friends_list, root_id, root_sex, root_bdate):
    ages = create_ranges_dict()
    for friend in friends_list:  
        date = friend.get('bdate','')
        if date == 'nan' or len(date.split('.')) < 3:
            continue
        date = helpers.datetime_parse(date)
        for k, v in ages.items():
            if date <= int(k):
                ages[k] += 1
                break
    ages.update({'id' : root_id, 'sex' : root_sex, 'age' : root_bdate})
    return ages

def file_parse_cities(json_string):
    result = list()
    persons = json.loads(json_string)
    for item in persons:  
        person_Id = item['Id']
        friends_list = item['Friends']
        friends_quantity = len(item)
        cities = defaultdict(int)
        for friend in friends_list:  
            city = friend.get('city')
            if city == '':
                continue
            cities[city] += 1 
        towns = { 
            '0': '', '1': '', '2':'',
            '3': '', '4': '', 
        }
        cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
        j = 0
        for item in cities[:5]:
            towns[str(j)] = '%s:%s' % (item[0],round(item[1]/friends_quantity,2))
            j+=1
        towns.update({'id':person_Id, 'total':friends_quantity})
        result.append(towns)
    return result

def parse_json_files(university):
    bdays_male = list()
    bdays_female = list()
    #cities = list()

    directory = Path('friends_'+university)
    for fname in os.listdir(directory):
        if fname.endswith(".json"): 
            path = directory / fname
            with io.open(path, encoding='utf-8') as json_file:
                male, female = file_parse_bdays(json_file.read())
                bdays_male += male
                bdays_female += female
                print('File passed. Quantity of rows in result: ', len(bdays_male))
                #json_file.seek(0)
                #cities += file_parse_cities(json_file.read())
    male_test = [row for row in bdays_male if row['age']!=0]
    male_valid = [row for row in bdays_male if row['age']==0]
   
    female_test = [row for row in bdays_male if row['age']!=0]
    female_valid = [row for row in bdays_male if row['age']==0]
    
    helpers.save_file(university + '_age_male_test', male_test)
    helpers.save_file(university + '_age_male_valid', male_valid)
    helpers.save_file(university + '_age_female_test', female_test)
    helpers.save_file(university + '_age_female_valid', female_valid)
    #helpers.save_file('cities_' + university, cities)

def quantify_ages(dataset):
    result = list()
    
    df = pd.DataFrame(dataset)
    persons = df.loc[:,['bdate']]
    persons = persons.bdate.apply(helpers.datetime_parse).values
    min_val = 22
    max_val = 72
    step = 1

    ranges = (range(max_val+step))[min_val:max_val+step:step] 

    for item in persons:
        for i, val in enumerate(ranges):
            if item <= val:
                result.append(i)
                break
    if len(persons) != len(result):
        print('Some rows were out of range')
    
    df.update({'bdate':result})
    return df.to_dict('records')
