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

# liege
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.58.0-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.58.64-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.58.128-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-37.77.59.0-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.216-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.217-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.218-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.22.220-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.17.224-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.17.228-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.30.160-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.30.164-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.30.176-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.44.112-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.44.120-MR-149.20.48.61.log.csv"))


# temple
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-37.77.58.0-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-37.77.58.64-MR-149.20.48.61.log.csv "))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-37.77.58.128-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-37.77.59.0-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.22.216-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.22.217-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.22.218-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.22.220-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.17.224-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.17.228-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.30.160-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.30.164-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.30.176-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.44.112-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.44.120-MR-149.20.48.61.log.csv"))

# ucl
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-37.77.58.0-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-37.77.58.64-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-37.77.58.128-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-37.77.59.0-MR-149.20.48.61.log.csv"))

# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.22.216-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.22.217-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.22.218-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.22.220-MR-149.20.48.61.log.csv"))

rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.17.224-MR-149.20.48.61.log.csv"))
rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.17.228-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.30.160-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.30.164-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.30.176-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.44.112-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.44.120-MR-149.20.48.61.log.csv"))


# umass
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-37.77.58.0-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-37.77.58.64-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-37.77.58.128-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-37.77.59.0-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.22.216-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.22.217-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.22.218-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.22.220-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.17.224-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.17.228-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.30.160-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.30.164-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.30.176-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.44.112-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.44.120-MR-149.20.48.61.log.csv"))


# wiilab
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-37.77.58.0-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-37.77.58.64-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-37.77.58.128-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-37.77.59.0-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.22.216-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.22.217-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.22.218-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.22.220-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.17.224-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.17.228-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.30.160-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.30.164-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.30.176-MR-149.20.48.61.log.csv"))
#
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.44.112-MR-149.20.48.61.log.csv"))
# rawCSV_file_list.append(os.path.join(PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.44.120-MR-149.20.48.61.log.csv"))

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

def datetime2exp_number(date):
    return int((date-datetime.datetime(2013, 7, 2, 7, 30)).total_seconds()/1800+1)

# Generate a list of unique, distinct colors
import colorsys
def get_N_HexCol(N=5):

    colors=[]
    for i in np.arange(0., 360., 360. / N):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors



# 定一个方法，使得挑出最短的prefix的mapping_entry，从而作为plot的题目
def get_plot_title(rawCSV_file_list):
    # 初始化一个长度为32位的prefix，方便后面选出最短prefix长度的比较
    prefix_tmp = 32
    first_rawCSV_file = rawCSV_file_list[0]
    with open(first_rawCSV_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')
            if tmp_list[0] != "RoundNoReply":
                if int(re.sub( "\d+.\d+.\d+.\d+\/", '', tmp_list[10])) < prefix_tmp:
                    me_prefix_shortest = tmp_list[10]
                    prefix_tmp = int(re.sub( "\d+.\d+.\d+.\d+\/", '', tmp_list[10]))

    plot_title = "Mapping Entry - {0}".format(me_prefix_shortest)
    return plot_title




# Main
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
        plt.scatter(range(1, len(timeXAxis)+1), negativeValue_list, color='black', s=1)
        # print [y for y, x in enumerate(normalValue_list, 1) if x == 1]
        i += 1



    # 此for loop只为绘制RoundNormal类型的 点状图
    i = 1
    for rawCSV_file in rawCSV_file_list:
        # All available marker styles are introduced in this webpage:
        # http://matplotlib.org/api/markers_api.html
        marker_styles = ['o', '*', '+', 'x', 's', '1', '2', '3', '4', '8', '<', '>', '^', 'D', 'd']
        marker_styles.reverse()
        # Generate a list of distinct colors
        colors = get_N_HexCol(20)
        # Record whether a certain RLOC has appreared before and associate a pair of marker and color for plotting
        rloc_marker_dict = {}

        # open current CSV log file to process each round
        with open(rawCSV_file) as f_handler:
            next(f_handler)
            for line in f_handler:
                tmp_list = line.split(";")
                # The data structure "LOG_COLUMN" is defined in file: config.py
                # We are just interested in round whose type is "RoundNormal
                if tmp_list[LOG_COLUMN['type']] == 'RoundNormal':
                    # For line of type "RoundNormal", we need to record the column:
                    # datetime and rloc set, because datetime
                    date = datetime.datetime.strptime(
                        # It is strange that when I open CSV log file with Excel, the datetime column is in format of
                        # "%d/%m/%Y %H:%M:%S", but in format of "%Y-%m-%d %H:%M:%S" opened with vim.
                        # Actually, the format "%Y-%m-%d %H:%M:%S" works when parsing datetime string in CSV log file
                        # into datetime object, and I do not know why...
                        tmp_list[LOG_COLUMN['date']], "%Y-%m-%d %H:%M:%S"
                    ).replace(
                        # zero the second and millisecond filed of target datetime object
                        second=0, microsecond=0
                    )

                    # Remember that c
                    rlocs= "#".join(tmp_list[14:])

                    if rlocs not in rloc_marker_dict.keys():
                        rloc_marker_dict[rlocs] = (marker_styles.pop(), colors.pop())
                    marker_color_pair = rloc_marker_dict[rlocs]


                    print marker_color_pair, date, datetime2exp_number(date), rlocs
                    plt.scatter(datetime2exp_number(date), i, marker=marker_color_pair[0], color=marker_color_pair[1])
        i += 1

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
                plt.annotate(
                    mappingEntry[0],
                    xy=(mappingEntry[1],mappingEntry[2]+0.04),
                    xytext=(mappingEntry[1],mappingEntry[2]+0.3),
                    arrowprops=dict(arrowstyle="->")
                )
                more_than_one_time_flag += 1
                time_tmp = mappingEntry[1]
                # 为下一次标注重合移动Y轴坐标做准备
                annotation_distance += 0.2
            # 第二次以后加注释开始
            else:
                # 如果此标注起始位置与上一次相差大于等于200，则标注的Y周坐标不用变更
                if (mappingEntry[1] - time_tmp) >= 200:
                    plt.annotate(
                        mappingEntry[0],
                        xy=(mappingEntry[1], mappingEntry[2]+0.04),
                        xytext=(mappingEntry[1], mappingEntry[2]+0.3),
                        arrowprops=dict(arrowstyle="->")
                    )
                    more_than_one_time_flag += 1
                    time_tmp = mappingEntry[1]
                # 如果此标注起始位置与上一次相差小于200，则标注的Y周坐标需要有上调或下降的变更
                else:
                    plt.annotate(
                        mappingEntry[0],
                        xy=(mappingEntry[1], mappingEntry[2]+0.04),
                        xytext=(mappingEntry[1], mappingEntry[2]+0.3+annotation_distance),
                        arrowprops=dict(arrowstyle="->"))
                    annotation_distance -= 0.2
                    more_than_one_time_flag += 1

        j += 1

    plt.xlim(0, len(timeXAxis))
    plt.ylim(0, i)
    plt.xlabel('Experiment number')
    plt.yticks(range(1, len(getEID_list())+1, 1), getEID_list())

    plt.title(get_plot_title(rawCSV_file_list))



    # 记录程序终止时间，用差可算出程序实际运行时间
    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time

    plt.show()


