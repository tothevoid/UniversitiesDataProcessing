import helpers
import io
import os
import csv
import json
import datetime
from collections import defaultdict
from operator import itemgetter
from collections import OrderedDict
from pathlib import Path

def file_parse_bdays(json_string):
    result = list()
    persons = json.loads(json_string)
    for item in persons:
        person_Id = item['Id']
        friends_list = item['Friends']
        friends_with_bdays = 0
        total_friends_age = 0  
        ages = {
            '22': 0,'27': 0,'32': 0,
            '37': 0,'42': 0,'47': 0,
            '52': 0,'57': 0,'62': 0,
            '67': 0,'72': 0,'77': 0,
            '82': 0
        }
        friends_quantity = len(friends_list)
        for friend in friends_list:  
            date = friend.get("bdate")
            if date == '' and len(date.split('.')) < 3:
                continue
            helpers.datetime_parse(date)
            total_friends_age += date
            friends_with_bdays += 1
            for k, v in ages.items():
                if date <= int(k):
                    ages[k] += 1
                    break
        ages.update({'id' : person_Id,'total' : friends_quantity})
        avg = 0.0 if friends_with_bdays==0 else round(total_friends_age/friends_with_bdays,2)
        ages.update({'avg':avg})
        result.append(ages)
    return result

def file_parse_cities(json_string):
    result = list()
    persons = json.loads(json_string)
    for item in persons:  
        person_Id = item['Id']
        friends_list = item['Friends']
        friends_quantity = len(item)
        cities = defaultdict(int)
        for friend in friends_list:  
            city = friend.get("city")
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
    bdays = list()
    cities = list()

    directory = Path('friends_'+university)
    for fname in os.listdir(directory):
        if fname.endswith(".json"): 
            path = directory / fname
            with io.open(path, encoding='utf-8') as json_file:
                bdays += file_parse_bdays(json_file.read())
                json_file.seek(0)
                cities += file_parse_cities(json_file.read())
    helpers.save_file('bdays_' + university, bdays)
    helpers.save_file('cities_' + university, cities)

