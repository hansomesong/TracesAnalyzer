# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 本脚本用来统计实验开始的第一天&最后一天，classification里共7个subcase的percentage分别是多少

from config.config import *
import os
import timeit
import re


# 此方法用于统计第'case'列为1的行数即文件个数，然后进一步判断有多少是在1st day就有变化的，
# 返回属于此情况的行数，文件数
def numbers_case1(csv_file):
    numbers_case1_1st_day = 0
    numbers_case1_18th_day = 0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果csv文件'case'列为为1，则表示该文件属于case1的变化
            if tmp_list[LOG_TIME_COLUMN['case']] == '1':
                # 如果csv文件'case1_change_time'列为'02/07/2013'，则表示该文件的case1的变化在第一天发生过
                if re.findall('02/07/2013', tmp_list[LOG_TIME_COLUMN['case1_change_time']]):
                    numbers_case1_1st_day = numbers_case1_1st_day + 1
                # 如果csv文件'case1_change_time'列为'18/07/2013'，则表示该文件的case1的变化在最后一天发生过
                elif re.findall('18/07/2013', tmp_list[LOG_TIME_COLUMN['case1_change_time']]):
                    numbers_case1_18th_day = numbers_case1_18th_day + 1

    return numbers_case1_1st_day, numbers_case1_18th_day



# 此方法用于统计第'case'列为3的行数即文件个数，然后进一步判断有多少是在1st day就有变化的，
# 返回属于此情况的行数，文件数
def numbers_case3(csv_file):
    numbers_case3_1st_day = 0
    numbers_case3_18th_day = 0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果csv文件'case'列为3，则表示该文件属于case3的变化
            if tmp_list[LOG_TIME_COLUMN['case']] == '3':
                # 如果csv文件'case3_4_change_time'列为'02/07/2013'，则表示该文件的case3的变化在第一天发生过
                if re.findall('02/07/2013', tmp_list[LOG_TIME_COLUMN['case3_4_change_time']]):
                    numbers_case3_1st_day = numbers_case3_1st_day + 1
                # 如果csv文件'case3_4_change_time'列为'18/07/2013'，则表示该文件的case3的变化在最后一天发生过
                elif re.findall('18/07/2013', tmp_list[LOG_TIME_COLUMN['case3_4_change_time']]):
                    numbers_case3_18th_day = numbers_case3_18th_day + 1

    return numbers_case3_1st_day, numbers_case3_18th_day



# 此方法用于统计第'case'列为4的行数即文件个数，然后进一步判断有多少是在1st day就有变化的，
# 返回属于此情况的行数，文件数
def numbers_case4(csv_file):
    numbers_case4_1st_day = 0
    numbers_case4_18th_day = 0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果csv文件'case'列为4，则表示该文件属于case4的变化
            if tmp_list[LOG_TIME_COLUMN['case']] == '4':
                # 如果csv文件'case3_4_change_time'列为'02/07/2013'，则表示该文件的case4的变化在第一天发生过
                if re.findall('02/07/2013', tmp_list[LOG_TIME_COLUMN['case3_4_change_time']]):
                    numbers_case4_1st_day = numbers_case4_1st_day + 1
                # 如果csv文件'case3_4_change_time'列为'18/07/2013'，则表示该文件的case4的变化在最后一天发生过
                elif re.findall('18/07/2013', tmp_list[LOG_TIME_COLUMN['case3_4_change_time']]):
                    numbers_case4_18th_day = numbers_case4_18th_day + 1

    return numbers_case4_1st_day, numbers_case4_18th_day



# 把所有属于case1的文件数都统计出来，用于验证
def numbers_case1_all_days(csv_file):
    numbers_case1_all_days = 0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果csv文件'case'列为1，则表示该文件属于case1的变化
            if tmp_list[LOG_TIME_COLUMN['case']] == '1':
                numbers_case1_all_days = numbers_case1_all_days + 1

    return numbers_case1_all_days


# 把所有属于case3的文件数都统计出来，用于验证
def numbers_case3_all_days(csv_file):
    numbers_case3_all_days = 0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果csv文件'case'列为3，则表示该文件属于case3的变化
            if tmp_list[LOG_TIME_COLUMN['case']] == '3':
                numbers_case3_all_days = numbers_case3_all_days + 1

    return numbers_case3_all_days


# 把所有属于case4的文件数都统计出来，用于验证
def numbers_case4_all_days(csv_file):
    numbers_case4_all_days = 0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果csv文件'case'列为4，则表示该文件属于case4的变化
            if tmp_list[LOG_TIME_COLUMN['case']] == '4':
                numbers_case4_all_days = numbers_case4_all_days + 1

    return numbers_case4_all_days



