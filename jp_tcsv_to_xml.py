# title: jp_tcsv_to_xml
# description: A Python script for batch-converting Japanese csv and/or tsv files to xml.
# author: Peter Yanase
# version: 1.0
# license: GPLv3

# IMPORTANT! mojimoji can not be installed with pip on Python 3.9, so use Python 3.8 during the installation of cutlet.
# Do not forget to install mecab and and unidic-lite. For details, see: https://github.com/polm/fugashi

import os
import csv
from cutlet import Cutlet

def normalize(value):
    return str(Cutlet().slug(value)).replace('-', '_')

for file_name in os.listdir():
    if file_name.endswith('tsv'):
        source_data = csv.reader(open(file_name), delimiter ='\t')
    elif file_name.endswith('csv'):
        source_data = csv.reader(open(file_name))
    else:
        continue
    while True:
        do_or_not = input('Convert ' + file_name + ' to XML? [y/n]\n').lower()
        if do_or_not == 'y':
            first_row = True
            tags = []
            collection = normalize(input('Name your collection.\n'))
            entry = normalize(input('Name your entries.\n'))
            header = '<?xml version="1.0" encoding="UTF-8"?>\n<' + collection + '>\n'
            footer = '</' + collection + '>'
            output_file_name = file_name[:-3] + 'xml'
            output_file = open(output_file_name, 'w')
            output_file.write(header)
            for row in source_data:
                if first_row:
                    for tag in row :
                        tag = normalize(tag)
                        tags.append(tag)
                    first_row = False
                else:
                    output_file.write('\t<' + entry + '>\n')
                    for column_nr in range(len(tags)):
                        output_file.write('\t\t<' + tags[column_nr] + '>' + row[column_nr] + '</' + tags[column_nr] + '>\n')
                    output_file.write('\t</' + entry + '>\n')
            output_file.write(footer)
            output_file.close()
            print('XML file generated:', output_file_name + '\n')
            break
        elif do_or_not == 'n':
            break
        else:
            print('Input y or n\n')
print('No more csv or tsv files to convert!')
