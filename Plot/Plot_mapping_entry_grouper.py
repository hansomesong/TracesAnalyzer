# -*- coding: utf-8 -*-
__author__ = 'yueli'

import numpy as np
import matplotlib.pyplot as plt
from config.config import *
import timeit
import re

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


# 定义一个方法，使得可以得到当前绘图时用到的所有需用箭头标记出来的不同的mapping_entry，
# 返回值为list的list，内层list=[mapping_entry,experiment number,y轴值]，
# 外层list变量为不同的mapping_entry
def getMappingEntry_list(timeXAxis, rawCSV_file, index_value):
    mappingEntry_list = []
    with open(rawCSV_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')
            if tmp_list[0] != 'RoundNoReply':
                if tmp_list[10] not in [a[0] for a in mappingEntry_list]:
                    mappingEntry_list.append([tmp_list[10], timeXAxis.index(tmp_list[1]), index_value])

    return mappingEntry_list




if __name__ == '__main__':
    # 记录程序起始时间
    start_time = timeit.default_timer()


    # 画图时作为X轴的时间
    timeXAxis = getTime(rawCSV_file_list)

    # 此处循环plot出整体，negativeMapReply用蓝线表示，normalReply用绿线表示
    i = 1
    for rawCSV_file in rawCSV_file_list:
        negativeValue_list = []
        normalValue_list = []
        negativeValue_list, normalValue_list = getYAxisValue(timeXAxis, rawCSV_file, i)
        plt.scatter(range(len(timeXAxis)), negativeValue_list, color = 'blue')
        plt.scatter(range(len(timeXAxis)), normalValue_list, color = 'green')
        i = i + 1



    # 此处循环为给不同的mappingEntry变化时标注出来，打上箭头，
    # 并且避免了由于X轴间距太小而annotaion被重叠在一起打印出来的情况
    j = 1
    for rawCSV_file in rawCSV_file_list:
        mappingEntry_list = getMappingEntry_list(timeXAxis, rawCSV_file, j)
        # 添加一个新变量，in the case of 不同mappingEntry离得太近，会发生标注重叠现象
        annotation_distance = 0
        more_than_one_time_flag = 0
        for mappingEntry in mappingEntry_list:
            # 第一次加注释开始
            if more_than_one_time_flag == 0:
                plt.annotate(mappingEntry[0], xy=(mappingEntry[1],mappingEntry[2]+0.04),
                         xytext=(mappingEntry[1],mappingEntry[2]+0.3),arrowprops=dict(arrowstyle="->"))
                more_than_one_time_flag = more_than_one_time_flag + 1
                time_tmp = mappingEntry[1]
                # 为下一次标注重合移动Y轴坐标做准备
                annotation_distance = annotation_distance + 0.2
            # 第二次以后加注释开始
            else:
                # 如果此标注起始位置与上一次相差大于等于200，则标注的Y周坐标不用变更
                if (mappingEntry[1] - time_tmp) >= 200:
                    plt.annotate(mappingEntry[0], xy=(mappingEntry[1],mappingEntry[2]+0.04),
                             xytext=(mappingEntry[1],mappingEntry[2]+0.3),arrowprops=dict(arrowstyle="->"))
                    more_than_one_time_flag = more_than_one_time_flag + 1
                    time_tmp = mappingEntry[1]
                # 如果此标注起始位置与上一次相差小于200，则标注的Y周坐标需要有上调或下降的变更
                else:
                    plt.annotate(mappingEntry[0], xy=(mappingEntry[1],mappingEntry[2]+0.04),
                                 xytext=(mappingEntry[1],mappingEntry[2]+0.3+annotation_distance),
                                 arrowprops=dict(arrowstyle="->"))
                    annotation_distance = annotation_distance - 0.2
                    more_than_one_time_flag = more_than_one_time_flag + 1

        j = j + 1




    plt.xlim(0, len(timeXAxis))
    plt.ylim(0, i)
    plt.xlabel('Experiment number')
    plt.yticks(range(1,len(getEID_list())+1,1), getEID_list())



    # 记录程序终止时间，用差可算出程序实际运行时间
    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
    plt.show()


