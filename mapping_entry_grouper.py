__author__ = 'yueli'
# -*- coding: utf-8 -*-

import pprint
from config.config import *
import logging
# 借助第三方 package: netaddr来实现 IP subnetwork的排序
from netaddr import *
import networkx as nx
import matplotlib.pyplot as plt
import re
import random

# 定义一个排序函数，使得作为key的EID可以从小到大排列，作为value的Mapping entry list内部也可以按照从小到大排列
def sort_dic_key_value(dic_origin):
        # 把作为key的EID从小到大排列，排序完由EID:Mapping entry组成的键值对的dictionary变为(EID,Mapping entry)元组的list
        dic_sorted = sorted(dic_origin.items())
        # 把每个value list的元素按从小到大依次排列

        for i in dic_sorted:
            i[1].sort()

        return dic_sorted



if __name__ == '__main__':

    # 读取环境变量 ‘PROJECT_LOG_DIR’ (此变量定义在工作目录下.profile或者.bashprofile)
    try:
        LOG_DIR = os.environ['PROJECT_LOG_DIR']
    except KeyError:
        print "Environment variable PROJECT_LOG_DIR is not properly defined or " \
              "the definition about this variable is not taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"


    # 定义字典，存储需要读入的文件
    # 注意：所以本脚本的执行依赖于读入文件(comparison_time_liege.csv,etc.)的格式
    # 如果有朝一日，csv文件格式改变，本脚本也许需要做些修改
    input_logs = {
        'liege': os.path.join(LOG_DIR, 'comparison_time_liege.csv'),
        'temple': os.path.join(LOG_DIR, 'comparison_time_temple.csv'),
        'ucl': os.path.join(LOG_DIR, 'comparison_time_ucl.csv'),
        'umass': os.path.join(LOG_DIR, 'comparison_time_umass.csv'),
        'wiilab': os.path.join(LOG_DIR, 'comparison_time_wiilab.csv')
    }


    # 利用Python logging模块，记录脚本运行信息，有利于debug...
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), '{0}.log'.format(__file__)),
        level=logging.INFO,
        filemode='w',
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.debug(input_logs)

    result_dict = {}
    for vantage_name, log_file in input_logs.iteritems():
        result_dict[vantage_name] = {}
        with open(log_file) as f_handler:
            next(f_handler)
            num = 1
            for line in f_handler:
                tmp_list = line.split(';')
                if tmp_list[LOG_TIME_COLUMN['mapping_entry']] != '':
                    EID = IPAddress(tmp_list[LOG_TIME_COLUMN['eid']])
                    # me_list 存贮从CSV文件 mapping_entry 提取出的已经去掉出现次数的纯 mapping_entry
                    # 用 .split(',') 使得一次同时出现多个 mapping_entry 可以分开存储
                    # 删掉所有0.0.0.0/0的 mapping_entry
                    me_list = [IPNetwork(a) for a in re.sub("', \d+\)", '', re.sub("\('", '', tmp_list[LOG_TIME_COLUMN['mapping_entry']])).split(',') if a != '0.0.0.0/0']
                    # 如果此 key(EID) 已经存在，只要在 key 位置加入新 value 即可
                    if result_dict[vantage_name].has_key(EID):
                        # 如何当前的mapping entry 不同于已存的 mapping entry，则进行添加
                        for a in me_list:
                            if a not in result_dict[vantage_name][EID]:
                                result_dict[vantage_name][EID].append(a)
                        # 如何当前的mapping entry 等于已存的 mapping entry，则什么也不做
                            else:
                                continue
                    # 如果此 key(EID) 不存在，则需要添加 key value 对
                    else:
                        result_dict[vantage_name].update({EID: me_list})

    # print "Try the new sorted method: "
    # print "length of result_dict['liege']:", len(sort_dic_key_value(result_dict['liege']))
    # print sort_dic_key_value(result_dict['liege'])

    sorted_list_liege = sort_dic_key_value(result_dict['liege'])
    dic_me_grouper = {}
    for i, element in enumerate(sorted_list_liege):
         # 如果maping entry的个数>1,才有资格作为dic_me_grouper的key
         if len(element[1]) > 1:
            eid_list = [element[0]]
            i = i+1
            # 如果 i >= sorted_list_liege的长度则会溢出，
            # 如果下一个EID被当前prefix最短的mapping entry包含，则被新dic添加
            while i < len(sorted_list_liege) and sorted_list_liege[i][0] in element[1][0]:
                eid_list.append(sorted_list_liege[i][0])
                i = i+1
            dic_me_grouper.update({element[1][0]: eid_list})


    print "length of dic_me_grouper:", len(sort_dic_key_value(dic_me_grouper))
    print "Final result"
    pprint.pprint(sort_dic_key_value(dic_me_grouper))

    all_eid_set = []
    with open(os.path.join(LOG_DIR, 'comparison_time_liege.csv')) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            all_eid_set.append(IPAddress(tmp_list[LOG_TIME_COLUMN['eid']]))

    all_eid_set = list(set(all_eid_set))

    print 'In original file, eid number is', len(all_eid_set)
    # pprint.pprint(all_eid_set)

    middle_process = [element[0] for element in sort_dic_key_value(result_dict['liege'])]
    print len(middle_process)
    #pprint.pprint(middle_process)

    after_process = []
    for value in dic_me_grouper.itervalues():
        after_process.extend(value)
    print "After processing,", len(after_process)
    #pprint.pprint(sorted(after_process))

    rest = list(set(all_eid_set)-set(middle_process))
    pprint.pprint(rest)









