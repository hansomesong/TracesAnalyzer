'''In this python scirpt, we plan to define some globle variable'''


import os
csv_file_destDir = '/home/cloud/Documents/Codes/TracesAnalyzer/log/'
CSV_ALL_FILE = '/home/cloud/Documents/Codes/TracesAnalyzer/log/statistic_all.csv'
CSV_FILE_DESTDIR =  '/home/cloud/Documents/Codes/TracesAnalyzer/log/'


traces_log ={

    'liege' : '/home/cloud/Documents/PlanetLab/liege/mappings',
    'temple' : '/home/cloud/Documents/PlanetLab/temple/mappings',
    'ucl' : '/home/cloud/Documents/PlanetLab/ucl/mappings',
    'umass' : '/home/cloud/Documents/PlanetLab/umass/mappings',
    'wiilab' : '/home/cloud/Documents/PlanetLab/wiilab/mappings'

}


# f = os.path.dirname(os.path.realpath(__file__))
# print f


if not os.path.isdir("log"):
    os.makedirs("log")