# -*- coding: utf-8 -*-
__author__ = 'qsong'

import os
import logging
import socket
import csv
import glob
import datetime
from utility.REPattern_opt import *


class Round(object):

    # 根究CSV文件中的每一列，生成一个Round类型的对象
    # csv_row 可能的形式有：
    # 'RoundNormal',
    # '2013-07-18 23:30:18',
    # '37.77.56.64',
    # '149.20.48.61',
    # '139.165.12.211',
    # '149.20.48.61',
    # '37.77.56.64',
    #  '95.97.83.93', '0.17900', '3', '37.77.56.64/26', '1440', '1', '0', '0,87.195.196.77,up,50,100',
    # '1,95.97.83.93,up,10,100',
    # '2,2001:9e0:8500:b00::1,up,50,100'
    def __init__(self, csv_row):
        self.csv_row = csv_row
        self.type = csv_row[0]
        self.date = datetime.datetime.strptime("".join(csv_row[1].split(" ")), "%Y-%m-%d%H:%M:%S")
        # Remove second and just keep year,month,day,hour,minute
        self.date = self.date.replace(second=0, microsecond=0)
        self.eid = csv_row[2]
        self.resolver = csv_row[3]
        if self.type == 'RoundNormal':
            self.auth = csv_row[12]
            self.mobile = csv_row[13]
            self.locator_count = csv_row[9]
            # rloc_addrs could be in format "0,87.195.196.77#1,95.97.83.93"
            self.rloc_addrs = "#".join([",".join(csv_column.split(',')[0:2]) for csv_column in csv_row[14:]])
            # te_attrs refers to Traffic Engineering related attributes: priority, weight and status
            self.te_attrs = "#".join([",".join(csv_column.split(',')[2:]) for csv_column in csv_row[14:]])
            self.locators = "#".join(csv_row[14:])
    def __repr__(self):
        return ";".join(self.csv_row)

    def __str__(self):
        return ";".join(self.csv_row)

class LogFile(object):

    def __init__(self, csv_file):

        self.rounds = sorted([Round(csv_row) for csv_row in self.csv_sort_list(csv_file)], key=lambda item: item.date)
        self.eid = self.rounds[0].eid
        self.resolver = self.rounds[0].resolver


    def csv_sort_list(self, csv_file, delimiter=';'):
        """Read target csv file into a list and return a sorted list to be written"""
        with open(csv_file, 'rt') as csvfile:

            reader = csv.reader(csvfile, delimiter=delimiter)
            csv_cont_list = list(reader)
            return csv_cont_list[1:]

    def __repr__(self):
        return "LogFile object with eid:{0} and resolver{1} and {2} rounds".format(self.eid, self.resolver, len(self.rounds))


def is_all_resolver_coherent_for_eid(output_file, csv_files, logger):
    """
        input: dict, eid as key and list of LogFile objects as value
        output: RLOC_set_coherent, TE_coherent
        2015-01-17 save comparison result into a CSV file
    """

    print "IS_ALL_RESOLVER"

    with open(output_file, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'EID_Resolver_Pair',
                'Type_Coherent',
                'Auth_Coherent',
                'Mobile_Coherent',
                'Locator_Count_Coherent',
                'RLOC_Address_Coherent',
                'TE_Coherent'
            ]
        )
        for eid_resolver_pair, log_file_list in csv_files.iteritems():
            # 返回13个文件中每条记录比较的结果， 字典类型
            res = is_coherent(log_file_list, eid_resolver_pair, logger)
            # rloc_coherent 和 te_coherent中间有一项为False的时候就要打印警告信息了
            if not res['coherent']:
                writer.writerow([
                        eid_resolver_pair,
                        res['type_coherent'],
                        res['auth_coherent'],
                        res['mobile_coherent'],
                        res['locator_count_coherent'],
                        res['rloc_address_coherent'],
                        res['te_coherent']

                ])



