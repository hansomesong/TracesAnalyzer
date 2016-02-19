# -*- coding: utf-8 -*-
__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
import pprint
from config.config import *
import datetime
from collections import Counter

# Import the targeted raw CSV file
rawCSV_file_liege = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_liege.csv')
rawCSV_file_temple = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_temple.csv')
rawCSV_file_ucl = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_ucl.csv')
rawCSV_file_umass = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_umass.csv')
rawCSV_file_wiilab = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_wiilab.csv')

# 开始统计各个 case 的个数
def num_case_counter(rawCSV_file):

    dict_case_time = {'case1': [],
                      'case3': [],
                      'case4': []}

    for line in open(rawCSV_file):
        lines = line.split(";")
        if lines[8] == "1":
            dict_case_time['case1'].extend([datetime.datetime.strptime(i.split(" ")[0], "%d/%m/%Y") for i in lines[15].split(",")])
        elif lines[8] == "3":
            dict_case_time['case3'].extend([datetime.datetime.strptime(i.split(" ")[0], "%d/%m/%Y") for i in lines[18].split(",")])
        elif lines[8] == "4":
            dict_case_time['case4'].extend([datetime.datetime.strptime(i.split(" ")[0], "%d/%m/%Y") for i in lines[18].split(",")])

    return dict_case_time

def statiscs_process(input_dict):
    for key, value in input_dict.iteritems():
        input_dict[key] = sorted(Counter(value).most_common(), key=lambda x: x[0])
        start_date = input_dict[key][0][0]
        involved_dates = [x[0] for x in input_dict[key]]
        for i in range(len(input_dict[key])):
            start_date += datetime.timedelta(days=1)
            if start_date not in involved_dates:
                input_dict[key].append((start_date, 0))
                print "Add datetime", start_date, "into current list"
        input_dict[key] = sorted(Counter(input_dict[key]).most_common(), key=lambda x: x[0])



if __name__ == "__main__":

     result =  num_case_counter(rawCSV_file_liege)

     statiscs_process(result)

     pprint.pprint(result)


