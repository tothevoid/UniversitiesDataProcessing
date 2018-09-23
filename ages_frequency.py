import pandas as pd
from collections import defaultdict
import datetime
import helpers

universities = ['narfu','tsu','mgu']

curr_time = datetime.datetime.now()

for university in universities:
    dataset = pd.read_csv('./datasets/'+university+'.csv',';', encoding='ansi')
    dates = dataset.loc[:,['bdate']].astype(str)
    ages = defaultdict(int)
    for index,row in dates.iterrows():
        bdate = row['bdate']
        age = str(helpers.datetime_parse(bdate))
        ages[age] += 1
    ages = sorted(ages.items())
    print(ages)
 
    with open('age_freq_'+university+'.csv', 'w') as output_file:
        for i in ages:
            output_file.write(i[0]+';'+str(i[1])+'\n')