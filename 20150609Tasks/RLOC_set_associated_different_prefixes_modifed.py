# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 此脚本用来分组，分组规则为对于同一组RLOC set可以对应多少个不同的prefix
# 因此考虑构建dictionary的结构，key为RLOC set，value为prefix


import timeit
import re
from config.config import *
from netaddr import *
import pprint
import logging
import resolver_comparator as rc

# 2015-06-22: All the following codes are used to generate a dictionary whose key is RLOC set and value is
# a list of prefix. To reduce the execution time, first iterate the "comparison_time_<VANTAGE>.csv" file, we only look
# up concrete log file only and if only the attribute "Different Locator Count" is greater than 1. Otherwise, the prefix
# list and the RLOC value are directly used as key-value pair in final dictionary.


def rloc_set_associated_one_prefix(tmp_list):
    dic_rloc_set_prefixes = {}

    # 按照此行对应的RLOC set，创建相应字典，因为此函数只针对comparison_time_vp.csv文件的一行，
    # 所以但凡创建字典肯定是没有过的key元素，所以只要创建无需添加
    # 但是因为直接从 tmp_list[LOG_TIME_COLUMN['mapping_entry']] 里取得时候还有该mapping_entry出现的次数，
    # 所以用.split()和replace()等消除掉
    # 同理把tmp_list[LOG_TIME_COLUMN['RLOC_set']尾部的'\r\n'也消除掉
    # 把从LOG_TIME_COLUMN['RLOC_set'] 及之后的 LOG_TIME_COLUMN['different_locator_count']-1 列的RLOC合并成最终想用的key
    rloc_set_key_list = []
    # for i in range(0, int(tmp_list[LOG_TIME_COLUMN['different_locator_count']])):
    #     rloc_set_key_list.append(tmp_list[LOG_TIME_COLUMN['RLOC_set'] + i].replace('\r\n',''))

    for rloc_addr in tmp_list[LOG_TIME_COLUMN['RLOC_set']:]:
        rloc_set_key_list.append(rloc_addr.replace('\r\n',''))

    # 从rloc_set_key_list生成rloc_set_key作为key，将LOG_TIME_COLUMN['mapping_entry'] 作为value存进字典即可
    dic_rloc_set_prefixes[','.join(rloc_set_key_list)] = \
        [(tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(',')[0].replace("(",'').replace("'",''), tmp_list[LOG_TIME_COLUMN['eid']])]

    return dic_rloc_set_prefixes

def mapping_entry_list_generator(mapping_entries):
    """
        input: mapping entry string with format such as: "('0.0.0.0/0', 752),('1.0.0.0/0', 742)"
        output: a list of mapping entry
    """
    tmp_list = mapping_entries.replace('(', '').replace(')', '').replace("'", "").split(',')
    # 我们只把 下标为偶数的 元素放入最终返回的list中
    mapping_entry_list = [element for x, element in enumerate(tmp_list) if x % 2 == 0]
    return mapping_entry_list

def multiple_rloc_processor(tmp_list):
    dic_rloc_set_prefixes = {}
    # 要用函数的输入tmp_list构造出csv_file的路径
    csv_file = os.path.join(PLANET_CSV_DIR,
                            tmp_list[LOG_TIME_COLUMN['vantage']],
                            '{0}-EID-{1}-MR-{2}.log.csv'.format(
                                LOG_PREFIX[tmp_list[LOG_TIME_COLUMN['vantage']]],
                                tmp_list[LOG_TIME_COLUMN['eid']],
                                tmp_list[LOG_TIME_COLUMN['resolver']]
                            )
    )

    with open(csv_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp = line.split(';')
            # 只有Round Type是Normal时才予以考虑
            if tmp[LOG_COLUMN['round_type']] == 'RoundNormal':
                # tmp_list[LOG_COLUMN['locator_id']:] 的形式为：['0,87.195.36.39,up,50,100', '1,95.97.176.115,up,10,100']
                # key的形式为："87.195.36.39,95.97.176.115"
                key = ",".join([element.split(',')[1] for element in tmp[LOG_COLUMN['locator_id']:]])
                value = [tmp[LOG_COLUMN['mapping_entry']]]
                if key in dic_rloc_set_prefixes.keys():
                    dic_rloc_set_prefixes[key].extend(value)
                else:
                    dic_rloc_set_prefixes[key] = value


    # 返回最终结果前，去重
    for key, value in dic_rloc_set_prefixes.iteritems():
        dic_rloc_set_prefixes[key] = list(set(value))


    return dic_rloc_set_prefixes

def rloc_prefixes_dict_generator():
    """
        input:
        output: a dictionay of dictionary
    """
    result_dict = {}
    for vp in TRACES_LOG.keys():
        # Each vantange name is a key in final returned dictionary and its value is also a dictionary
        result_dict[vp]={}
        with open(os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))) as f_handler:
            # The first line does not contain useful information
            next(f_handler)
            for line in f_handler:
                tmp_list = line.split(';')
                # We only consider those lines containing "RoundNormal" round type
                # LOG_TIME_COLUMN['round_type_set'] indicates the index of attribute "Round Type Set" which is a string
                # storing all round types and separted by comma
                if "RoundNormal" in tmp_list[LOG_TIME_COLUMN['round_type_set']].split(','):
                    # Still divide into two cases: line containing one RLOC address and multiple RLOC addresses.
                    if int(LOG_TIME_COLUMN['different_locator_count']) == 1:
                        # The key format is a string, such as: "87.195.196.77,95.97.83.93,2001:9e0:8500:b00::1"
                        # 会不会出现这样的隐患呢？就是 Python将 "87.195.196.77,95.97.83.93,2001:9e0:8500:b00::1"和
                        # "87.195.196.77,2001:9e0:8500:b00::1,95.97.83.93"视为不同的键。换言之，必须保证CSV文件中RLOC Set按
                        # 顺序排列好的
                        key = ",".join(tmp_list[LOG_TIME_COLUMN['RLOC_set']])
                        # tmp_list[LOG_TIME_COLUMN['mapping_entry']]格式如下：('0.0.0.0/0', 752)
                        value = mapping_entry_list_generator(tmp_list[LOG_TIME_COLUMN['mapping_entry']])
                        # 注意： 此时不考虑prefix重复问题
                        if key in result_dict[vp].keys():
                            result_dict[vp][key].extend(value)
                        else:
                            result_dict[vp][key] = value
                    else:
                        # Case where multiple RLOC addresses in the same line, we should know
                        tmp_dict = multiple_rloc_processor(tmp_list)
                        for key, value in tmp_dict.iteritems():
                            if key in result_dict[vp].keys():
                                result_dict[vp][key].extend(value)
                            else:
                                result_dict[vp][key] = value
        # 每处理完一个comparison_time_<VANTANGE>.csv file, 就对所得字典进行一次去重操作
        for key, value in result_dict[vp].iteritems():
            result_dict[vp][key] = list(set(value))

    return result_dict

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

    result_dict = rloc_prefixes_dict_generator()

    for vp, vp_dict in result_dict.iteritems():
        print 'In', vp, ', there are', len(vp_dict), 'groups, in which one RLOC associated with different prefixes'
        pprint.pprint(vp_dict)

    print "Overall statistical result:"
    for vp, vp_dict in result_dict.iteritems():
        one2one_nb = sum([1 for element in vp_dict.values() if len(element) == 1])
        print "One to One pair number in", vp, "is", one2one_nb, "among", len(vp_dict), "pairs."

    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
    logger.debug("Execution time (in unit of second) of this script: {0}".format(stop_time - start_time))

