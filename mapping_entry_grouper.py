# -*- coding: utf-8 -*-
__author__ = 'yueli'

import pprint
from config.config import *
import resolver_comparator
import logging
# 借助第三方 package: netaddr来实现 IP subnetwork的排序
from netaddr import *
import re
import timeit
import datetime

# 定义一个排序函数，使得作为key的EID可以从小到大排列，作为value的Mapping entry list内部也可以按照从小到大排列
def sort_dic_key_value(dic_origin):
        # 把作为key的EID从小到大排列，排序完由EID:Mapping entry组成的键值对的dictionary变为(EID,Mapping entry)元组的list
        dic_sorted = sorted(dic_origin.items())
        # 把每个value list的元素按从小到大依次排列

        for i in dic_sorted:
            i[1].sort()

        return dic_sorted



if __name__ == '__main__':
    start_time = timeit.default_timer()
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

#   关于数据结构 result_dict, 其最终形式为：
#   result_dict = {
#       ‘liege’     : {'eid', [list of mapping entries]},
#       'temple'    : {'eid', [list of mapping entries]},
#       ...
#   }

#   me_grouper_dict = {
#       'liege'     : {'mapping entry': [list of eid]}
#       'temple'    : {'mapping entry': [list of eid]}
#       ...
#   }


    result_dict = {}
    me_grouper_dict ={}
    for vantage_name, log_file in input_logs.iteritems():
        result_dict[vantage_name] = {}
        me_grouper_dict[vantage_name] ={}
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
        # 处理完一个comparison_time_<VANTAGE_POINT>.csv类型的文件，准备更新字典me_grouper_dict
        sorted_list_liege = sort_dic_key_value(result_dict[vantage_name])
        i = 0
        while i < len(sorted_list_liege):
            # 如果maping entry的个数>1,才有资格作为dic_me_grouper的key
            logger.debug("In the first loop, current i is:{0}".format(i))
            if len(sorted_list_liege[i][1]) > 1:
                possible_key = sorted_list_liege[i][1][0]
                eid_list = [sorted_list_liege[i][0]]
                next_eid = sorted_list_liege[i+1][0]
                i = i+1
                # 如果 i >= sorted_list_liege的长度则会溢出，
                # 如果下一个EID被当前prefix最短的mapping entry包含，则被新dic添加
                while (i < len(sorted_list_liege)) and (next_eid in possible_key):
                    eid_list.append(next_eid)
                    i = i+1
                    next_eid = sorted_list_liege[i][0]
                logger.debug("{0} => after processing: {1}".format(possible_key, eid_list))
                logger.debug("after while loop, current i: {0}".format(i))
                me_grouper_dict[vantage_name].update({possible_key: eid_list})
                # dic_me_grouper[sorted_list_liege[i][1][0]] = eid_list
            else:
                i += 1


    print "me_grouper_dict:"
    pprint.pprint(me_grouper_dict)


    # 为方便后续操作，创建字典 vp_me_logs = {}
    # 其内容大体为：
    # vp_me_logs = {
    #       'liege'     : {'mapping entry': [list of logs]}
    #       'temple'    : {'mapping entry': [list of logs]}
    #       ...
    # }
    vp_me_logs = {}

    for vantage, me_eids_dic in me_grouper_dict.iteritems():
        # print vantage
        # pprint.pprint(me_eids_dic)
        vp_me_logs[vantage] ={}
        for me, eids_list in me_eids_dic.iteritems():
            vp_me_logs[vantage][me] =[str(eid) for eid in eids_list]
            vp_me_logs[vantage][me] = [
                "{0}-EID-{1}-MR-{2}.log.csv".format(
                    LOG_PREFIX[vantage], eid, mr
                )
                for eid in vp_me_logs[vantage][me] for mr in MR_LIST
            ]


    pprint.pprint(vp_me_logs)

    # # 为了Debug而把所有详细内容打印出来
    # for vantage, me_logs_dic in vp_me_logs.iteritems():
    #     logger.info("Processing {0}".format(vantage))
    #     for me, log_list in me_logs_dic.iteritems():
    #         log_obj_list = [
    #             resolver_comparator.LogFile(
    #                 os.path.join(PLANET_CSV_DIR, vantage, log_file_str)
    #             )
    #             for log_file_str in log_list
    #         ]
    #         print log_obj_list
    #         logger.info(resolver_comparator.is_coherent(log_obj_list, str(me), logger))






    print me_grouper_dict['liege'] == me_grouper_dict['temple'] == me_grouper_dict['ucl'] == me_grouper_dict['umass'] == me_grouper_dict['wiilab']


    print me_grouper_dict['liege'].items() == me_grouper_dict['temple'].items() == me_grouper_dict['ucl'].items() == me_grouper_dict['umass'].items() == me_grouper_dict['wiilab'].items()

    # for i in me_grouper_dict.iteritems():
    #     logger.info(i)



    # 用raw_file_list来储存每个group里含有的EID－MR-149.20.48.61.log.csv，方便后面画图
    for vp, me_eid_dic in me_grouper_dict.iteritems():
        raw_file_list = []
        for me, eid_presented_list in me_eid_dic.iteritems():
            for eid in eid_presented_list:
                raw_file_list.append(os.path.join(PLANET_CSV_DIR, vp, "{0}-EID-{1}-MR-149.20.48.61.log.csv".format(LOG_PREFIX[vp], str(eid))))

        # # 逐个打开每个group的文件用来画图
        # for raw_file in raw_file_list:
        #     with open(raw_file) as f_handler:
        #         me_in_raw_file = []
        #         next(f_handler)
        #         for line in f_handler:
        #             tmp_list = line.split(";")
        #             tmp_dt = datetime.datetime.strptime(tmp_list[1], "%Y-%m-%d %H:%M:%S")
        #             me_in_raw_file.append(tmp_list[10])

        # 逐个打开每个group的文件用来检测第一列是什么
        for raw_file in raw_file_list:
            with open(raw_file) as f_handler:
                me_in_raw_file = []
                next(f_handler)
                for line in f_handler:
                    tmp_list = line.split(";")
                    if tmp_list[0] != "RoundNoReply":
                        me_in_raw_file.append(tmp_list[0])
                print raw_file, "---->",set(me_in_raw_file)


    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time