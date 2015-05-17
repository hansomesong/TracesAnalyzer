# -*- coding: utf-8 -*-
'''In this python script, we plan to define some globl variables'''


import os

# 读取 环境变量 ‘PLANETLAB’ and 'PROJECT_LOG_DIR'
# 上述 环境变量 定义在 工作目录下 .profile中 (也有可能定义在 .bashprofile中)
try:

    PLANET_DIR = os.environ['PLANETLAB']
    CSV_FILE_DESTDIR = os.environ['PROJECT_LOG_DIR']


except KeyError:

    print "Environment variable PLANETLAB is not properly defined or " \
          "the definition about this variable is not taken into account."
    print "If PLANETLAB is well defined, restart Pycharm to try again!"

if not os.path.isdir("log"):
    os.makedirs("log")

# csv_file_destDir = '/Users/qsong/Documents/TracesAnalyzer/log/'
csv_file_destDir = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/'
# CSV_ALL_FILE = '/Users/qsong/Documents/TracesAnalyzer/log/statistic_all.csv'
CSV_ALL_FILE = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/statistic_all.csv'
# CSV_FILE_DESTDIR =  '/Users/qsong/Documents/TracesAnalyzer/log/'
# #
#
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
    'round_type_set':8,
    'change_time': 14
}

LOG_COLUMN ={
    'type': 0,
    'date': 1,
    'eid' : 2,
    'resovler': 3
}