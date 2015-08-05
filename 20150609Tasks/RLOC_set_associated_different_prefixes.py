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
import numpy as np
import matplotlib.pyplot as plt


# 针对comparison_time_vp.csv中一行多个prefix的情况
def rloc_set_associated_diff_prefix(tmp_list):
    dic_rloc_set_prefixes = {}
    dic_prefix_rloc_set = {}

    # 要用函数的输入tmp_list构造出csv_file的路径
    csv_file = os.path.join(PLANET_CSV_DIR, tmp_list[LOG_TIME_COLUMN['vantage']],
                            '{0}-EID-{1}-MR-{2}.log.csv'.format(LOG_PREFIX[tmp_list[LOG_TIME_COLUMN['vantage']]],
                                        tmp_list[LOG_TIME_COLUMN['eid']], tmp_list[LOG_TIME_COLUMN['resolver']]))

    with open(csv_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')
            dic_tmp = {}

            # 只有Round Type是Normal时才予以考虑
            if tmp_list[LOG_COLUMN['round_type']] == 'RoundNormal':
                rloc_set_list = []
                # 将LOG_COLUMN['locator_id']列到LOG_COLUMN['locator_id']－1列的RLOC拼成一个string，暂时作为value存起来
                # for i in range(0, int(tmp_list[LOG_COLUMN['locator_count']])):
                #     rloc_set_list.append((tmp_list[LOG_COLUMN['locator_id'] + i]).split(',')[1].replace('\r\n',''))

                for rloc_addr in tmp_list[LOG_COLUMN['locator_id']:]:
                    rloc_set_list.append(rloc_addr.split(',')[1].replace('\r\n',''))

                dic_tmp[(tmp_list[LOG_COLUMN['mapping_entry']].split(',')[0].replace("(",'').replace("'",''), tmp_list[LOG_COLUMN['eid']])] \
                    = rloc_set_list

            # 每一行处理完相当于新建了一个dic，所以要与最终存整个文件的的dic merge
            # 用此语法合并2个字典即可：dictMerged = dict(dict1, **dict2)，即：
            # dictMerged = dic_prefix_rloc_set （和dict1为同一个字典）
            # dict1 ＝ dic_prefix_rloc_set
            # dict2 ＝ dic_tmp
            # dic_prefix_rloc_set = dict(dic_prefix_rloc_set, **dic_tmp)
            for key, value in dic_tmp.iteritems():
                if key in dic_prefix_rloc_set.keys():
                    dic_prefix_rloc_set[key].extend(value)
                else:
                    dic_prefix_rloc_set[key] = value

    # 在此 dic_prefix_rloc_set 遍历了整个文件，并以prefix为key，[RLOC set]为value的字典形式存储了下来
    # 现在先对 dic_prefix_rloc_set 消一次重，因为value为list，有可能重复记录了很多次，方便后续工作
    for key, value in dic_prefix_rloc_set.iteritems():
        dic_prefix_rloc_set[key] = ','.join(list(set(value)))

    # 因为在当前得到的dic_prefix_rloc_set中，key为prefix，而value为RLOC set
    # 与我们最终要返回的dic的key和value刚好相反，所以此处需要把key和value对互换
    for value, key in dic_prefix_rloc_set.iteritems():
        if key in dic_rloc_set_prefixes.keys():
            dic_rloc_set_prefixes[key].extend([value])
        else:
            dic_rloc_set_prefixes[key] = [value]

    # dic_rloc_set_prefixes 已接近最终想要返回的dic，只需要再去一次重即可
    for key, value in dic_rloc_set_prefixes.iteritems():
        dic_rloc_set_prefixes[key] = list(set(value))


    return dic_rloc_set_prefixes


# 此函数用来针对某一行构造一个字典
# 以 LOG_TIME_COLUMN['locators_set'] 中的RLOC set作为key，处理时可以.split('#')
# LOG_TIME_COLUMN['mapping_entry'] 作为value
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



# 此函数将调用 resolver_comparator 里的is_coherent_for_given_date(log_file_list, eid, logger)函数，
# 去比较所给log是否coherent并返回True或False
def is_conherent_in_group(vp, eid_list):
    # 根据输入的 vp 和 eid_list 确定 log_file_list
    consistent_result_list = []
    for eid in eid_list:
        log_file_list = []
        for mr in MR_LIST:
            log_file_list.append(os.path.join(PLANET_CSV_DIR, vp,
                                              '{0}-EID-{1}-MR-{2}.log.csv'.format(LOG_PREFIX[vp], eid, mr)))
        consistent_result_list.append(rc.is_coherent_for_given_date(log_file_list, eid, logger)['coherent'])

    # 得到类似于 consistent_result_list ＝ [True, True, False] 的list，如果其中有一个为False，则几组之间的比较结果肯定也为False
    # 只有全为True，则整体比较才可能是True
    if False in consistent_result_list:
        return False
    else:
        return True

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

    # # 在5个csv文件中直接逐行读取数值
    #
    #
    # # 创建一个总字典，存储每个vantage对应的子字典
    # dic_rloc_set_prefix = {}
    # consistent_result_list = {}
    # for vp in VP_LIST:
    #     dic_rloc_set_prefix[vp] = {}
    #     with open(os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))) as f_handler:
    #         next(f_handler)
    #         for line in f_handler:
    #             tmp_list = line.split(';')
    #
    #             # 只有当LOG_TIME_COLUMN['round_type_set']中含有RoundNormal时予以考虑
    #
    #             if re.search('RoundNormal', tmp_list[LOG_TIME_COLUMN['round_type_set']]):
    #                 # 如果 LOG_TIME_COLUMN['mapping_entry']只含有一个元素时，为节省时间，则可直接创建字典：
    #                 # 由于LOG_TIME_COLUMN['mapping_entry']列的显示格式是 ('37.77.58.0/23', 537),('37.77.58.0/26', 71)
    #                 # 所以用 .split(',')之后的list个数为实际prefix个数的2倍
    #                 if len(tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(','))/2 == 1:
    #                     # 此处可调用函数 rloc_set_associated_one_prefix(tmp_list) 来实现
    #                     # 用此语法合并2个字典即可：dictMerged = dict(dict1, **dict2)
    #                     # dict1相当于main函数里最终结果的字典，dict2相当于每次调用函数时返回的字典
    #                     # 即：dictMerged = dic_rloc_set_prefix （和dict1为同一个字典）
    #                     # dict1 ＝ dic_rloc_set_prefix
    #                     # dict2 ＝ rloc_set_associated_one_prefix(tmp_list)
    #                     # dic_rloc_set_prefix[vp] = dict(dic_rloc_set_prefix[vp], **rloc_set_associated_one_prefix(tmp_list))
    #                     tmp_dict = rloc_set_associated_one_prefix(tmp_list)
    #                     for key, value in tmp_dict.iteritems():
    #                         if key in dic_rloc_set_prefix[vp].keys():
    #                             dic_rloc_set_prefix[vp][key].extend(value)
    #                         else:
    #                             dic_rloc_set_prefix[vp][key] = value
    #
    #
    #                 # 当 LOG_TIME_COLUMN['mapping_entry'] 的个数不为一时，则必须得遍历原 PlanetLab_CSV 文件已确定哪个RLOC对应哪个prefix，
    #                 # 即调用函数 rloc_associated_diff_prefix(csv_file)
    #                 else:
    #                     # dic_rloc_set_prefix[vp] = dict(dic_rloc_set_prefix[vp], **rloc_set_associated_diff_prefix(tmp_list))
    #                     tmp_dict = rloc_set_associated_diff_prefix(tmp_list)
    #                     for key, value in tmp_dict.iteritems():
    #                         if key in dic_rloc_set_prefix[vp].keys():
    #                             dic_rloc_set_prefix[vp][key].extend(value)
    #                         else:
    #                             dic_rloc_set_prefix[vp][key] = value
    #
    #
    #     # 去重。。。
    #     for key, value in dic_rloc_set_prefix[vp].iteritems():
    #         dic_rloc_set_prefix[vp][key] = list(set(value))
    #
    #
    #     print '\n\nIn', vp, ', there are', len(dic_rloc_set_prefix[vp]), 'groups, in which one RLOC associated with different prefixes'
    #     pprint.pprint(dic_rloc_set_prefix[vp])
    #     logger.debug('\n\nIn {0}, there are {1} groups, in which one RLOC associated with different prefixes'.format(vp, len(dic_rloc_set_prefix[vp])))
    #     logger.debug(dic_rloc_set_prefix[vp])
    #
    #     # 在此调用函数 is_conherent_in_group()，并存在
    #     consistent_result_list[vp] = []
    #     for key, value in dic_rloc_set_prefix[vp].iteritems():
    #         eid_list = [i[1] for i in value]
    #         consistent_result_list[vp].append(is_conherent_in_group(vp, eid_list))
    #
    #     # 将几组之间consistent的最终结果打印出来
    #     print "There are", consistent_result_list[vp].count(True), "True over", len(consistent_result_list[vp]), "groups in total,"
    #     print "and", consistent_result_list[vp].count(False), "False over", len(consistent_result_list[vp])
    #     logger.debug("There are {0} True over {1} groups in total, "
    #                  "and {2} False over {3}".format(consistent_result_list[vp].count(True),
    #                                                  len(consistent_result_list[vp]),
    #                                                  consistent_result_list[vp].count(False),
    #                                                  len(consistent_result_list[vp])))
    #     print "Consistent result in", vp, "---->", consistent_result_list[vp]
    #     logger.debug("Consistent result in {0} ----> {1}".format(vp, consistent_result_list[vp]))


    # Modify the size and dpi of picture, default size is (8,6), default dpi is 80
    plt.gcf().set_size_inches(8,6)
    plt.gcf().set_dpi(300)

    # 此处开始画图，input应当为上段代码的输出，但为加速直接把数据输入
    n_groups = 5
    x = [1, 2, 3, 4, 5]
    total_number = (14, 14, 14, 14, 14)
    true_number = (4, 2, 8, 4, 8)

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25

    # opacity = 0.4
    rects1 = plt.bar(index, total_number, bar_width, color='yellow',label='uncorrelated groups')
    rects2 = plt.bar(index, true_number, bar_width, color='b',label='correlated groups')

    plt.xlabel('vantage point', fontsize=22)
    # plt.ylabel('Number', fontsize=16)
    # plt.title('Number of RLOC set associated with different prefixes', fontsize=18)
    plt.xticks(index + bar_width, ('1', '2', '3', '4', '5'))
    # plt.yticks(np.arange(0,50,10), ('', '', '200', '', '4*10exp10', ''))
    plt.ylim(0,18)
    plt.legend()
    plt.savefig(os.path.join(PLOT_DIR, 'Number_RLOC_set_different_prefixes.eps'), dpi=300)
    plt.show()


    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
    logger.debug("Execution time (in unit of second) of this script: {0}".format(stop_time - start_time))