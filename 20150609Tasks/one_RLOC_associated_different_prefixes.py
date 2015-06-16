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
                for i in range(0, int(tmp_list[LOG_COLUMN['locator_count']])):
                    prefix_current = tmp_list[LOG_COLUMN['mapping_entry']]
                    # 因为tmp_list[LOG_COLUMN['locator_id']不是纯的ip地址值，所以需要把用不到的信息删除
                    locator_id = IPAddress(tmp_list[LOG_COLUMN['locator_id'] + i].split(',')[1])

                    # 如果当前这个RLOC还不是dic_rloc_prefixes中的key，则说明此RLOC还未添加
                    # 那就把此RLOC作为key，并添加相应的prefix作为value
                    if locator_id not in dic_rloc_prefixes.keys():
                        dic_rloc_prefixes[locator_id] = [prefix_current]
                    # 如果当前这个RLOC已经是dic_rloc_prefixes中的key了的话，只要给此key添加不重复的value即可
                    else:
                        # 如果要添加的value是新值的话再进行添加
                        if prefix_current not in dic_rloc_prefixes[locator_id]:
                            dic_rloc_prefixes[locator_id].append(prefix_current)

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
    for i in range(0, int(tmp_list[LOG_TIME_COLUMN['different_locator_count']])):
        dic_rloc_prefixes[IPAddress(tmp_list[LOG_TIME_COLUMN['RLOC_set'] + i].replace('\r\n',''))] \
            = [tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(',')[0].replace("(",'').replace("'",'')]

    return dic_rloc_prefixes



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

    # 在5个csv文件中直接逐行读取数值



    for vp in VP_LIST:
        dic_rloc_prefix_liege = {}
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
                        dic_rloc_prefix_liege = dict(dic_rloc_prefix_liege, **rlocs_associated_one_prefix(tmp_list))
                    # 当 LOG_TIME_COLUMN['mapping_entry'] 的个数不为一时，则必须得遍历原 PlanetLab_CSV 文件已确定哪个RLOC对应哪个prefix，
                    # 即调用函数 rloc_associated_diff_prefix(csv_file)
                    else:
                        dic_rloc_prefix_liege = dict(dic_rloc_prefix_liege, **rloc_associated_diff_prefix(tmp_list))


        print '\n\nIn', vp, ', there are', len(dic_rloc_prefix_liege), 'groups, in which one RLOC associated with different prefixes'
        pprint.pprint(dic_rloc_prefix_liege)

    # 由于dic的key现为string，无法直接调用sorted(),如需排序目前思路为将所有的key即不同的RLOC转变为IPAddress()型之后即可排序


    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
