import pandas as pd
from collections import defaultdict
import datetime
import helpers

universities = ['narfu','tsu','mgu']

curr_time = datetime.datetime.now()
#make datetimeparse func

for university in universities:
    dataset = pd.read_csv(university+'.csv',';', encoding='ansi')
    dates = dataset.loc[:,['bdate']].astype(str)
    ages = defaultdict(int)
    for index,row in dates.iterrows():
        bdate = row['bdate']
        if (university=='tsu'):
            if (bdate != '0'):
                age = curr_time.year - int(bdate)
        else:
            items = bdate.split('.')
            if len(items) == 3:
                age = curr_time.year - int(items[2]) - 1
                if (curr_time.month==int(items[1]) and curr_time.day >= int(items[0])) or (curr_time.month>int(items[1])):
                    age = datetime.datetime.now().year - int(items[2])  
        age = str(age)
        ages[age] += 1
    ages = sorted(ages.items())
    print(ages)
 
   
    with open('age_freq_'+university+'.csv', 'w') as output_file:
        for i in ages:
            output_file.write(i[0]+';'+str(i[1])+'\n')