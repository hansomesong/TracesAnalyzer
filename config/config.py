'''In this python script, we plan to define some globl variables'''


import os
csv_file_destDir = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/'
CSV_ALL_FILE = '/Users/yueli/Documents/Codes/TracesAnalyzer/log/statistic_all.csv'
CSV_FILE_DESTDIR =  '/Users/yueli/Documents/Codes/TracesAnalyzer/log/'

traces_log ={

    'liege' : '/Users/yueli/Documents/Codes/PlanetLab/liege/mappings',
    'temple' : '/Users/yueli/Documents/Codes/PlanetLab/temple/mappings',
    'ucl' : '/Users/yueli/Documents/Codes/PlanetLab/ucl/mappings',
    'umass' : '/Users/yueli/Documents/Codes/PlanetLab/umass/mappings',
    'wiilab' : '/Users/yueli/Documents/Codes/PlanetLab/wiilab/mappings'

}
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


if not os.path.isdir("log"):
    os.makedirs("log")