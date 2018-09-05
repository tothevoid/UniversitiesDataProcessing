import io
import os
import csv
import datetime
import helpers

def union():
    currdir = os.path.dirname(os.path.abspath(__file__))
    narfu_path = os.path.join(currdir, 'narfu.csv')
    bdays_path = os.path.join(currdir, 'bdays.csv')

    input_file = csv.DictReader(open(narfu_path, newline=''),delimiter=';')
    bdays_file = csv.DictReader(open(bdays_path, encoding='utf-8', newline=''))
    bdays_file = list(bdays_file)

    result = list()
    for row in input_file:
        date = row['bdate']
        ids = row['id']
        print(ids)
        items = date.split('.')
        age = ''
        if len(items) == 3:
            curr_time = datetime.datetime.now()
            age = datetime.datetime.now().year - int(items[2]) - 1
            if (curr_time.month==int(items[1]) and curr_time.day >= int(items[0])) or (curr_time.month>int(items[1])):
                age = datetime.datetime.now().year - int(items[2])  
        for r in bdays_file:
            if r['id'] == ids:
                val = r
                val.update({'age':age})
                result.append(val)
                break

    print(result)
    print(len(result))

    helpers.save_file('ages',result)

def split_files():
    currdir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(currdir, 'ages.csv')
    reader = csv.DictReader(open(path, encoding='utf-8', newline=''))
    reader = list(reader)
  
    empty = list()
    nonempty = list()
    for row in reader:
        row.pop('total')
        row.pop('avg')
        if row['age'] == '0':
            empty.append(row)
        else:
            nonempty.append(row)

    len(empty)
    len(nonempty)
    helpers.save_file('test', empty)
    helpers.save_file('validate', nonempty)

split_files()