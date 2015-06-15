# -*- coding: utf-8 -*-
# 有点儿意思： 我通过修改我工作目录中的.profile文件添加环境变量$PLANETLAB_CSV,然后运行source .profile使得修改生效
# 然后需要重启Pycharm，使得Pycharm可以读取到刚刚刚添加的变量，不然有可能抛出异常
__author__ = 'yueli'

import os
import logging
import socket
import csv
import glob
import datetime
import multiprocessing as mp
from operator import itemgetter, attrgetter
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
        self.type = csv_row[0]
        self.date = datetime.datetime.strptime("".join(csv_row[1].split(" ")), "%Y-%m-%d%H:%M:%S")
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

class LogFile(object):

    def __init__(self, csv_file, date_list=''):
        # 2015-06-12: 添加一个 可选参数date_list, 其可能的格式为：['2015-07-02', '2015-07-04']
        #如果date_list不为空，那么只把含有 出现在后者中的时间 的Round放入self.rounds之中
        if not date_list:
            self.rounds = sorted(
                [
                    Round(csv_row) for csv_row in self.csv_sort_list(csv_file)
                    # Round(csv_row)构造了一个Round类型的Object,date是其一个attribute(类型为datetime),date()是datetime类型对象
                    # 的一个方法，目的是只返回datetime对象的date部分
                    if Round(csv_row).date.date() in [
                        datetime.datetime.strptime(element, "%Y-%m-%d").date() for element in date_list
                    ]
                ],
                key=lambda item: item.date
            )
        #如若不然，则把CSV log file中所有的Round都放进去
        else:
            self.rounds = sorted(
                [Round(csv_row) for csv_row in self.csv_sort_list(csv_file)],
                key=lambda item: item.date
            )
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



def csv_files_dict(traces_csv_dir, logger):
    """
        input: str, a path to a certain vantage csv format traces directory
        output : dict, key=eid, value = 13 resolvers response files
    """
    eids, resovlers = get_eid_resolver_sort_list(traces_csv_dir)

    # 初始化 返回结果
    # 其可能返回结果：
    # result ={
    #   'eid', [LogFile1, LogFile2, ...]
    # }
    result = {}

    for eid in eids:
        result[eid] = []

    # for csv_file_name in os.listdir(traces_csv_dir):
    # glob.glob(filepath)直接获得就是绝对地址了
    print len(glob.glob(traces_csv_dir+'/*.log.csv'))
    for csv_file_name in glob.glob(traces_csv_dir+'/*.log.csv'):
        # EID_RESOVLER_P.findall(csv_file_name)[0]返回的是一个tuple,
        # 要想获得eid，需要EID_RESOVLER_P.findall(csv_file_name)[0][0]
        # 因为 正则表达式操作有时候不成功，所以应该放到try...except之中
        try:
            eid = EID_RESOVLER_P.findall(csv_file_name)[0][0]
        except Exception:
            logger.critical("Unable to extract EID from file name{0}".format(csv_file_name))
        try:
            result[eid].append(LogFile(csv_file_name))
        except KeyError:
            logger.critical("key of {eid} is not found in result dictionary!!".format(eid=eid))
            print "key of {eid} is not found in result dictionary!!".format(eid=eid)
            exit()

    return result


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
                'EID',
                'Reply_Time_Coherent',
                'Type_Coherent',
                'Auth_Coherent',
                'Mobile_Coherent',
                'Locator_Count_Coherent',
                'RLOC_Address_Coherent',
                'TE_Coherent'
            ]
        )
        for eid, log_file_list in csv_files.iteritems():
            # 返回13个文件中每条记录比较的结果， 字典类型
            res = is_coherent(log_file_list, eid, logger)
            # rloc_coherent 和 te_coherent中间有一项为False的时候就要打印警告信息了
            if not res['coherent']:
                # logging.info(
                #     "EID:{0} Reply time:{1} Type:{2} Auth:{3} Mobile:{4} Locator_count:{5} RLOC address:{6} TE:{7}".format(
                #         eid,
                #         res['reply_time_coherent'],
                #         res['type_coherent'],
                #         res['auth_coherent'],
                #         res['mobile_coherent'],
                #         res['locator_count_coherent'],
                #         res['rloc_address_coherent'],
                #         res['te_coherent']
                #     )
                # )
                writer.writerow([
                        eid,
                        res['reply_time_coherent'],
                        res['type_coherent'],
                        res['auth_coherent'],
                        res['mobile_coherent'],
                        res['locator_count_coherent'],
                        res['rloc_address_coherent'],
                        res['te_coherent']

                ])

def is_coherent_for_given_date(log_file_list, eid, logger, date_list=''):

    """
        2015-06-10: 添加方法 is_coherent_for_given_date 用以处理log file中某些特定日期的实验结果
        input
            log_file_list   : type(list), list of CSV log file path
            eid             : type(str), indicate current processing EID
            logger          : type(logging handler), used for recording debug information
            date_list       : type(list), indicate the interested, optional parameter, default value is vide string
    """
    # 注意本函数中 参数log_file_list代表一个存储文件路径的list, 而函数is_coherent()中的同名参数
    # 代表的其实是 一个包含Log_file类型对象的list
    return is_coherent([LogFile(file_path, date_list) for file_path in log_file_list], eid, logger)




