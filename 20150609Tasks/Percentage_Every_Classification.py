# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 本脚本用来统计实验开始的第一天&最后一天，classification里共7个subcase的percentage分别是多少

from config.config import *
import os
import timeit
import re


# 此方法用于统计第Q列为1的行数即文件个数，然后进一步判断有多少是在1st day就有变化的，
# 返回属于此情况的行数，文件数
def numbers_case1(csv_file):
    numbers_case1_1st_day = 0
    numbers_case1_18th_day = 0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果csv文件第Q列为1，则表示该文件属于case1的变化
            if tmp_list[16] == '1':
                # 如果csv文件第O列为'02/07/2013'，则表示该文件的case1的变化在第一天发生过
                if re.findall('02/07/2013', tmp_list[14]):
                    numbers_case1_1st_day = numbers_case1_1st_day + 1
                # 如果csv文件第O列为'18/07/2013'，则表示该文件的case1的变化在最后一天发生过
                elif re.findall('18/07/2013', tmp_list[14]):
                    numbers_case1_18th_day = numbers_case1_18th_day + 1

    return numbers_case1_1st_day, numbers_case1_18th_day



# 此方法用于统计第Q列为3的行数即文件个数，然后进一步判断有多少是在1st day就有变化的，
# 返回属于此情况的行数，文件数
def numbers_case3_1st_day(csv_file):

    with open(csv_file) as f_handler:
        next(f_handler)

    return True



# 此方法用于统计第Q列为4的行数即文件个数，然后进一步判断有多少是在1st day就有变化的，
# 返回属于此情况的行数，文件数
def numbers_case4_1st_day(csv_file):

    with open(csv_file) as f_handler:
        next(f_handler)

    return True



# 此方法用于统计参与第一天实验的总文件数
# 待定是否需要此方法！！因为可以在main中直接把case1-4的文件数相加！！
def numbers_total_cases():


    return True


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


    vp_list = ["liege", "temple", "ucl", "umass", "wiilab"]
    numbers_case1_1st_day_list = []
    numbers_case1_18th_day_list = []

    # 遍历5个vp，统计各个case的个数
    for vp in vp_list:
        numbers_case1_1st_day, numbers_case1_18th_day = numbers_case1(
            os.path.join(CSV_FILE_DESTDIR, "comparison_time_{0}.csv".format(vp)))


        numbers_case1_1st_day_list.append(numbers_case1_1st_day)
        numbers_case1_18th_day_list.append(numbers_case1_18th_day)

    print "numbers_case1_1st_day_list:", numbers_case1_1st_day_list
    print "numbers_case1_18th_day_list:", numbers_case1_18th_day_list



    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time