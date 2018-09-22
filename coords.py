from time import sleep
import requests
import json
import pandas as pd

def set_file(university):
    df = pd.read_csv(university+'_mirgrations.csv',',',encoding='utf-8')
    df = df[df.quantity>=10]
    
    result = get_positions(df['from'].values)
    df.add(pd.DataFrame(result), fill_value=0)
    df.to_csv(university+'_migrations_coords.csv',sep=';',encoding='utf-8', index=False)
   
def get_positions(places):
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
    