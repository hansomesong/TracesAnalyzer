# -*- coding: utf-8 -*-
'''In this python script, we plan to define some globl variables'''


import os
import datetime

# 读取 环境变量 ‘PLANETLAB’ and 'PROJECT_LOG_DIR'
# 上述 环境变量 定义在 工作目录下 .profile中 (也有可能定义在 .bashprofile中)
try:
    # $HOME/Documents/Codes/TracesAnalyzer/log
    CSV_FILE_DESTDIR = os.environ['PROJECT_LOG_DIR']
    # $HOME/Documents/Codes/PlanetLab_CSV
    PLANET_CSV_DIR = os.environ['PLANETLAB_CSV']
    # $HOME/Documents/Codes/Luigi_Codes/PlanetLab_20140716
    PLANET_DIR = os.environ['PLANETLAB']
    # 存储 生成CSV文件的路径
    # $HOME/Documents/Codes/TracesAnalyzer/Plot
    PLOT_DIR = os.environ['PROJECT_PLOT_DIR']


except KeyError:

    print "Environment variable PLANETLAB is not properly defined or " \
          "the definition about this variable is not taken into account."
    print "If PLANETLAB is well defined, restart Pycharm to try again!"

# csv_file_destDir = '/Users/qsong/Documents/TracesAnalyzer/log/'
# csv_file_destDir = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/'

CSV_ALL_FILE = os.path.join(CSV_FILE_DESTDIR, 'statistic_all.csv')

VP_LIST = ["liege", "temple", "ucl", "umass", "wiilab"]
# VP_LIST = ["wiilab"]

TRACES_LOG=\
{
    'liege'      : os.path.join(PLANET_DIR, 'liege', 'mappings'),
    'temple'     : os.path.join(PLANET_DIR, 'temple', 'mappings'),
    'ucl'       : os.path.join(PLANET_DIR, 'ucl', 'mappings'),
    'umass'     : os.path.join(PLANET_DIR, 'umass', 'mappings'),
    'wiilab'    : os.path.join(PLANET_DIR, 'wiilab', 'mappings')
}

# Describe corresponding relationship between column name and digital index
# in files such as 'comparison_time_<VANTAGE>.csv'
LOG_TIME_COLUMN ={
    'vantage': 0,
    'log_file_name': 1,
    'eid': 2,
    'resolver': 3,
    'mapping_entry': 4,
    'coherence': 5,
    'rloc_set_coherence': 6,
    'te_coherence': 7,
    'case': 8,
    'round_type_set':9,
    'different_locator_count': 10,
    'locators_count_set': 11,
    'different_locators': 12,
    'locators_set': 13,
    'new_deployment_number': 14,
    'case1_change_time': 15,
    'case1_change_pattern': 16,
    'case3_4_number': 17,
    'case3_4_change_time': 18,
    'case3_4_change_pattern': 19,
    'RLOC_set': 20
}


# 对应文件PlanetLab_CSV中：planetlab1-EID-0.0.0.0-MR-198.6.255.40.log.csv 中 每一列代表什么
LOG_COLUMN ={

    'round_type': 0,
    'date': 1,
    'eid' : 2,
    'resovler': 3,
    'request_src': 4,
    'request_dst': 5,
    'request_for': 6,
    'reply_src': 7,
    'rtt': 8,
    'locator_count': 9,
    'mapping_entry': 10,
    'ttl': 11,
    'auth': 12,
    'mobile': 13,
    'locator_id': 14,
    'locator_address': 15,
    'locator_state': 16,
    'locator_priority': 17,
    'locator_weight': 18

}

MR_LIST = [
    "149.20.48.61",
    "149.20.48.77",
    "173.36.254.164",
    "193.162.145.50",
    "195.50.116.18",
    "198.6.255.37",
    "198.6.255.40",
    "202.51.247.10",
    "202.214.86.252",
    "206.223.132.89",
    "217.8.97.6",
    "217.8.98.42",
    "217.8.98.46"
]

LOG_PREFIX ={
    'liege'      : 'planetlab1',
    'temple'     : 'planetlab2',
    'ucl'       : 'onelab1',
    'umass'     : 'planetlab2',
    'wiilab'    : 'planetlab2'
}

# 该字典对于 resolver_comparator.py 特别有用。。。
ERROR_MESSAGE = {
    'round_number': 'The total round number for EID:{0} of is not coherent. Reason:{1}',
    'type': 'The type of rounds for EID:{0} at {1}th trial is not coherent. Reason: {2}',
    'reply_time': 'The reply time of rounds for EID:{0} at {1}th trial is not coherent!!!',
    'auth': 'The auth attirbute of rounds for EID:{0} at {1}th trial is not coherent!!!',
    'mobile': 'The mobile attirbute of rounds for EID:{0} at {1}th trial is not coherent!!!',
    'locator_count': 'The locator_count attirbute of rounds for EID:{0} at {1}th trial is not coherent. Reason: {2}',
    'RLOC address': 'The RLOC address of rounds for EID:{0} at {1}th trial is not coherent. Reason: {2}',
    'TE': 'The traffic engineering related attributes for EID:{0} at {1}th trial is not coherent!!! Reason: {2}'
}

# 设定实验开始和结束的时间
START_TIME = datetime.datetime.strptime("02/07/2013  07:30:23", "%d/%m/%Y %H:%M:%S")


# if __name__ == 'main':
#     print "Path of Planet log files directory:", PLANET_DIR
#     print "Path of processed log files directory:", CSV_FILE_DESTDIR
