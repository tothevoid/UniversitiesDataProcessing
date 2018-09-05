import csv
import os

def save_file(output_name, output_items):
    keys = output_items[0].keys()
    with open('%s.csv' % (output_name), 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_items)

def read_csv_as_dict(relative_path, delimeter):
    currdir = os.path.dirname(os.path.abspath(__file__))
    path =  os.path.join(currdir, relative_path)
    with open(path, newline='') as dataset:
        reader = csv.DictReader(dataset,delimiter = delimeter)
        return list(reader)