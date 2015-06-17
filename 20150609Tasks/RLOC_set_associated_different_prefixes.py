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
                for i in range(0, int(tmp_list[LOG_COLUMN['locator_count']])):
                    rloc_set_list.append((tmp_list[LOG_COLUMN['locator_id'] + i]).split(',')[1].replace('\r\n',''))
                dic_tmp[tmp_list[LOG_COLUMN['mapping_entry']].split(',')[0].replace("(",'').replace("'",'')] \
                    = ','.join(rloc_set_list)

            # 每一行处理完相当于新建了一个dic，所以要与最终存整个文件的的dic merge
            # 用此语法合并2个字典即可：dictMerged = dict(dict1, **dict2)，即：
            # dictMerged = dic_prefix_rloc_set （和dict1为同一个字典）
            # dict1 ＝ dic_prefix_rloc_set
            # dict2 ＝ dic_tmp
            dic_prefix_rloc_set = dict(dic_prefix_rloc_set, **dic_tmp)

    # 因为在当前得到的dic_prefix_rloc_set中，key为prefix，而value为RLOC set
    # 与我们最终要返回的dic的key和value刚好相反，所以此处需要把key和value对互换
    dic_tmp = {}
    for value, key in dic_prefix_rloc_set.items():
        dic_tmp[key] = value
    dic_rloc_set_prefixes = dict(dic_rloc_set_prefixes, **dic_tmp)

    # for value, key in dic_prefix_rloc_set.items():
    #     if key in dic_rloc_set_prefixes.keys():
    #         dic_rloc_set_prefixes[key] = dic_rloc_set_prefixes[key] + ',' + value
    #     else:
    #         dic_rloc_set_prefixes[key] = value


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
    for i in range(0, int(tmp_list[LOG_TIME_COLUMN['different_locator_count']])):
        rloc_set_key_list.append(tmp_list[LOG_TIME_COLUMN['RLOC_set'] + i].replace('\r\n',''))

    # 从rloc_set_key_list生成rloc_set_key作为key，将LOG_TIME_COLUMN['mapping_entry'] 作为value存进字典即可
    dic_rloc_set_prefixes[','.join(rloc_set_key_list)] = \
        [tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(',')[0].replace("(",'').replace("'",'')]

    return dic_rloc_set_prefixes



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



    for vp in VP_LIST:
        dic_rloc_set_prefix = {}
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
                        # 此处可调用函数 rloc_set_associated_one_prefix(tmp_list) 来实现
                        # 用此语法合并2个字典即可：dictMerged = dict(dict1, **dict2)
                        # dict1相当于main函数里最终结果的字典，dict2相当于每次调用函数时返回的字典
                        # 即：dictMerged = dic_rloc_set_prefix （和dict1为同一个字典）
                        # dict1 ＝ dic_rloc_set_prefix
                        # dict2 ＝ rlocs_associated_one_prefix(tmp_list)
                        dic_rloc_set_prefix = dict(dic_rloc_set_prefix, **rloc_set_associated_one_prefix(tmp_list))
                        logger.debug(str(dic_rloc_set_prefix))

                    # 当 LOG_TIME_COLUMN['mapping_entry'] 的个数不为一时，则必须得遍历原 PlanetLab_CSV 文件已确定哪个RLOC对应哪个prefix，
                    # 即调用函数 rloc_associated_diff_prefix(csv_file)
                    else:
                        dic_rloc_set_prefix = dict(dic_rloc_set_prefix, **rloc_set_associated_diff_prefix(tmp_list))


        print '\n\nIn', vp, ', there are', len(dic_rloc_set_prefix), 'groups, in which one RLOC associated with different prefixes'
        pprint.pprint(dic_rloc_set_prefix)



    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time