def is_coherent(log_file_list, eid, logger):
    """
        input   : log_file_list     : a list of LogFile object (13 log files in format of CSV)
                : eid               : string, indicate current processing for which EID
                : date_list          : list, duration to be compared, e.x.["2013-05-14 08:00", "2013-05-14 08:30" ]
                : logger            : logging handler, record debug information

        output  : a dictionary of comparison metric and result key-value pair
    """
    logger.debug("Processing {0}".format(eid))
    # 默认 coherent值为True, 一旦有异常情况出现，则返回False, 方法立即结束
    # 因为本方法，只能记录下第一次 各个参与比较的log_file的no-coherence之处，这种做法主要是为了降低 程序的复杂度和对系统资源消耗
    # 如若需要统计错误异常的总次数，则需要修改代码

    # 开头即直接初始化返回的结果，所有的比较指标，默认值都为 True
    res = {
        'coherent': True,
        'round_number_coherent': True,
        'type_coherent': True,
        'reply_time_coherent': True,
        'auth_coherent': True,
        'mobile_coherent': True,
        'locator_count_coherent': True,
        'rloc_address_coherent': True,
        'te_coherent': True

    }

    # 错误信息字典，给出no-coherence的具体原因
    error_message = {
        'round_number': 'The total round number for EID:{0} of is not coherent. Reason:{1}',
        'type': 'The type of rounds for EID:{0} at {1}th trial is not coherent. Reason: {2}',
        'reply_time': 'The reply time of rounds for EID:{0} at {1}th trial is not coherent!!!',
        'auth': 'The auth attirbute of rounds for EID:{0} at {1}th trial is not coherent!!!',
        'mobile': 'The mobile attirbute of rounds for EID:{0} at {1}th trial is not coherent!!!',
        'locator_count': 'The locator_count attirbute of rounds for EID:{0} at {1}th trial is not coherent. Reason: {2}',
        'RLOC address': 'The RLOC address of rounds for EID:{0} at {1}th trial is not coherent. Reason: {2}',
        'TE': 'The traffic engineering related attributes for EID:{0} at {1}th trial is not coherent!!! Reason: {2}'
    }
    # 首先要判断 type是不是一致, 如果不一致，则将coherent改为False
    # 我们需要对比每一个时刻的round的类型，如果在某一时刻不一致，立即退出循环

    # 同时我们也需要确保 每一个log文件含有的round数量是一致的，否则立即退出 因为比较没有意义！！
    tmp = list({len(log_file.rounds) for log_file in log_file_list})
    logging.debug("The common round number for EID:{0} is {1}".format(eid, tmp[0]))
    if len(tmp) != 1:
        reason = "|".join([str(round_number) for round_number in tmp])
        logger.critical(error_message['round_number'].format(eid, reason))
        # 虽然这个时候，方法返回True, 但是没有意义
        res['round_number_coherent'] = False
        res['coherent'] = False
        return res

    # 一旦13个logfile中包含的round数量是一样的，那么随便一个文件的round数量就是round_number
    round_number = list({len(log_file.rounds) for log_file in log_file_list})[0]

    # 要对每一次round进行遍历处理
    for i in range(round_number):
        # 首先比较 type是否一致
        types_list = list(
            set(
                [log_file.rounds[i].type for log_file in log_file_list
                    if log_file.rounds[i].type != 'RoundNoReply' and log_file.rounds[i].type != 'PrintSkipped']
            )
        )
        logging.debug("The type list for EID:{0} at {1}th trial is following:{2}".format(eid, i+1, "|".join(types_list)))

        # 首先比较 round的类型，如果13个round的类型不一致，直接return，退出函数（这样节约时间。。。不继续比较了）
        if len(types_list) != 1 and len(types_list) != 0:
            reason = ",".join(list(types_list))
            logger.warning(error_message['type'].format(eid, i+1, reason))
            res['type_coherent'] = False
            res['coherent'] = False
            return res

        else:
            # 如果进入这个 条件分支，则所有的比较进行完才返回return
            # 其实这个时候 types_list 中也只含有 RoundNormal

            if 'RoundNormal' in types_list:
                # 如果13个回复都是 RoundNormal的话则需要继续比较 locators
                rounds_list = [
                    log_file.rounds[i] for log_file in log_file_list if log_file.rounds[i].type == 'RoundNormal'
                ]

                # 首先比较 13个回复是否一致, 如果时间都不一致，立即停止比较退出函数
                if len({round_obj.date for round_obj in rounds_list}) != 1:
                    logger.warning(error_message['reply_time'].format(eid, i+1))
                    res['reply_time_coherent'] = False

                if len({round_obj.auth for round_obj in rounds_list}) != 1:
                    logger.warning(error_message['auth'].format(eid, i+1))
                    res['auth_coherent'] = False

                if len({round_obj.mobile for round_obj in rounds_list}) != 1:
                    logger.warning(error_message['mobile'].format(eid, i+1))
                    res['mobile_coherent'] = False

                # 判断locator_count是不是一致
                tmp = list({round_obj.locator_count for round_obj in rounds_list})
                logging.debug("The locator count for EID:{0} at {1}th trial is following:{2}".format(eid, i+1, "|".join(tmp)))

                if len(tmp) != 1:
                    reason = "|".join(tmp)
                    logger.warning(error_message['locator_count'].format(eid, i+1, reason))
                    res['locator_count_coherent'] = False

                # 判断 RLOC addreses是不是一致
                tmp = list({round_obj.rloc_addrs for round_obj in rounds_list})
                logging.debug("The RLOC address set for EID:{0} at {1}th trial is following:{2}".format(eid, i+1, "|".join(tmp)))

                if len(tmp) != 1:
                    reason = "|".join(tmp)
                    logger.warning(error_message['RLOC address'].format(eid, i+1, reason))
                    res['rloc_address_coherent'] = False

                # 判断 Traffic Engineering attributes是不是一致
                tmp = list({round_obj.te_attrs for round_obj in rounds_list})
                logging.debug("The RLOC address set for EID:{0} at {1}th trial is following:{2}".format(eid, i+1, "|".join(tmp)))

                if len(tmp) != 1:
                    reason = "|".join(tmp)
                    logger.warning(error_message['TE'].format(eid, i+1, reason))
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


