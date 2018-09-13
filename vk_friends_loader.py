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

directory = ''
log = ''
password = ''

def load_data(ids_list):
    results = list()
    total_empty = 0
    count_of_iterations = math.ceil(len(ids_list)/25.0)
    delay = 0
    with open('script.js', 'r') as script_file:
        script = script_file.read()
    for i in range(count_of_iterations):
        if (i % 100 == 0 and i!=0):
            save_results('iter%s'%(i),results)
            results = list()
        sequence = ids_list[i*25 : i*25+25]
        ids_str = ','.join(str(e) for e in sequence)
        j = 0
        start = time.time()
        for index,item in enumerate(vk_execute(script, ids_str)):
            if item is None or len(item) == 0:
                print('empty '+str(sequence[index]))
                total_empty+=1
                continue
            j+=1
            friends = list() 
            for friend in item:
                bdate = friend.get('bdate','')
                city = friend.get('city','')
                city = city['title'] if city!='' else city
                friends.append({'city':city,'bdate':bdate})
            results.append({'Id':sequence[index], 'Friends':friends})
        time.sleep(delay)
        time_passed = time.time()-start
        print('iteration %s of %s passed and it takes %ss' % (i+1,count_of_iterations,round(time_passed,1)))
    save_results('last_iter',results)
    print(total_empty)

def save_results(name,results):
    js = json.dumps(results)
    fname = name + '.json'
    with open(directory + fname, 'w', encoding='utf-8') as outfile:
        outfile.write(js)

def vk_execute(script, ids):
    vk_session = vk_api.VkApi(log, password)
    vk_session.auth()
    vk = vk_session.get_api()
    content = script.replace('{{ids}}',ids)
    return vk.execute(code=content)

def get_freinds(university):
    log, password = vk_auth.get_logpass()
    directory = './friends_' + university + '/'
    df = pd.read_csv('./datasets/'+university+'.csv',';', encoding='ansi')
    dataset = df.loc[:,'id'].values
    print('default size: ',dataset.size)
    if not os.path.exists(directory):
        os.makedirs(directory)
    dataset = np.unique(dataset)
    print('distincted size: ',dataset.size)
    load_data(dataset)