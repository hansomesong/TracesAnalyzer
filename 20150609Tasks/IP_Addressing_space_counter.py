# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 此脚本用来查看指定某天的IP Addressing Space个数
# 性能优化测试：
# 测试平台： MacAir 2014 4G RAM, 128G SSD硬盘
# 参考指标： 优化前对 wiilab的测试结果为，89 seconds
# 优化手段1：将re.search()函数直接替换为 string equability test, 速度提升至74 seconds
# 优化手段2：将logger记录信息的level变为INFO，速度继续提升至 64 seconds


import timeit
import re
from config.config import *
from netaddr import *
import pprint
import logging
import numpy as np
import matplotlib.pyplot as plt


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
                # S. 直接比较 两个字符串是否相等，速度要优于 re.serach()方法
                if given_date == tmp_list[LOG_COLUMN['date']].split(' ')[0] and \
                        (IPAddress(tmp_list[LOG_COLUMN['eid']]) in IPNetwork(tmp_list[LOG_COLUMN['mapping_entry']])):
                    # print tmp_list[LOG_COLUMN['date']], tmp_list[LOG_COLUMN['mapping_entry']]
                    prefix_given_time.append(tmp_list[LOG_COLUMN['mapping_entry']])

    logger.debug('In method prefix_finder_given_time, set(prefix) = {0}'.format([prefix_tmp for prefix_tmp in set(prefix_given_time)]))
    return [prefix_tmp for prefix_tmp in set(prefix_given_time)]


# 定义一个method，调用netaddr里的cidr_merge函数，可以merge所给的所有prefix_list
# input为prefix_list，output为merge过的smallest possible list of CIDR subnets
def merge_all_prefixes(prefix_list):

    IP_network_list = [IPNetwork(prefix_tmp) for prefix_tmp in prefix_list]
    logger.debug("IP_network_list: {0}".format(IP_network_list))

    return cidr_merge(IP_network_list)



# 此method可以统计出每一个类似于 IPNetwork('37.77.56.48/28')的prefix下有多少个IP地址，即2的(32-28)次方个IP地址
# 在 netaddr中调用 IPNetwork('37.77.56.48/28').size 即可
# input为已经merge过的smallest possible subnets 的list，逐一统计出每个prefix的size，然后求合
# output即为在某一vp下，一共有多少个可用IP地址
def prefix_size(merged_prefix_list):
    prefix_size_total = 0
    for prefix in merged_prefix_list:
        prefix_size_total = prefix_size_total + prefix.size

    return prefix_size_total



# Main
if __name__ == '__main__':
    start_time = timeit.default_timer()

    logging.basicConfig(
        filename=os.path.join(os.getcwd(), '{0}.log'.format(__file__)),
        level=logging.DEBUG,
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
    prefix_size_dic = {}

    for given_date in given_date_list:
        prefix_size_dic[given_date] = {}
        prefix_list_given_time_tmp = []
        for vp in VP_LIST:
            # 打开5个comparison_time_vp.csv先进行第一次筛选，如果某一行只有No Map Reply就没有必要再打开那个log文件了
            with open(os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))) as f_handler:
                next(f_handler)
                for line in f_handler:
                    tmp_list = line.split(';')

                    # 如果是RoundNoReply则没有必要处理此行
                    if tmp_list[LOG_TIME_COLUMN['round_type_set']] != 'RoundNoReply':
                        csv_file = os.path.join(PLANET_CSV_DIR, vp, '{0}-EID-{1}-MR-{2}.log.csv'.format(LOG_PREFIX[vp],
                                                                                                        tmp_list[LOG_TIME_COLUMN['eid']], tmp_list[LOG_TIME_COLUMN['resolver']]))

                        logger.debug(csv_file)
                        prefix_list_given_time_tmp.extend(prefix_finder_given_time(csv_file, given_date))
                        logger.debug('prefix_list_given_time_tmp ----> {0}'.format(prefix_list_given_time_tmp))


            # # 遍历此vp下的所有csv file (已被上面一段code顶替)
            # for file_name in os.listdir(os.path.join(PLANET_CSV_DIR, vp)):
            #     csv_file = os.path.join(PLANET_CSV_DIR, vp, file_name)
            #     logger.debug(csv_file)
            #
            #     # 得到了所有文件路径和given_time之后即可调用prefix_finder_given_time(csv_file, given_date)来获得prefix_list
            #     prefix_list_given_time_tmp.extend(prefix_finder_given_time(csv_file, given_date))
            #     logger.debug('prefix_list_given_time_tmp ----> {0}'.format(prefix_list_given_time_tmp))


            # 将得到的prefix_list_given_time_tmp取set，以消除重复项
            prefix_list_given_time = [prefix_tmp for prefix_tmp in set(prefix_list_given_time_tmp)]
            # 调用merge_all_prefixes method，用python自带包 netaddr 里的 cidr_merge()得到可能的最小的subnet
            merged_prefix_list_given_time = merge_all_prefixes(prefix_list_given_time)
            logger.debug("There are {0} CIDR subnets in {1}".format(len(merged_prefix_list_given_time), vp))
            logger.debug(merged_prefix_list_given_time)
            print "There are {0} CIDR subnets in {1}".format(len(merged_prefix_list_given_time), vp)
            pprint.pprint(merged_prefix_list_given_time)

            # 计算给定的一组merged list of prefixes，去求它们size的总和
            prefix_size_dic[given_date][vp] = prefix_size(merged_prefix_list_given_time)
            print 'prefix_size_dic[', given_date, '][', vp, '] ='
            pprint.pprint(prefix_size_dic[given_date][vp])
            logger.debug('prefix_size_dic[{0}][{1}] = {2}'.format(given_date, vp, prefix_size_dic[given_date][vp]))



    # Modify the size and dpi of picture, default size is (8,6), default dpi is 80
    plt.gcf().set_size_inches(8,6)
    plt.gcf().set_dpi(300)

    # 此处开始画图，input应当为上段代码的输出，但为加速直接把数据输入
    n_groups = 5

    ip_addr_number_1st_day = (40.57, 40.73, 40.73, 40.73, 40.73)
    ip_addr_number_18th_day = (37.54, 37.74, 40.27, 37.70, 37.70)
    prefix_number_1st_day = (17.3, 17.3, 17.3, 17.3, 17.3)
    prefix_number_18th_day = (20.7, 20.8, 20.6, 20.7, 20.7)

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.2

    rects1 = plt.bar(index, prefix_number_1st_day, bar_width, color='blue',label= 'aggregated prefixes')
    rects2 = plt.bar(index + bar_width, ip_addr_number_1st_day, bar_width, color='yellow',label= 'covered IP space')
    rects3 = plt.bar(index + 2*bar_width, prefix_number_18th_day, bar_width, color='blue')
    rects4 = plt.bar(index + 3*bar_width, ip_addr_number_18th_day, bar_width, color='yellow')

    plt.xlabel('vantage point', fontsize=28)
    # plt.ylabel('number', fontsize=28)
    # plt.title('Prefix number and possible IP address number')
    plt.xticks(index + 2*bar_width, index + 1)
    plt.yticks(10*index, ['', '', '200', '', '4*10exp10'], fontsize=18)
    plt.xlim(0, 4+4*bar_width)
    plt.ylim(0, 50)
    plt.legend()
    # plt.savefig(os.path.join(PLOT_DIR, 'Prefix_and_IP_addr_number.eps'),
    #             dpi=300)
    plt.show()

    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
    logger.debug("Execution time (in unit of second) of this script: {0}".format(stop_time - start_time))