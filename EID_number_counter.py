# -*- coding: utf-8 -*-
__author__ = 'yueli'

import os
import timeit
import re
from config.config import *
import matplotlib.pyplot as plt




def find_target_log_file(targetDir):
    file_path_lists = []
    for raw_file_lists in os.listdir(targetDir):
        if re.search('EID4_list_2013-07-\d+.txt', raw_file_lists):
            file_path_lists.append(os.path.join(targetDir, raw_file_lists))

    return file_path_lists


# 定义一个可以从13个MR中找出回复数量最多的那个MR
def select_MR_most_response(targetCSVFile):
    eid_current = "0.0.0.0"
    reply_number_most = 0
    target_csv_file = []

    with open(targetCSVFile) as f_handler:
        next(f_handler)
        target_csv_file_tmp = []
        for line in f_handler:
            tmp_list = line.split(';')
            reply_number_current = sum([int(b) for b in re.findall("\d+", re.sub( "'\d+.\d+.\d+.\d+\/\d+', ", '', tmp_list[4]))])

            # 如果当前的 EID 和记录的EID一致，即在13个MR之内，那么 mapping entry 出现的数量最多的则是要找的目标file
            if tmp_list[2] == eid_current:
                if reply_number_current > reply_number_most:
                    reply_number_most = reply_number_current
                    target_csv_file_tmp.append(tmp_list[1])
            # 如果当前的 EID 和记录的EID不一致了，那说明此时已更换新的EID，那么 eid_current 和 reply_number_most 都要随之更新
            else:
                eid_current = tmp_list[2]
                reply_number_most = reply_number_current
                target_csv_file.append(target_csv_file_tmp[-1])
                target_csv_file_tmp.append(tmp_list[1])
        target_csv_file.append(target_csv_file_tmp[-1])


    return target_csv_file


# 定义一个可以把所有采样点的 Mapping Response 都记录下来的方法
def get_num_different_response(rawCSVFile):
    num_different_response = {}
    with open(rawCSVFile) as f_handler:
        next(f_handler)




if __name__ == '__main__':
    start_time = timeit.default_timer()
    # 读取环境变量 ‘PROJECT_LOG_DIR’ (此变量定义在工作目录下.profile或者.bashprofile)
    try:
        PLANET_DIR = os.environ['PLANETLAB']
        CSV_FILE_DESTDIR = os.environ['PROJECT_LOG_DIR']
    except KeyError:
        print "Environment variable PROJECT_LOG_DIR is not properly defined or " \
              "the definition about this variable is not taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"

    # 此部分用于统计已有的txt文档里直接存储的EID个数／天，针对5个vantage point都有统计，以列表形式存储每个VP的EID个数
    vp_list = ["liege", "temple", "ucl", "umass", "wiilab"]
    for vp in vp_list:
        Y_vp = []
        for target_file in find_target_log_file(os.path.join(PLANET_DIR, vp, "eid")):
            with open(target_file) as f_handler:
                file_list = []
                for line in f_handler:
                    file_list.append(line)

            Y_vp.append(len(file_list))
        print Y_vp



    # 此部分由于统计每天不同回复类型的EID个数，判断标准为：
    # 1. 在13个MR中选取 response 数最多的 MR 为统计对象，这样可以避免13个MR针对同一EID有不同 response 的情况
    # 2. 选择一个 échantillon par jour, e.g.,  midi de chaque jour 作为采样点，这样可以避免出现一天中回复有所变化的情况

    print select_MR_most_response(os.path.join(CSV_FILE_DESTDIR, "comparison_time_liege.csv"))







    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time