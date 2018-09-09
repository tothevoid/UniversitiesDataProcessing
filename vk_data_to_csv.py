import helpers
import io
import os
import csv
import json
import datetime
from collections import defaultdict
from operator import itemgetter
from collections import OrderedDict

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
            if date == 'hidden':
                continue
            items = date.split('.')
            if len(items) < 3:
                continue
            date = datetime.datetime.now().year - int(items[2])
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
    helpers.save_file('bdays_new', result)

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
            if city == 'hidden':
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
    helpers.save_file('cities_new', result)

currdir = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(currdir, 'vk_data')

for fname in os.listdir(directory):
    if fname.endswith(".json"): 
        path = (os.path.join(directory, fname))
        with io.open(path, encoding='utf-8') as json_file:
            file_parse_bdays(json_file.read())
            json_file.seek(0)
            file_parse_cities(json_file.read())

