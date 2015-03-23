# -*- coding: utf-8 -*-
from config.config import *
from utility.REPattern_opt import *

import csv
import os
import sys
sys.path.append('../')
import socket
from utility.RoundInstanceFactory import *
#from csv_sorter import *

# 定义Logfile class
# 因为试验是对任意一个EID，向13个MAP Resolver进行询问，结果分别存至13个logfile.
# 判断13个MAP resolver的回复是否一致，可以通过13个Logfile instance来进行。。


class LogFile(object):
    """
        CSV文件的每一行都可以用来生成一个Logfile类型的对象
    # """
    # def __init__(self,
    #              vantage, file_path, eid, resolver, coherent, RLOC_set_coherent, TE_coherent, round_type_list,
    #              locators_str
    # ):
    def __init__(self, csv_row):
        # Instance attribute 'vantage' stores the name of the vantage point
        self.vantage = csv_row[0]
        # Instance attribute 'file_path' stores the absolute path to this log file
        self.file_path = csv_row[1]
        self.eid = csv_row[2]
        self.resolver = csv_row[3]
        self.coherent = csv_row[4]
        self.RLOC_set_coherent = csv_row[5]
        self.TE_coherent = csv_row[6]
        self.round_type_list = csv_row[7].split(',')
        # A sorted list including all locator addressses appeared in a logfile.
        # This list could be empty if the target logfile does not contain RoundNormal type round
        self.locators_str = csv_row[11]

    def __repr__(self):
        return "{0};{1};{2};{3};{4};{5}".format(
            self.vantage, self.file_path, self.eid, self.resolver, self.round_type_list, self.locators_str
        )


def csv_sort_list(csv_file, delimiter=';'):
    """Read target csv file into a list and return a sorted list to be written"""
    with open(csv_file, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)

        # Do not forget to convert "reader" into list type, sorted works uniquely for list type.
        csv_cont_list = list(reader)

        # Respectively store csv file's header and content into a separate list
        csv_header = csv_cont_list[0]
        csv_body = csv_cont_list[1:]

        # Firstly, sort all csv rows according to (EID, resolver) pair. Here we rely on python lambda technique
        # and socket module's inet_aton function. Ask for google for more information
        # An example of csv_body element:
        # liege;/Users/qsong/Documents/PlanetLab/liege/mappings/planetlab1-EID-0.0.0.0-MR-149.20.48.61.log;
        # 	0.0.0.0;149.20.48.61;TRUE;TRUE;TRUE;NegativeReply,RoundNoReply;0;0;0
        # EID 和 Resolver分别占据第三四列 (如果输出CSV文件格式有变，则EID和Resolver的index有可能会发生变化)
        csv_body = sorted(csv_body, key=lambda item: socket.inet_aton(item[2])+socket.inet_aton(item[3]))
        return [csv_header, csv_body]

def csv_logfile_list(csv_file, delimiter=';'):
    """Convert input csv_file as a list of logfile instance"""
    with open(csv_file, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)

        # Do not forget to convert "reader" into list type, sorted works uniquely for list type.
        csv_cont_list = list(reader)
        csv_body = csv_cont_list[1:]

        # Firstly, sort all csv rows according to (EID, resolver) pair. Here we rely on python lambda technique
        # and socket module's inet_aton function. Ask for google for more information
        # An example of csv_body element:
        # liege;/Users/qsong/Documents/PlanetLab/liege/mappings/planetlab1-EID-0.0.0.0-MR-149.20.48.61.log;
        # 	0.0.0.0;149.20.48.61;TRUE;TRUE;TRUE;NegativeReply,RoundNoReply;0;0;0
        # EID 和 Resolver分别占据第三四列 (如果输出CSV文件格式有变，则EID和Resolver的index有可能会发生变化)
        csv_body = sorted(csv_body, key=lambda item: socket.inet_aton(item[2])+socket.inet_aton(item[3]))
        return [LogFile(csv_row) for csv_row in csv_body]



def write_csv(dest_csv, csv_cont):
    """ Writes a semicolon-delimited CSV file."""
    with open(dest_csv, 'wb') as out_file:
        writer = csv.writer(out_file, delimiter=';')
        writer.writerow(csv_cont[0])
        for row in csv_cont[1]:
            writer.writerow(row)


def get_locator_list_by_vantage_eid_resolver(csv_body_list, vantage, eid, resolver):
    for csv_row in csv_body_list:
        # csv_row is a list whose content is like: (2015-1-13)
        # liege 第一列
        # /Users/qsong/Documents/PlanetLab/liege/mappings/planetlab1-EID-37.77.56.64-MR-149.20.48.61.log 第二列
        # 37.77.56.64	149.20.48.61	第三，四列
        # TRUE	TRUE	TRUE	第五六七列
        # RoundNormal,RoundNoReply	第八列
        # 1	3	第九十列
        # 3	    第十一列
        # LOCATOR0=87.195.196.77,LOCATOR0_STATE=up,LOCATOR0_PRIORITY=50,LOCATOR0_WEIGHT=100#LOCATOR1=95.97.83.93,LOCATOR1_STATE=up,LOCATOR1_PRIORITY=10,LOCATOR1_WEIGHT=100#LOCATOR2=2001:9e0:8500:b00::1,LOCATOR2_STATE=up,LOCATOR2_PRIORITY=50,LOCATOR2_WEIGHT=100
        # 0	    第十三列 (表示case的取值)
        # 87.195.196.77	第十四列
        # 95.97.83.93	第十五咧
        # 2001:9e0:8500:b00::1	第十六列
        if eid in csv_row and resolver in csv_row and vantage in csv_row:
            # 目前，RLOC Address Set在CSV文件中，是从第十四列开始的，index=13
            return csv_row[13:]