# override this method in resolver_comparator
def is_coherent(log_file_list, eid_resolver_pair, logger):
    """
        input: a list of LogFile object
        output: True or false
    """
    logger.debug("Processing {0}".format(eid_resolver_pair))
    # 默认 coherent值为True, 一旦有异常情况出现，则返回False, 方法立即结束
    # 如若需要统计错误异常的总次数，则需要修改代码
    # 所有的比较指标，默认值都为 True
    res = {
        'coherent': True,
        'type_coherent': True,
        'auth_coherent': True,
        'mobile_coherent': True,
        'locator_count_coherent': True,
        'rloc_address_coherent': True,
        'te_coherent': True

    }
    error_message = {
        'type': 'The type of 5 rounds for eid resolver pair {0} at time {1} is not coherent. Reason: {2}',
        'auth': 'The auth attirbute of 5 rounds for eid resolver pair {0} at time {1} is not coherent. Reason: {2}',
        'mobile': 'The mobile attirbute of rounds for eid resolver pair {0} at time {1} is not coherent. Reason: {2}',
        'locator_count': 'The locator_count attirbute of 5 rounds for eid resolver pair {0} at time {1} is not coherent. Reason: {2}',
        'RLOC address': 'The RLOC address of 5 rounds for eid resolver pair {0} at time {1} is not coherent. Reason: {2}',
        'TE': 'The traffic engineering related attributes for eid resolver pair {0} at time {1} is not coherent. Reason: {2}'
    }
    # 首先要判断 type是不是一致, 如果不一致，则将coherent改为False
    # 我们需要对比每一个时刻的round的类型，如果在某一时刻不一致，立即退出循环

    # 同时我们也需要确保 每一个log文件含有的round数量是一致的，否则立即退出 因为比较没有意义！！


    # 将所有logfile中的round合并到一个round_list中，并且按时间顺序排序
    all_rounds = []

    for log_file in log_file_list:
        all_rounds.extend(log_file.rounds)

    # 貌似这个排序队性能没啥提升
    all_rounds = sorted(all_rounds, key=lambda item: item.date)

    # Retrieve all present datetime in currently processed five LogFile object
    all_datetime = list({round_obj.date for round_obj in all_rounds})
    # Sort all datetime object in ascending order
    all_datetime = sorted(all_datetime)

    rounds_date_dict = {}

    for date in all_datetime:
        rounds_date_dict[date] = []


    # Populate dictionary "round_date_dict", whose format is expected to be following:
    # round_date_dict ={
    #   datetime(2013,7,2,8,30): [round1, round2,....],
    #   datetime(2013,7,2,9,30): [round1, round2,....],
    #   ...
    # }
    for round_obj in all_rounds:
        rounds_date_dict[round_obj.date].append(round_obj)

    for date in sorted(rounds_date_dict.iterkeys()):
        logger.debug("EID-Resolver pair: {0} Date:{1} Round length:{2}".format(
            eid_resolver_pair,
            date,
            len(rounds_date_dict[date]))
        )

    # Start to process the round group(at least one, at most five) corresponding to each datetime
    for date in sorted(rounds_date_dict.iterkeys()):
        round_group = rounds_date_dict[date]
        if len(round_group) < 3:
            # If at a certain time, round number is less than 3, record this as a warning
            logging.warning("Process eid resolver pair {0} time: {1} including {2} round record".format(
                eid_resolver_pair,
                str(date),
                len(round_group))
            )

        # 首先比较 type是否一致
        types_list = list(set(
            [round_obj.type for round_obj in round_group if round_obj.type != 'RoundNoReply']
            )
        )
        logging.debug("The reply type list for eid resolver pair {0} at time {1} is following:{2}".format(
            eid_resolver_pair,
            str(date),
            "|".join(types_list))
        )

        # 首先比较 round的类型，如果5个round的类型不一致，直接return，退出函数（这样节约时间。。。不继续比较了）
        if len(types_list) != 1 and len(types_list) != 0:
            reason = ",".join(list(types_list))
            logger.warning(error_message['type'].format(eid_resolver_pair, str(date), reason))
            res['type_coherent'] = False
            res['coherent'] = False
            return res

        else:
            # 如果进入这个 条件分支，则所有的比较进行完才返回return
            # 其实这个时候 types_list 中也只含有 RoundNormal

            if 'RoundNormal' in types_list:

                tmp = list({round_obj.auth for round_obj in round_group if round_obj.type == 'RoundNormal'})
                if len(tmp) != 1:
                    logger.warning(error_message['auth'].format(eid_resolver_pair, str(date), "|".join(tmp)))
                    res['auth_coherent'] = False
                # 判断 mobile
                tmp = list({round_obj.mobile for round_obj in round_group if round_obj.type == 'RoundNormal'})
                if len(tmp) != 1:
                    logger.warning(error_message['mobile'].format(eid_resolver_pair, str(date), "|".join(tmp)))
                    res['mobile_coherent'] = False

                # 判断locator_count是不是一致
                tmp = list({round_obj.locator_count for round_obj in round_group if round_obj.type == 'RoundNormal'})
                logging.debug("The locator count for eid resolver pair {0} at time {1} is following:{2}".format(
                    eid_resolver_pair,
                    str(date),
                    "|".join(tmp))
                )
                if len(tmp) != 1:
                    reason = "|".join(tmp)
                    logger.warning(error_message['locator_count'].format(eid_resolver_pair, str(date), reason))
                    res['locator_count_coherent'] = False

                # 判断 RLOC addreses是不是一致
                tmp = list({round_obj.rloc_addrs for round_obj in round_group if round_obj.type == 'RoundNormal'})
                logging.debug("The RLOC address set for eid resolver pair {0} at time {1} is following:{2}".format(
                    eid_resolver_pair,
                    str(date),
                    "|".join(tmp))
                )
                if len(tmp) != 1:
                    reason = "|".join(tmp)
                    logger.warning(error_message['RLOC address'].format(eid_resolver_pair, str(date), reason))
                    res['rloc_address_coherent'] = False

                # 判断 Traffic Engineering attributes是不是一致
                tmp = list({round_obj.te_attrs for round_obj in round_group if round_obj.type == 'RoundNormal'})
                logging.debug("The RLOC address set for eid resolver pair {0} at time {1} is following:{2}".format(
                    eid_resolver_pair,
                    str(date),
                    "|".join(tmp))
                )
                if len(tmp) != 1:
                    reason = "|".join(tmp)
                    logger.warning(error_message['TE'].format(eid_resolver_pair, str(date), reason))
                    res['te_coherent'] = False

    # 最后返回一个 包含各种指标比较结果的字典
    if False in res.itervalues():
        res['coherent'] = False
    return res

