# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 这个script的目的是：
# 第一：统计Map Reply中至少有一个Locator的EID的个数
# 第二：统计Map Reply中至少2个Locator的EID的个数
# 第三：统计所有出现的Locator

from config.config import *

def count_eid_by_nb_locator(file_path, locator_nb):
    '''
        Given a vantage point, count the eid associated with given number locators
        @file_path: the path to the CSV file such as comparison_time_liege.csv
        @locator_nb: the number of locator, such as 1 or 2 even 3

        This method returns a list of EID
    '''
    result = []
    with open(file_path) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp = line.split(";")
            rloc_list = tmp[LOG_TIME_COLUMN['RLOC_set']:]
            # 最后一个元素会含有换行符，删除之
            rloc_list = [element.strip() for element in rloc_list]
            if len(rloc_list) >= locator_nb:
               result.append(tmp[LOG_TIME_COLUMN['eid']])
    # 不要忘记除去list中出现的重复EID
    return list(set(result))

def count_all_locators(file_path):
    '''
        Given a vantage point, count the all present locators
        @file_path: the path to the CSV file such as comparison_time_liege.csv

        This method returns a list of locator
    '''
    result = []
    with open(file_path) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp = line.split(";")
            rloc_list = tmp[LOG_TIME_COLUMN['RLOC_set']:]
            # 最后一个元素会含有换行符，删除之
            rloc_list = [element.strip() for element in rloc_list]
            result.extend(rloc_list)
    # 不要忘记除去list中出现的重复locator
    return list(set(result))


if __name__ == '__main__':
    result1 = []

    for vp in VP_LIST:
        # input file
        rawCSV_file = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))
        result1.extend(count_eid_by_nb_locator(rawCSV_file, 1))

    result1 = list(set(result1))

    print result1
    print len(result1)

    result2 = []

    for vp in VP_LIST:
        # input file
        rawCSV_file = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))
        result2.extend(count_eid_by_nb_locator(rawCSV_file, 2))

    result2 = list(set(result2))

    print result2
    print len(result2)


    result_rloc = []

    for vp in VP_LIST:
    # input file
        rawCSV_file = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))
        result_rloc.extend(count_all_locators(rawCSV_file))

    result_rloc = list(set(result_rloc))

    print result_rloc
    print len(result_rloc)



