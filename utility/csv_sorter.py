__author__ = 'cloud'

import csv


target = '/home/cloud/Documents/Codes/TracesAnalyzer/log/statistic_liege.csv'
with open(target,'rt') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')
    next(reader)
    for row in reader:
        print row