# 参考链接
# http://stackoverflow.com/questions/17035077/python-logging-to-multiple-log-files-from-different-classes
def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(file_handler)
    l.addHandler(stream_handler)


# 工作线程，接受一个vantage，将处理结果写入到CSV文件中
# def worker(csv_result_file, csv_traces_dir, logger):
#     print "xxxxx"
#     is_all_resolver_coherent_for_eid(csv_result_file, csv_traces_dir, logger)


if __name__ == '__main__':
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
        # debug的时候 使用 PLANETLAB_DEBUG
        # 工作的时候 用 PLANETLAB_CSV
        PLANETLAB_DEV = os.environ['PLANETLAB_DEV']

    except KeyError:

        print "Environment variable PLANETLAB_DEV is not properly defined or the definition about this variable is not" \
              "taken into account."
        print "If PLANETLAB_DEV is well defined, restart Pycharm to try again!"


    # 构造字典，存储所有指向CSV格式的traces的路径
    # =========================================== ** =======================================================
    TRACES_CSV = {
        'liege':   "/".join([PLANETLAB_DEV, 'liege']),
        #'ucl':   "/".join([PLANETLAB_DEV, 'ucl']),
        # 'umass':   "/".join([PLANETLAB_DEV, 'umass']),
        # 'temple':   "/".join([PLANETLAB_DEV, 'temple']),
        # 'wiilab':   "/".join([PLANETLAB_DEV, 'wiilab']),

    }

    # 遍历字典 TRACES_CSV的键值，生成字典RESULT_FILE
    # 该字典用以存储 13个Map resolver的比较结果CSV文件路径，该字典可能形式如下
    # RESULT_FILE ={
    #   'liege' : '/Users/qsong/Documents/TracesAnalyzer/log/comparison_map_resolver_in_liege.csv'
    #   ...
    # }
    RESULT_FILE = {}
    for vantage in TRACES_CSV.iterkeys():
        RESULT_FILE[vantage] = os.path.join(LOG_DIR, "comparison_map_resolver_in_{0}.csv".format(vantage))


    # http://sebastianraschka.com/Articles/2014_multiprocessing_intro.html
    # Setup a list of processes that we want to run
    # LOGGING_DICT = {}
    #
    # for vantage, traces_dir in TRACES_CSV.iteritems():
    #     log_name = vantage+'_execution.log'
    #     setup_logger(vantage, os.path.join(LOG_DIR, log_name))
    #     logger = logging.getLogger(log_name)
    #     LOGGING_DICT[vantage] = logger
    #
    # processes = [
    #     mp.Process(
    #         target=worker,
    #         args=(RESULT_FILE[vantage], csv_files_dict(TRACES_CSV[vantage], LOGGING_DICT[vantage]), LOGGING_DICT[vantage])
    #     )
    #             for vantage in TRACES_CSV.iterkeys()
    # ]
    #
    # # Run processes
    # for p in processes:
    #     print "SSSSSSSS"
    #     p.start()
    #
    # # Exit the completed processes
    # for p in processes:
    #     p.join()



    logging.basicConfig(filename=os.path.join(os.getcwd(), 'execution_log.txt'),
                        level=logging.DEBUG,
                        filemode='w',
                        format='%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)

    # 遍历字典TRACES_CSV， 分别处理5个VP文件夹内的所有文件
    for vantage, traces_dir in TRACES_CSV.iteritems():
        # log_name = vantage+'_execution.log'
        # setup_logger(vantage, os.path.join(LOG_DIR, log_name))
        # logger = logging.getLogger(log_name)
        is_all_resolver_coherent_for_eid(RESULT_FILE[vantage], csv_files_dict(traces_dir, logger), logger)

















