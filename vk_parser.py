import vk_api
import math
import os
import json
import csv
import helpers
import time

log = ''
password = ''

def get_freinds(ids_list):
    results = list()
    total_empty = 0
    count_of_iterations = math.ceil(len(ids_list)/25.0)
    delay = 0
    with open('script.js', 'r') as script_file:
        script = script_file.read()
    for i in range(count_of_iterations):
        if (i % 100 == 0 and i!=0):
            results = save_results('iter%s'%(i),results)
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
                bdate = friend.get('bdate','hidden')
                city = friend.get('city','hidden')
                city = city['title'] if city!='hidden' else city
                friends.append({'city':city,'bdate':bdate})
            results.append({'Id':sequence[index], 'Friends':friends})
        time.sleep(delay)
        time_passed = time.time()-start
        print('iteration %s passed and it takes %ss' % (i+1, round(time_passed,1)))
    results = save_results('last_iter',results)
    print(total_empty)

def save_results(name,results):
    js = json.dumps(results)
    with open(name + '.json', 'w', encoding='utf-8') as outfile:
        outfile.write(js)
    #change it
    return list()

def vk_execute(script, ids):
    vk_session = vk_api.VkApi(log, password)
    vk_session.auth()
    vk = vk_session.get_api()
    content = script.replace('{{ids}}',ids)
    return vk.execute(code=content)

#distinct ids

reader = helpers.read_csv_as_dict('narfu.csv',';')
reader = [item['id'] for item in reader]
get_freinds(list(reader))

