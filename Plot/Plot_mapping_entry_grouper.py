# -*- coding: utf-8 -*-
__author__ = 'yueli'

import numpy as np
import matplotlib.pyplot as plt
from config.config import *
import timeit
import re
import datetime

# Import the targeted raw CSV file, and store them in the rawCSV_file_list
rawCSV_file_list = []
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.58.0-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.58.64-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.58.128-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.59.0-MR-149.20.48.61.log.csv"))

rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.216-MR-149.20.48.61.log.csv"))
rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.217-MR-149.20.48.61.log.csv"))
rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.218-MR-149.20.48.61.log.csv"))
rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.220-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.17.224-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.17.228-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.30.160-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.30.164-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.30.176-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.44.112-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.44.120-MR-149.20.48.61.log.csv"))

print rawCSV_file_list

# Define a function to get the longest Time list from the CSV file list
def getTime(rawCSV_file_list):
    time = []
    for rawCSV_file in rawCSV_file_list:
        with open(rawCSV_file) as f_handler:
            next(f_handler)
            for line in f_handler:
                tmp_list = line.split(';')
                if tmp_list[1] not in time:
                    time.append(tmp_list[1])

    return sorted(time)


# 定义一个方法，使其可以记录每个文件想要的数据作为plot时的y值
def getYAxisValue(timeXAxis, rawCSV_file, index_value):
    negativeReply_list = []
    normalReply_list = []
    for i in range(len(timeXAxis)):
        negativeReply_list.append(-1)
        normalReply_list.append(-1)

    with open(rawCSV_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')
            # 找出此时刻在timeXAxis中存储的下标，使得negativeReply_list和normalReply_list可以在相应位置上存储Y轴的值
            time_index = timeXAxis.index(tmp_list[1])
            # 如果此时刻结果为NegativeReply，则negativeReply_list和normalReply_list均需添加无用信息值以占位，使得plot时维度相等
            if tmp_list[0] == 'RoundNoReply':
                negativeReply_list[time_index] = -1
                normalReply_list[time_index] = -1
            else:
                # 如果此时刻结果为NegativeReply则negativeReply_list添加相关的最后可以plot出的数据值
                if tmp_list[0] == 'NegativeReply':
                    negativeReply_list[time_index] = index_value
                    normalReply_list[time_index] = -1
                else:
                    normalReply_list[time_index] = index_value
                    negativeReply_list[time_index] = -1

    return negativeReply_list, normalReply_list


# 定义一个方法，使得可以得到当前绘图时用到的所有EID，用一个list储存起来
def getEID_list():
    EID_list = []
    pattern = r"EID-\d+.\d+.\d+.\d+"
    for rawCSV_file in rawCSV_file_list:
        EID_list.append(re.search(pattern, rawCSV_file).group())

    return EID_list



if __name__ == '__main__':
    # 记录程序起始时间
    start_time = timeit.default_timer()

    # All available marker styles are introduced in this webpage:
    # http://matplotlib.org/api/markers_api.html
    marker_styles = ['o', '*', '+', 'x', 's', 'q', '1', '2', '3', '4']


    # 画图时作为X轴的时间
    timeXAxis = getTime(rawCSV_file_list)

    i = 1
    for rawCSV_file in rawCSV_file_list:
        negativeValue_list = []
        normalValue_list = []
        negativeValue_list, normalValue_list = getYAxisValue(timeXAxis, rawCSV_file, i)
        i = i + 1

        plt.scatter(range(len(timeXAxis)), negativeValue_list, color = 'blue')
        plt.scatter(range(len(timeXAxis)), normalValue_list, color = 'green', marker='*')




    for rawCSV_file in rawCSV_file_list:
        with open(rawCSV_file) as f_handler:
            next(f_handler)
            for line in f_handler:
                tmp_list = line.split(";")
                # The data structure "LOG_COLUMN" is defined in file: config.py
                if tmp_list[LOG_COLUMN['type']] != 'RoundNoReply':
                    round_dict = {
                        'type'      : tmp_list[LOG_COLUMN['type']],
                        # Convert datetime of format string into a Datetime type object, and
                        # gard just year, month, day, hour, minutes.
                        'datetime'  : datetime.datetime.strptime(tmp_list[LOG_COLUMN['date']], "%Y-%m-%d %H:%M:%S")


                    }



    plt.xlim(0, len(timeXAxis))
    plt.ylim(0, i)
    plt.xlabel('Experiment number')
    plt.yticks(range(1,len(getEID_list())+1,1), getEID_list())

    plt.show()



    # 记录程序终止时间，用差可算出程序实际运行时间
    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time

# plt.annotate('mapping_entry/prefix',xy=(0,2.03),xytext=(0,2.1),arrowprops=dict(arrowstyle="->"))
