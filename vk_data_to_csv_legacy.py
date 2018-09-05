import io
import os
import csv
import helpers
import json
import datetime
from collections import defaultdict
from operator import itemgetter
from collections import OrderedDict

def file_parse_bdays(persons):
    result = list()
    for key, value in persons.items():
        ids = key.split(',')
        i = 0
        response = json.loads(value)
        for person in response['response']:
            current_id = ids[i]
            i += 1 
            friends_quantity = 0
            friends_with_bdays = 0
            total_friends_age = 0
            ages = {
                '22': 0,'27': 0,'32': 0,
                '37': 0,'42': 0,'47': 0,
                '52': 0,'57': 0,'62': 0,
                '67': 0,'72': 0,'77': 0,
                '82': 0
            }
            if person:
                friends_quantity = len(person)
                for friend in person:  
                    date = friend.get("bdate")
                    if date is None:
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
            else:
                continue
            ages.update({'id':current_id})
            ages.update({'total':friends_quantity})
            avg = 0.0 if friends_with_bdays==0 else round(total_friends_age/friends_with_bdays,2)
            ages.update({'avg':avg})
            result.append(ages)
    return result

def file_parse_city(persons):
    result = list()
    for key, value in persons.items():
        ids = key.split(',')
        i = 0
        response = json.loads(value)   
        for person in response['response']:
            current_id = ids[i]
            i += 1 
            if person:
                friends_quantity = len(person)
                cities = defaultdict(float)
                for friend in person:  
                    city = friend.get("city")
                    if city is None:
                        continue
                    cities[city["title"]] += 1 
            else:
                continue
            towns = { 
                '0': '', '1': '', '2':'',
                '3': '', '4': '', 
            }
            cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
            # cities = OrderedDict(sorted(cities.items()))
            # for k, v in cities.items():
            #     cities[k] = v/friends_quantity
            j = 0
            for item in cities[:5]:
                towns[str(j)] = '%s:%s' % (item[0],round(item[1]/friends_quantity,2))
                j+=1
            towns.update({'id':current_id})
            towns.update({'total':friends_quantity})
            result.append(towns)
    return result

currdir = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(currdir, 'vk_data')
#bdays = list()
cities = list()

for fname in os.listdir(directory):
    if fname.endswith(".txt"): 
        path = (os.path.join(directory, fname))
        with io.open(path, encoding='utf-8') as file:
            filteredLines = list(filter(lambda x: x != '\n', file.readlines()))
            persons = dict(zip([e[:-1] for e in filteredLines[::2]], filteredLines[1::2]))
            #bdays += file_parse_bdays(persons)
            cities += file_parse_city(persons)
#helpers.save_file('bdays', bdays)
helpers.save_file('cities', cities)

