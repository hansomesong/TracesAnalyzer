# -*- coding: utf-8 -*-
'''In this python script, we plan to define some globl variables'''


import os
csv_file_destDir = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/'
CSV_ALL_FILE = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/statistic_all.csv'
CSV_FILE_DESTDIR =  '/Users/yueli/Documents/Codes/TracesAnalyzer/log/'

traces_log ={

    'liege' : '/Users/yueli/Documents/Codes/Luigi_Codes/PlanetLab_20140716/liege/mappings',
    'temple' : '/Users/yueli/Documents/Codes/Luigi_Codes/PlanetLab_20140716/temple/mappings',
    'ucl' : '/Users/yueli/Documents/Codes/Luigi_Codes/PlanetLab_20140716/ucl/mappings',
    'umass' : '/Users/yueli/Documents/Codes/Luigi_Codes/PlanetLab_20140716/umass/mappings',
    'wiilab' : '/Users/yueli/Documents/Codes/Luigi_Codes/PlanetLab_20140716/wiilab/mappings'

}

# csv_file_destDir = '/Users/yueli/Documents/Codes/TracesAnalyzer/test_log/'
# CSV_ALL_FILE = '/Users/yueli/Documents/Codes/TracesAnalyzer/test_log/statistic_all.csv'
# CSV_FILE_DESTDIR =  '/Users/yueli/Documents/Codes/TracesAnalyzer/test_log/'
#
# traces_log ={
#
#     'liege' : '/Users/yueli/Documents/Codes/PlanetLab_test/liege/mappings',
#     'temple' : '/Users/yueli/Documents/Codes/PlanetLab_test/temple/mappings',
#     'ucl' : '/Users/yueli/Documents/Codes/PlanetLab_test/ucl/mappings',
#     'umass' : '/Users/yueli/Documents/Codes/PlanetLab_test/umass/mappings',
#     'wiilab' : '/Users/yueli/Documents/Codes/PlanetLab_test/wiilab/mappings'
#
# }

# f = os.path.dirname(os.path.realpath(__file__))
# print f

# 需要想一个更高效的办法 要不然 这样每次都要修改路径 太麻烦了。。
if not os.path.isdir("log"):
    os.makedirs("log")

# csv_file_destDir = '/Users/qsong/Documents/yueli/TracesAnalyzer/log/'
# CSV_ALL_FILE = '/Users/qsong/Documents/yueli/TracesAnalyzer/log/statistic_all.csv'
# CSV_FILE_DESTDIR =  '/Users/qsong/Documents/yueli/TracesAnalyzer/log/'
# #
#
# traces_log ={
#      'liege' : '/Users/qsong/Documents/PlanetLab/liege/mappings',
#      'temple' : '/Users/qsong/Documents/PlanetLab/temple/mappings',
#      'ucl' : '/Users/qsong/Documents/PlanetLab/ucl/mappings',
#      'umass' : '/Users/qsong/Documents/PlanetLab/umass/mappings',
#      'wiilab' : '/Users/qsong/Documents/PlanetLab/wiilab/mappings'
# }