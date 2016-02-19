# -*- coding: utf-8 -*-
__author__ = 'yueli'
import operator
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

def statistics_process(input_dict, start_date, end_date):
    '''
       The statistics_process() method is used to process the returned dictionary by num_case_counter() by:
            counting the each case occurrence in each day
            add the date which is not present in the input dictionary
            sort the date list
    '''
    for key, value in input_dict.iteritems():
        # Since the input dictionary is with format such as:
        #   input_dict = {
        #       'case1' :   [datetime.datetime(2013,7,2,0,0), datetime.datetime(2013,7,2,0,0),
        #                                datetime.datetime(2013,7,2,0,0), datetime.datetime(2013,7,3,0,0)],
        #       'case2' :   [datetime.datetime(2013,7,2,0,0), datetime.datetime(2013,7,2,0,0),
        #                                datetime.datetime(2013,7,3,0,0), datetime.datetime(2013,7,3,0,0)],
        #       'case3' :   [datetime.datetime(2013,7,2,0,0), datetime.datetime(2013,7,2,0,0),
        #                                datetime.datetime(2013,7,3,0,0), datetime.datetime(2013,7,3,0,0)]
        #   }
        #   We want to know the occurrence of each element in the list associated with each case 1. To this end,
        #   we can use the Counter(UN_OBJECT_LIST).most_common() method, for example
        #   Counter(input_dict['case1']).most_common() return a list like this:
        #           [(datetime.datetime(2013,7,2,0,0), 3), (datetime.datetime(2013,7,3,0,0), 1)]
        #
        # We can further use python built-in method sorted() to sort a list. Different from list's sort method,
        # sorted() returns a new list. sorted(LIST, key=lambda x: x[0]) means the sort standard is to compare the
        # the first element in each element x.
        input_dict[key] = sorted(Counter(value).most_common(), key=lambda x: x[0])
        # # After sorting, now the minimum data is the first element of this list. The maximum datetim is the last
        # # element in this list. The next thing is to judge whether all dates between the minimum and maximum date are
        # # present in the list. If not, add this date into this list.
        # start_date = input_dict[key][0][0]
        # # For example, input_dict[key] = [(datetime.datetime(2013,7,2,0,0), 3), (datetime.datetime(2013,7,3,0,0), 1)]
        # # For example, input_dict[key][0] = (datetime.datetime(2013,7,2,0,0), 3)
        # # For example, input_dict[key][0][0] = datetime.datetime(2013,7,2,0,0)
        # end_date = input_dict[key][-1][0]
        # We need to know which dates are present in input_dict[key] and save them into a new list called: involved_dates
        involved_dates = [x[0] for x in input_dict[key]]
        for curr_date in datetime_generator(start_date, end_date, datetime.timedelta(days=1)):
            # print curr_date
            if curr_date not in involved_dates:
                input_dict[key].append((curr_date, 0))
                # print "Add datetime", curr_date, "into current list"
        # At last, do not forget to sort again (since the possible added elements are still in the last...)
        input_dict[key] = sorted(input_dict[key], key=lambda x: x[0])

def datetime_generator(start, end, delta):
    '''
        This method is a generator to generate a list of datetime between start and end. delta is the step
    '''
    curr = start
    while curr <= end:
        yield curr
        curr += delta


def avergae_statistics(rawCSV_files, start_date, end_date):
    tmp_list = []
    for rawCSV_file in rawCSV_files:
        result_dict = num_case_counter(rawCSV_file)
        statistics_process(result_dict, START_TIME, END_TIME)
        for key, value in result_dict.iteritems():
            result_dict[key] = [x[1] for x in value]
        tmp_list.append(result_dict)
        # pprint.pprint(result_dict)

    x = tmp_list[0]

    for y in tmp_list[1:]:
        x = {k: list(map(operator.add,
                          y.get(k, 0),
                          x.get(k, 0),
                        )
                    ) for k in set(x)}
        # print x

    date_list = [curr_date for curr_date in datetime_generator(start_date, end_date, datetime.timedelta(days=1))]
    for key, value in x.iteritems():
        x[key] = zip(date_list, value)
    return x



if __name__ == "__main__":

    #Construct the raw CSV file list, namely:
    # [
    #   '/Users/qsong/Documents/TracesAnalyzer/log/comparison_time_liege.csv',
    #   '/Users/qsong/Documents/TracesAnalyzer/log/comparison_time_temple.csv',
    #   '/Users/qsong/Documents/TracesAnalyzer/log/comparison_time_ucl.csv',
    #   '/Users/qsong/Documents/TracesAnalyzer/log/comparison_time_umass.csv',
    #   '/Users/qsong/Documents/TracesAnalyzer/log/comparison_time_wiilab.csv'
    # ]
    # VP_LIST is variable imported from config/config.py
    rawCSV_files = [os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp_name)) for vp_name in VP_LIST]

    # Indicate the start datetime and the end datetime
    START_TIME = datetime.datetime(2013, 7, 2, 0, 0) # namley 2013/07/02
    END_TIME = datetime.datetime(2013, 7, 18, 0, 0) # namley 2013/07/18

    pprint.pprint(avergae_statistics(rawCSV_files, START_TIME, END_TIME))










