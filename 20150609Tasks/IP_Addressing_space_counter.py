# -*- coding: utf-8 -*-
__author__ = 'yueli'

import os
import timeit
import re
from config.config import *
import datetime
from netaddr import *
import pprint
import logging


# 此脚本用来查看指定某天的IP Addressing Space个数

# 定义一个method，input为指定的csv file和指定的时间范围，output为在此时间范围内可以得到的所有mapping entry(prefix)
def prefix_finder_given_time(csv_file, given_date):
    prefix_given_time = []

    with open(csv_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果是RoundNoReply则没有必要处理此行
            if tmp_list[LOG_COLUMN['round_type']] != 'RoundNoReply':

                # 在指定时间范围内进行处理
                if re.search(given_date, tmp_list[LOG_COLUMN['date']]):
                    # print tmp_list[LOG_COLUMN['date']], tmp_list[LOG_COLUMN['mapping_entry']]
                    prefix_given_time.append(tmp_list[LOG_COLUMN['mapping_entry']])

    # print "method", [prefix_tmp for prefix_tmp in set(prefix_given_time)]
    return [prefix_tmp for prefix_tmp in set(prefix_given_time)]


# 定义一个method，调用netaddr里的cidr_merge函数，可以merge所给的所有prefix_list
# input为prefix_list，output为merge过的smallest possible list of CIDR subnets
def merge_all_prefixes(prefix_list):

    IP_network_list = [IPNetwork(prefix_tmp) for prefix_tmp in prefix_list]
    logger.debug("IP_network_list: {0}".format(IP_network_list))

    return cidr_merge(IP_network_list)




# Main
if __name__ == '__main__':
    start_time = timeit.default_timer()

    logging.basicConfig(
        filename=os.path.join(os.getcwd(), '{0}.log'.format(__file__)),
        level=logging.INFO,
        filemode='w',
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    logger = logging.getLogger(__name__)

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


    given_date_list = ["2013-07-02", "2013-07-18"]

    for given_date in given_date_list:
        prefix_list_given_time_tmp = []
        for vp in VP_LIST:
            # 遍历此vp下的所有csv file
            for file_name in os.listdir(os.path.join(PLANET_CSV_DIR, vp)):
                csv_file = os.path.join(PLANET_CSV_DIR, vp, file_name)
                logger.debug(csv_file)

                # 得到了所有文件路径和given_time之后即可调用prefix_finder_given_time(csv_file, given_date)来获得prefix_list
                prefix_list_given_time_tmp.extend(prefix_finder_given_time(csv_file, given_date))
                logger.debug(prefix_list_given_time_tmp)


            # 将得到的prefix_list_given_time_tmp取set，以消除重复项
            prefix_list_given_time = [prefix_tmp for prefix_tmp in set(prefix_list_given_time_tmp)]
            # 调用merge_all_prefixes method，用python自带包 netaddr 里的 cidr_merge()得到可能的最小的subnet
            merged_prefix_list_given_time = merge_all_prefixes(prefix_list_given_time)
            logger.debug("There are {0} CIDR subnets in {1}".format(len(merged_prefix_list_given_time), vp))
            logger.debug(merged_prefix_list_given_time)
            print "There are {0} CIDR subnets in {1}".format(len(merged_prefix_list_given_time), vp)
            pprint.pprint(merged_prefix_list_given_time)




    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
    logger.debug("Execution time (in unit of second) of this script: {0}".format(stop_time - start_time))