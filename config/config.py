# -*- coding: utf-8 -*-
'''In this python script, we plan to define some globl variables'''


import os

# 读取 环境变量 ‘PLANETLAB’ and 'PROJECT_LOG_DIR'
# 上述 环境变量 定义在 工作目录下 .profile中 (也有可能定义在 .bashprofile中)
try:

    PLANET_DIR = os.environ['PLANETLAB']
    PLANET_CSV_DIR = os.environ['PLANETLAB_CSV']
    # 存储 生成CSV文件的路径
    PLOT_DIR = os.environ['PROJECT_PLOT_DIR']
    CSV_FILE_DESTDIR = os.environ['PROJECT_LOG_DIR']

except KeyError:

    print "Environment variable PLANETLAB is not properly defined or " \
          "the definition about this variable is not taken into account."
    print "If PLANETLAB is well defined, restart Pycharm to try again!"

# # csv_file_destDir = '/Users/qsong/Documents/TracesAnalyzer/log/'
# csv_file_destDir = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/'

CSV_ALL_FILE = os.path.join(CSV_FILE_DESTDIR, 'statistic_all.csv')

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

# if __name__ == 'main':
#     print "Path of Planet log files directory:", PLANET_DIR
#     print "Path of processed log files directory:", CSV_FILE_DESTDIR
