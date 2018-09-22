import vk_api
import math
import os
import json
import csv
import helpers
import time
import pandas as pd
import numpy as np
import vk_auth
from pathlib import Path

directory = ''
log = ''
password = ''

def load_data(data):
    results = list()
    total_empty = 0
    count_of_iterations = math.ceil(len(data[:])/25.0)
    delay = 0
    start = time.time()
    with open('script.js', 'r') as script_file:
        script = script_file.read()
    for i in range(count_of_iterations):
        if (i % 100 == 0 and i!=0):
            save_results('iter%s'%(i),results)
            results = list()
        sequence = data[:][i*25 : i*25+25]
        ids_str = ','.join(str(e[0]) for e in sequence)
        j = 0
      
        for index,item in enumerate(vk_execute(script, ids_str)):
            item_id = sequence[index][0]
            item_bdate = sequence[index][1]
            item_sex = sequence[index][2]
            if item is None or len(item) == 0:
                total_empty+=1
                continue
            j+=1
            friends = list() 
            for friend in item:
                bdate = friend.get('bdate','')
                city = friend.get('city','')
                sex = friend.get('sex','')
                city = city['title'] if city!='' else city
                friends.append({'city':city,'bdate':bdate, 'sex':sex})
            results.append({'id':item_id,'bdate':item_bdate,'sex':item_sex,'friends':friends})
        time.sleep(delay)
        time_passed = (time.time()-start) / (i+1) * (count_of_iterations - i) / 60
        print('iteration %s of %s passed (%sm left)' % (i+1,count_of_iterations,round(time_passed,2)),end='\r')
    save_results('last_iter',results)
    print(total_empty)

def save_results(name,results):
    global directory
    js = json.dumps(results)
    fname = name + '.json'
    with open(Path(directory) / fname, 'w', encoding='utf-8') as outfile:
        outfile.write(js)

def vk_execute(script, ids):
    vk_session = vk_api.VkApi(log, password)
    vk_session.auth()
    vk = vk_session.get_api()
    content = script.replace('{{ids}}',ids)
    return vk.execute(code=content)

def get_freinds(university):
    print('Current university:',university)
    global log
    global password
    global directory
    log, password = vk_auth.get_logpass()
    directory = './friends_' + university + '/'
    df = pd.read_csv('./datasets/'+university+'.csv',';', encoding='ansi')
    df = df.dropna(subset=['id'])
    df = df.drop_duplicates(subset=['id'])
    df.id = df.id.astype(int)
    df.bdate = df.bdate.astype(str)
    dataset = df.loc[:,['id','bdate','sex']].values
    if not os.path.exists(directory):
        os.makedirs(directory)
    load_data(dataset)