def get_eid_resolver_sort_list(vantage_name):
    # 获取某个vantage试验结果traces的路径
    # 变量 traces_log是在config.py中定义的
    logDirRoot = traces_log[vantage_name]
    # 获取logDirRoot指定的文件夹下的全部文件名，放入到一个list中
    logFilePathList = os.listdir(logDirRoot)
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

if __name__ == '__main__':
    # for vantage_name, value in traces_log.items():
    #     # Iterate all statistics CSV file for each vantage and retrieve all csv rows into a separate list
    #     # named 'csv_all'
    #     eids, resolvers = get_eid_resolver_sort_list(vantage_name)
    #     csv_file = CSV_FILE_DESTDIR+'comparison_time_{0}.csv'.format(vantage_name)
    #     csv_header = csv_sort_list(csv_file)[0]
    #     csv_body = csv_sort_list(csv_file)[1]
    #
    #     with open(CSV_FILE_DESTDIR+'comparison_map_resolver_in_{0}.csv'.format(vantage_name), 'wb') as cf:
    #         spamwriter = csv.writer(cf, dialect='excel', delimiter=';')
    #         spamwriter.writerow(['Vantage', 'EID', 'Locator Count Consistence'])
    #         # Define a set to store RLOC addre
    #         # ==================
    #
    #         # ==================
    #         locator_addr_set = set()
    #         for eid in eids:
    #             # Initially, we consider locator_addr_consistence is True
    #             # Then iterate all 13 different resolvers to get respective locator address set
    #             # If one (eid, resolver) pair returns a different locator address set other than the one returned by
    #             # pair(eid, resolvers[0]), we change the flag 'locator_addr_consistence' into false ane break.
    #             locator_addr_consistence = True
    #
    #             # For each eid, firstly choose the a comparison reference
    #             eid_locator_addr_set = set(
    #                 get_locator_list_by_vantage_eid_resolver(csv_body, vantage_name, eid, resolvers[0])
    #             )
    #             for resolver in resolvers[1:]:
    #                 if eid_locator_addr_set != set(get_locator_list_by_vantage_eid_resolver(csv_body, vantage_name, eid, resolver)):
    #                     locator_addr_consistence = False
    #                     break
    #             spamwriter.writerow([vantage_name, eid, locator_addr_consistence])
    #
    #
    # # 以下部分代码，用以对5个vantage point的traces进行比价，并将比较结果写入到CSV文件中
    # # Analyze statistic_all.csv to verify that for the same (eid, resolver) pair, all 5 vantage points have seen the
    # # same result.
    # target_csv = CSV_FILE_DESTDIR+'statistic_all.csv'
    # eids, resolvers = get_eid_resolver_sort_list('liege')
    #
    # csv_body = csv_sort_list(target_csv)[1]
    #
    # with open(CSV_FILE_DESTDIR+'comparison_among_vantage_point.csv', 'wb') as cf:
    #     spamwriter = csv.writer(cf, dialect='excel', delimiter=';')
    #     spamwriter.writerow(['EID', 'Resolver', 'Locator Count Consistence'])
    #     # Define a set to store RLOC addre
    #     locator_addr_set = set()
    #     for eid in eids:
    #         # Initially, we consider locator_addr_consistence is True
    #         # Then iterate all 13 different resolvers to get respective locator address set
    #         # If one (eid, resolver) pair returns a different locator address set other than the one returned by
    #         # pair(eid, resolvers[0]), we change the flag 'locator_addr_consistence' into false ane break.
    #         for resolver in resolvers:
    #             # choose liege vantage's as comparison reference.
    #             locator_addr_consistence = True
    #             #print eid, resolver
    #             eid_locator_addr_set = set(get_locator_list_by_vantage_eid_resolver(csv_body, 'liege', eid, resolver))
    #             for vantage_name in traces_log.keys():
    #                 if eid_locator_addr_set != set(get_locator_list_by_vantage_eid_resolver(csv_body, vantage_name, eid, resolver)):
    #                     locator_addr_consistence = False
    #                     break
    #             spamwriter.writerow([eid, resolver, locator_addr_consistence])
    for vantage_name, value in traces_log.items():
        # Iterate all statistics CSV file for each vantage and retrieve all csv rows into a separate list
        # named 'csv_all'
        eids, resolvers = get_eid_resolver_sort_list(vantage_name)

        print len(eids)

        csv_file = CSV_FILE_DESTDIR+'comparison_time_{0}.csv'.format(vantage_name)

        logfile_list = csv_logfile_list(csv_file)
        logfile_dict = dict()
        for eid in eids:
            logfile_dict[eid] =[]
            for logfile in logfile_list:
                if logfile.eid == eid:
                    logfile_dict[eid].append(logfile)

        # grouped_logfile_list = [[logfile] for eid in eids for logfile in logfile_list if logfile.eid == eid]
        for eid in eids:

            print len(logfile_dict[eid])

        for eid, logfiles in logfile_dict.iteritems():
            coherent = True
            logfile.round_type_list = [round_type for logfile in logfiles for round_type in logfile.round_type_list
                                           if round_type != 'RoundNoReply'
            ]
            print logfile







        # print len(grouped_logfile_list[0])
        #
        # for logfile in logfile_list:
        #     print logfile











