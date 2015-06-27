# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 此脚本用来查看指定某天的IP Addressing Space个数
# 性能优化测试：
# 测试平台： MacAir 2014 4G RAM, 128G SSD硬盘
# 参考指标： 优化前对 wiilab的测试结果为，89 seconds
# 优化手段1：将re.search()函数直接替换为 string equability test, 速度提升至74 seconds
# 优化手段2：将logger记录信息的level变为INFO，速度继续提升至 64 seconds
# 优化手段3：开一次文件处理多个日期，速度继续提高至近 35 seconds


import timeit
from config.config import *
from netaddr import *
import pprint
import logging

# 定义一个method，input为指定的csv file和指定的时间范围，output为在此时间范围内可以得到的所有mapping entry(prefix)
def prefix_finder_given_time(csv_file, given_date_list):
    # 输入感兴趣的date list, 返回字典，key分别为日期
    prefix_given_time = {}
    for element in given_date_list:
        # element 的形式 可能为 “2015-07-23”
        prefix_given_time[element] = []

    with open(csv_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 如果是RoundNoReply则没有必要处理此行
            if tmp_list[LOG_COLUMN['round_type']] != 'RoundNoReply':
                exp_date = tmp_list[LOG_COLUMN['date']].split(' ')[0]
                # 在指定时间范围内进行处理
                if exp_date in given_date_list:
                    if (IPAddress(tmp_list[LOG_COLUMN['eid']]) in IPNetwork(tmp_list[LOG_COLUMN['mapping_entry']])):
                        prefix_given_time[exp_date].append(tmp_list[LOG_COLUMN['mapping_entry']])

    logger.debug('In method prefix_finder_given_time, set(prefix) = {0}'.format([prefix_tmp for prefix_tmp in set(prefix_given_time)]))
    for date, prefix_list in prefix_given_time.iteritems():
        prefix_given_time[date] = list(set(prefix_list))

    return prefix_given_time


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

    prefix_size_dic = {}


    for vp in VP_LIST:
        prefix_size_dic[vp]={}
        for given_date in given_date_list:
            prefix_size_dic[vp][given_date] = []

        # 打开5个comparison_time_vp.csv先进行第一次筛选，如果某一行只有No Map Reply就没有必要再打开那个log文件了
        with open(os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))) as f_handler:
            next(f_handler)
            for line in f_handler:
                tmp_list = line.split(';')

                # 如果是RoundNoReply则没有必要处理此行
                if tmp_list[LOG_TIME_COLUMN['round_type_set']] != 'RoundNoReply':

                    csv_file = os.path.join(
                        PLANET_CSV_DIR,
                        vp,
                        '{0}-EID-{1}-MR-{2}.log.csv'.format(
                            LOG_PREFIX[vp],
                            tmp_list[LOG_TIME_COLUMN['eid']],
                            tmp_list[LOG_TIME_COLUMN['resolver']]
                        )
                    )
                    logger.debug(csv_file)
                    tmp_dict = prefix_finder_given_time(csv_file, given_date_list)
                    for key, value in tmp_dict.iteritems():
                       prefix_size_dic[vp][key].extend(value)
        for key, value in prefix_size_dic[vp].iteritems():
            prefix_size_dic[vp][key] = prefix_size(merge_all_prefixes(list(set(value))))

    pprint.pprint(prefix_size_dic)
        # print 'prefix_size_dic[', given_date, '][', vp, '] ='
        # pprint.pprint(prefix_size_dic[given_date][vp])
        # logger.debug('prefix_size_dic[{0}][{1}] = {2}'.format(given_date, vp, prefix_size_dic[given_date][vp]))


    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
    logger.debug("Execution time (in unit of second) of this script: {0}".format(stop_time - start_time))