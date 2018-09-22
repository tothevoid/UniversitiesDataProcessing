import csv
import os
import datetime

def save_file(output_name, output_items):
    keys = output_items[0].keys()
    with open('%s.csv' % (output_name), 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_items)

def datetime_parse(dt):
    age = -1
    curr_time = datetime.datetime.now()
    items = dt.split('.')
    if len(items) == 3:
        age = datetime.datetime.now().year - int(items[2]) - 1
        if (curr_time.month==int(items[1]) and curr_time.day >= int(items[0])) or (curr_time.month>int(items[1])):
            age = datetime.datetime.now().year - int(items[2])  
    return age