def get_eid_resolver_sort_list(log_dir):
    # 获取某个vantage试验结果traces的路径
    # 变量 traces_log是在config.py中定义的
    # 获取logDirRoot指定的文件夹下的全部文件名，放入到一个list中
    logFilePathList = os.listdir(log_dir)
    # 将上一步所得的list中所有元素拼接成一个长字符串，存储至target当中
    target = "".join(logFilePathList)
    # 对获得的字符串使用正则表达式，提取文件名中包含的EID以及Resolver值
    res = EID_RESOVLER_P.findall(target)
    eid_set = set([element[0] for element in res])
    resolver_set = set([element[1] for element in res])
    # 对EID，Resolver进行排序，将结果放至list中
    resolvers = sorted(list(resolver_set), key=lambda item: socket.inet_aton(item))
    eids = sorted(list(eid_set), key=lambda item: socket.inet_aton(item))
    return eids, resolvers

def get_eids_resolvers_list_vantages(traces_log):
    # 从5个vantage中获取eid和resolver的list
    # 如果5个vantage中 eid, resolver不一致，那么返回结果为空
    eids = set()
    resolvers = set()
    liege_eids, liege_resolvers = get_eid_resolver_sort_list(TRACES_CSV['liege'])
    eid_number = len(liege_eids)
    resolver_number = len(liege_resolvers)
    for vantage, traces_dir in TRACES_CSV.iteritems():
        tmp_eids, tmp_resolvers = get_eid_resolver_sort_list(traces_dir)
        eids = eids | set(tmp_eids)
        resolvers = resolvers | set(tmp_resolvers)
    if len(eids) <> eid_number or len(resolvers) <> resolver_number:
        # if EID number in liege vantage is different with the union set of all vantage points about EID
        # return empty list
        eids = []
        resolvers = []
    else:
        resolvers = sorted(list(resolvers), key=lambda item: socket.inet_aton(item))
        eids = sorted(list(eids), key=lambda item: socket.inet_aton(item))

    return eids, resolvers

if __name__ == '__main__':
    # 首先确保 5个 vantage 中含有的 eid, resolver是一致的，否则比较没有意义
    # 创建logging对象记录运行日志
    # 参考链接：http://blog.csdn.net/jgood/article/details/4340740
    # http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python

    # 常数, 记录当前文件所在目录
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    print "CURRENT DIRECTORY:", CURRENT_DIR

    # 常数, 根据CURRENT_DIR 构造log文件地址
    LOG_DIR = os.path.join(CURRENT_DIR, 'log')
    print "LOG DIRECTORY", LOG_DIR


    # 读取环境变量PLANETLAB_CSV
    try:

        PLANETLAB_DEV = os.environ['PLANETLAB_CSV']

    except KeyError:

        print "Environment variable PLANETLAB_DEV is not properly defined or the definition about this variable is not" \
              "taken into account."
        print "If PLANETLAB_DEV is well defined, restart Pycharm to try again!"


    # 构造字典，存储所有指向CSV格式的traces的路径
    TRACES_CSV = {

        'liege':   "/".join([PLANETLAB_DEV, 'liege']),
        'ucl':   "/".join([PLANETLAB_DEV, 'ucl']),
        'umass':   "/".join([PLANETLAB_DEV, 'umass']),
        'temple':   "/".join([PLANETLAB_DEV, 'temple']),
        'wiilab':   "/".join([PLANETLAB_DEV, 'wiilab']),

    }

    RESULT_FILE = os.path.join(LOG_DIR, 'comparison_among_vantage_point.csv')

    # 创建logging, 记录程序执行过程
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), 'vantage_level_comparison_log.txt'),
        level=logging.INFO,
        filemode='w',
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    logger = logging.getLogger(__name__)

    eids, resolvers = get_eids_resolvers_list_vantages(TRACES_CSV)

    all_csv_files = []

    for traces_csv_dir in TRACES_CSV.itervalues():
        all_csv_files.extend(glob.glob(traces_csv_dir+'/*.log.csv'))

    csv_file_dict = {}
    for eid in eids:
        for resolver in resolvers:

            csv_file_dict[(eid, resolver)] = []

    for csv_file in all_csv_files:
        # EID_RESOVLER_P.findall(csv_file) returns a list of tuple
        # The result may be in format [('0.0.0.0', '193.162.145.50')]
        eid_resolver_pair = EID_RESOVLER_P.findall(csv_file)[0]
        if eid_resolver_pair:
            csv_file_dict[eid_resolver_pair].append(LogFile(csv_file))

    is_all_resolver_coherent_for_eid(RESULT_FILE, csv_file_dict, logger)


















