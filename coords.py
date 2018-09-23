from time import sleep
import requests
import json
import pandas as pd

def get_coords(university):
    df = pd.read_csv(university+'_mirgrations.csv',',',encoding='utf-8')
    df = df[df.quantity>=10]
    
    result = load_coords(df['from'].values)
    df.add(pd.DataFrame(result), fill_value=0)
    df.to_csv(university+'_migrations_coords.csv',sep=';',encoding='utf-8', index=False)
   
def load_coords(places):
    result = list()
    iters = 0
    
    for place in places:
        request = 'https://nominatim.openstreetmap.org/search?q=%s&format=json' % (place)
        try:
            r = requests.get(request).text
            json_response = json.loads(r)
            pl = json_response[0]
            result.append({'lat':pl['lat'], 'lon':pl['lon'], 'determined_name':pl['display_name']})
        except:
            result.append({'lat':'nan', 'lon':'nan', 'determined_name':'nan'})
        sleep(1)
        iters+=1
        print(iters,'of',len(places),end='\r')
    return result

def get_regions(name):
    with open(name) as input_file:
        res = input_file.readlines() 
    result = list()
    iters = 0
    names = [item.replace('\n','') for item in res]
    for name in names:
        request = 'https://nominatim.openstreetmap.org/search?q=%s&format=json&polygon_geojson=1' % (name)
        try:
            r = requests.get(request).text
            json_response = json.loads(r)
            pl = json_response[0]
            result.append({'name':name,'determined_name':pl['display_name'],'box':json.dumps(pl['geojson'])})
        except:
            result.append({'name':name,'determined_name':'nan','box':'nan'})
        sleep(1)
        iters+=1
        print(iters,'of',len(names),end='\r')
    df = pd.DataFrame(result)
    df.to_csv('regions.csv',sep=';',encoding='utf-8', index=False)