# Main
if __name__ == '__main__':
    start_time = timeit.default_timer()
    # 读取环境变量 ‘PROJECT_LOG_DIR’ (此变量定义在工作目录下.profile或者.bashprofile)
    try:
        PLANET_DIR = os.environ['PLANETLAB']
        CSV_FILE_DESTDIR = os.environ['PROJECT_LOG_DIR']
        PLANET_CSV_DIR = os.environ['PLANETLAB_CSV']
        PLOT_DIR = os.environ['PROJECT_PLOT_DIR']
    except KeyError:
        print "Environment variable PROJECT_LOG_DIR is not properly defined or " \
              "the definition about this variable is not taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"


    # 为每一个case各初始化2个list，分别用来存储某个case某一天的变化次数
    numbers_case1_1st_day_list = []
    numbers_case1_18th_day_list = []
    numbers_case3_1st_day_list = []
    numbers_case3_18th_day_list = []
    numbers_case4_1st_day_list = []
    numbers_case4_18th_day_list = []

    # 遍历5个vp，统计各个case的个数
    for vp in VP_LIST:
        # 统计出Case1的1st day和18th day，5个VP里各自的变化个数
        numbers_case1_1st_day, numbers_case1_18th_day = numbers_case1(
            os.path.join(CSV_FILE_DESTDIR, "comparison_time_{0}.csv".format(vp)))
        numbers_case1_1st_day_list.append(numbers_case1_1st_day)
        numbers_case1_18th_day_list.append(numbers_case1_18th_day)

        numbers_case3_1st_day, numbers_case3_18th_day = numbers_case3(
            os.path.join(CSV_FILE_DESTDIR, "comparison_time_{0}.csv".format(vp)))
        numbers_case3_1st_day_list.append(numbers_case3_1st_day)
        numbers_case3_18th_day_list.append(numbers_case3_18th_day)

        numbers_case4_1st_day, numbers_case4_18th_day = numbers_case4(
            os.path.join(CSV_FILE_DESTDIR, "comparison_time_{0}.csv".format(vp)))
        numbers_case4_1st_day_list.append(numbers_case4_1st_day)
        numbers_case4_18th_day_list.append(numbers_case4_18th_day)

        print "Case1 total ->", numbers_case1_all_days(
            os.path.join(CSV_FILE_DESTDIR, "comparison_time_{0}.csv".format(vp)))

        print "Case3 total ->", numbers_case3_all_days(
            os.path.join(CSV_FILE_DESTDIR, "comparison_time_{0}.csv".format(vp)))

        print "Case4 total ->", numbers_case4_all_days(
            os.path.join(CSV_FILE_DESTDIR, "comparison_time_{0}.csv".format(vp)))


    # For 1st day, 给每一个list求和，即算出某一Case在1st day5个VP的变化总数
    sum_num_case1_1st_day = float(sum(numbers_case1_1st_day_list))
    print "sum_num_case1_1st_day_list:", sum_num_case1_1st_day
    sum_num_case3_1st_day = float(sum(numbers_case3_1st_day_list))
    print "sum_num_case3_1st_day:", sum_num_case3_1st_day
    sum_num_case4_1st_day = float(sum(numbers_case4_1st_day_list))
    print "sum_num_case4_1st_day:", sum_num_case4_1st_day

    # 5个VP的Case1,3,4在1st day变化数的总和
    sum_1st_day = sum_num_case1_1st_day + sum_num_case3_1st_day + sum_num_case4_1st_day
    # 计算每个case的percentage
    percentage_case1_1st_day = sum_num_case1_1st_day / sum_1st_day * 100
    print "percentage_case1_1st_day =", percentage_case1_1st_day
    percentage_case3_1st_day = sum_num_case3_1st_day / sum_1st_day * 100
    print "percentage_case3_1st_day =", percentage_case3_1st_day
    percentage_case4_1st_day = sum_num_case4_1st_day / sum_1st_day * 100
    print "percentage_case4_1st_day =", percentage_case4_1st_day


    # For 18th day, 给每一个list求和，即算出某一Case在18th day5个VP的变化总数
    sum_num_case1_18th_day = float(sum(numbers_case1_18th_day_list))
    print "sum_num_case1_18th_day:", sum_num_case1_18th_day
    sum_num_case3_18th_day = float(sum(numbers_case3_18th_day_list))
    print "numbers_case3_18th_day_list:", sum_num_case3_18th_day
    sum_num_case4_18th_day = float(sum(numbers_case4_18th_day_list))
    print "numbers_case4_18th_day_list:", sum_num_case4_18th_day

    # 5个VP的Case1,3,4在18th day变化数的总和
    sum_18th_day = sum_num_case1_18th_day + sum_num_case3_18th_day + sum_num_case4_18th_day
    # 计算每个case的percentage
    percentage_case1_18th_day = sum_num_case1_18th_day / sum_18th_day * 100
    print "percentage_case1_18th_day =", percentage_case1_18th_day
    percentage_case3_18th_day = sum_num_case3_18th_day / sum_18th_day * 100
    print "percentage_case3_18th_day =", percentage_case3_18th_day
    percentage_case4_18th_day = sum_num_case4_18th_day / sum_18th_day * 100
    print "percentage_case4_18th_day =", percentage_case4_18th_day





    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time