# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 此脚本用来分组，分组规则为对于同一个RLOC可以对应多少个不同的prefix
# 因此考虑构建dictionary的结构，key为RLOC，value为prefix


import timeit
import re
from config.config import *
from netaddr import *
import pprint
import logging
import resolver_comparator as rc

# 针对comparison_time_vp.csv中一行多个prefix的情况
def rloc_associated_diff_prefix(tmp_list):
    dic_rloc_prefixes = {}

    # 要用函数的输入tmp_list构造出csv_file的路径
    csv_file = os.path.join(PLANET_CSV_DIR, tmp_list[LOG_TIME_COLUMN['vantage']],
                            '{0}-EID-{1}-MR-{2}.log.csv'.format(LOG_PREFIX[tmp_list[LOG_TIME_COLUMN['vantage']]],
                                        tmp_list[LOG_TIME_COLUMN['eid']], tmp_list[LOG_TIME_COLUMN['resolver']]))

    with open(csv_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 只有Round Type是Normal时才予以考虑
            if tmp_list[LOG_COLUMN['round_type']] == 'RoundNormal':

                # 找出此map reply中有几个RLOC，由此可以遍历tmp_list[LOG_COLUMN[locator_id']]列及之后的(locator_count-1)列
                for rloc_addr in tmp_list[LOG_COLUMN['locator_id']:]:
                    prefix_current = tmp_list[LOG_COLUMN['mapping_entry']]
                    eid_current = tmp_list[LOG_COLUMN['eid']]
                    # 因为tmp_list[LOG_COLUMN['locator_id']不是纯的ip地址值，所以需要把用不到的信息删除
                    locator_id = IPAddress(rloc_addr.split(',')[1])

                    # 如果当前这个RLOC还不是dic_rloc_prefixes中的key，则说明此RLOC还未添加
                    # 那就把此RLOC作为key，并添加相应的prefix作为value
                    if locator_id not in dic_rloc_prefixes.keys():
                        dic_rloc_prefixes[locator_id] = [(prefix_current, eid_current)]
                    # 如果当前这个RLOC已经是dic_rloc_prefixes中的key了的话，只要给此key添加不重复的value即可
                    else:
                        # 如果要添加的value是新值的话再进行添加
                        if prefix_current not in dic_rloc_prefixes[locator_id]:
                            dic_rloc_prefixes[locator_id].append((prefix_current, eid_current))

    return dic_rloc_prefixes


# 此函数用来针对某一行构造一个字典
# 以 LOG_TIME_COLUMN['RLOC_set'] 及之后的 LOG_TIME_COLUMN['different_locator_count']-1 列的RLOC作为key
# LOG_TIME_COLUMN['mapping_entry'] 作为value
def rlocs_associated_one_prefix(tmp_list):
    dic_rloc_prefixes = {}

    # 按照此行对应的RLOC的个数，创建相应字典，因为此函数只针对comparison_time_vp.csv文件的一行，
    # 所以但凡创建字典肯定是没有过的key元素，所以只要创建无需添加
    # 但是因为直接从 tmp_list[LOG_TIME_COLUMN['mapping_entry']] 里取得时候还有该mapping_entry出现的次数，
    # 所以用.split()和replace()等消除掉
    # 同理把tmp_list[LOG_TIME_COLUMN['RLOC_set']尾部的'\r\n'也消除掉
    # for i in range(0, int(tmp_list[LOG_TIME_COLUMN['different_locator_count']])):
    #     dic_rloc_prefixes[IPAddress(tmp_list[LOG_TIME_COLUMN['RLOC_set'] + i].replace('\r\n',''))] \
    #         = [tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(',')[0].replace("(",'').replace("'",'')]

    for rloc_addr in tmp_list[LOG_TIME_COLUMN['RLOC_set']:]:
        dic_rloc_prefixes[IPAddress(rloc_addr.replace('\r\n', ''))] = \
            [(tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(',')[0].replace("(",'').replace("'",''),
              tmp_list[LOG_TIME_COLUMN['eid']])]

    return dic_rloc_prefixes




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

    # 在5个csv文件中直接逐行读取数值


    # 创建一个总字典，存储每个vantage对应的子字典
    dic_rloc_prefix = {}
    consistent_result_list = {}
    for vp in VP_LIST:
        dic_rloc_prefix[vp] = {}
        with open(os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))) as f_handler:
            next(f_handler)
            for line in f_handler:
                tmp_list = line.split(';')

                # 只有当LOG_TIME_COLUMN['round_type_set']中含有RoundNormal时予以考虑
                if re.search('RoundNormal', tmp_list[LOG_TIME_COLUMN['round_type_set']]):
                    # 如果 LOG_TIME_COLUMN['mapping_entry']只含有一个元素时，为节省时间，则可直接创建字典：
                    # 由于LOG_TIME_COLUMN['mapping_entry']列的显示格式是 ('37.77.58.0/23', 537),('37.77.58.0/26', 71)
                    # 所以用 .split(',')之后的list个数为实际prefix个数的2倍
                    if len(tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(','))/2 == 1:
                        # 此处可调用函数 rlocs_associated_one_prefix(tmp_list) 来实现
                        # 用此语法合并2个字典即可：dictMerged = dict(dict1, **dict2)
                        # dict1相当于main函数里最终结果的字典，dict2相当于每次调用函数时返回的字典
                        # 即：dictMerged = dic_rloc_prefix_liege （和dict1为同一个字典）
                        # dict1 ＝ dic_rloc_prefix_liege
                        # dict2 ＝ rlocs_associated_one_prefix(tmp_list)
                        tmp_dict = rlocs_associated_one_prefix(tmp_list)
                        for key, value in tmp_dict.iteritems():
                            if key in dic_rloc_prefix[vp].keys():
                                dic_rloc_prefix[vp][key].extend(value)
                            else:
                                dic_rloc_prefix[vp][key] = value
                    # 当 LOG_TIME_COLUMN['mapping_entry'] 的个数不为一时，则必须得遍历原 PlanetLab_CSV 文件已确定哪个RLOC对应哪个prefix，
                    # 即调用函数 rloc_associated_diff_prefix(csv_file)
                    else:
                        tmp_dict = rloc_associated_diff_prefix(tmp_list)
                        for key, value in tmp_dict.iteritems():
                            if key in dic_rloc_prefix[vp].keys():
                                dic_rloc_prefix[vp][key].extend(value)
                            else:
                                dic_rloc_prefix[vp][key] = value

                        # dic_rloc_prefix[vp] = dict(dic_rloc_prefix_liege, **rloc_associated_diff_prefix(tmp_list))


        # 去重。。。
        for key, value in dic_rloc_prefix[vp].iteritems():
            dic_rloc_prefix[vp][key] = list(set(value))


        print '\n\nIn', vp, ', there are', len(dic_rloc_prefix[vp]), 'groups, in which one RLOC associated with different prefixes'
        pprint.pprint(dic_rloc_prefix[vp])
        logger.debug('\n\nIn {0}, there are {1} groups, in which one RLOC associated with different prefixes'.format(vp, len(dic_rloc_prefix[vp])))
        logger.debug(dic_rloc_prefix[vp])

        # 在此调用函数 is_conherent_in_group()，并存在
        consistent_result_list[vp] = []
        for key, value in dic_rloc_prefix[vp].iteritems():
            eid_list = [i[1] for i in value]
            consistent_result_list[vp].append(is_conherent_in_group(vp, eid_list))

        # 将几组之间consistent的最终结果打印出来
        print "There are", consistent_result_list[vp].count(True), "True over", len(consistent_result_list[vp]), "groups in total,"
        print "and", consistent_result_list[vp].count(False), "False over", len(consistent_result_list[vp])
        logger.debug("There are {0} True over {1} groups in total, "
                     "and {2} False over {3}".format(consistent_result_list[vp].count(True),
                                                     len(consistent_result_list[vp]),
                                                     consistent_result_list[vp].count(False),
                                                     len(consistent_result_list[vp])))
        print "Consistent result in", vp, "---->", consistent_result_list[vp]
        logger.debug("Consistent result in {0} ----> {1}".format(vp, consistent_result_list[vp]))



    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
    logger.debug("Execution time (in unit of second) of this script: {0}".format(stop_time - start_time))
