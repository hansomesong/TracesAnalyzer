# -*- coding: utf-8 -*-
# This script leverages multiple process technique to accelerate LISP/Planet experimental log file.
# To achieve this, we employ process pool and queue functionality, provided by python.
# The script is coded by inspiring from the following link:
# http://stackoverflow.com/questions/13446445/python-multiprocessing-safely-writing-to-a-file

import multiprocessing as mp
from utility.RoundInstanceFactory import *
from utility.csv_sorter import *
import sys
import timeit

# we need some predefined variables stored in config/config.py, to know such as where store all log files
from config.config import *


# Although many processes could involve in the treatment of log file, we have only one process responsible for
# writing logfile-related entry(a row in the context of CSV file) into the given CSV file. The advantage of this
# is to avoid the concurrence about the write access to target CSV file.
def listener(q):
    with open(csv_file, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel', delimiter=';')
        # 创建 输出 csv文件的 第一行
        spamwriter.writerow(
            [
                'Vantage',
                'Log File Name',
                'EID',
                'Resolver',
                'MAPPING_ENTRY',
                'Coherence',
                'RLOC set Consistence',
                'TE coherent',
                'case',
                'Round Type Set',
                'Different Locator Count',
                'Locators Count Set',
                'Different Locators',
                'Locators set',
                #'Locator count flap',
                #'Locators flap',
                'New Deployement number',
                'case1 change time',
                'case1 change pattern',
                'Case3&4 number',
                'case3&4 change time',
                'case3&4 change pattern',
                'RLOC Set'
            ]
        )

        while 1:
            csv_row = q.get()
            # 如果从 (被N多个进程共享的) result queue 中提取到了 字符串 ‘TERMINATE’，那么结束listener进程
            if csv_row == "TERMINATE":
                break
            spamwriter.writerow(csv_row)

# In our process pool, except the one in charge of writing records into CSV file, all rest processes are used
# to treat log file stored in a certain directory. Every time a process processes a log file, it store the retrieved
# information into a QUEUE data structure, which will be served by listener process.
def worker(vantage, log_file, q):
    '''stupidly simulates long running process'''
    R = RoundInstanceFactory(log_file)
    #csv_row = [arg, R.isRLOCSetCoherent(), R.getRoundTypeSet()]
    csv_row = [vantage, log_file, R.EID, R.resolver]
    csv_row.append(",".join(R.MAPPING_ENTRY)) # Yue added MAPPING_ENTRY into CSV files
    csv_row.append(R.coherent)
    csv_row.append(R.RLOCSetCoherent)  # print 'Locator Count Consistence'
    csv_row.append(R.TECoherent)       # print 'TE coherent'

    csv_row.append(R.case)  # Add judge logfile case

    csv_row.append(",".join(R.round_type_list))   # print 'Round Type List'

    # Here add 2 rows: locator_count_list and locator_list
    csv_row.append(len(R.locator_count_list)) # print 'Different Locators Count'
    csv_row.append(",".join(R.locator_count_list)) # print 'Locators Count Set'

    csv_row.append(len(R.locator_list))    # print 'Different locators'
    csv_row.append(R.getLocatorSet())       # print 'Locators set'

    #Here add 2 rows: locator_count_list and locator_list
    #csv_row.append(R.isLocatorCountFlap())
    #csv_row.append(R.isLocatorsFlap())

    # 显示Case1,3,4的具体变化情况
    # Case1的具体变化情况 nd_number, change_time, pattern = R.statistics_new_deployment()
    csv_row.extend(R.statistics_new_deployment())

    # Case3 & Case4 的具体变化情况 nd_number, change_time, pattern = R.statistics_new_deployment()
    csv_row.extend(R.statistics_Case3_Case4())

    # 这列忘了当时是在干嘛，就先注销了
    # csv_row.append(sys.getsizeof(R))

    # 每列只显示一个RLOC
    csv_row.extend(R.locator_addr_list)

    q.put(csv_row)


def main(vantage, traces_log_dir):
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count()+12)

    #put listener to work first
    watcher = pool.apply_async(listener, (q,))

    #fire off workers
    jobs = []

    for lists in os.listdir(traces_log_dir):
    #Do not forget to verify that the current file to be processed is a real log file
    #Otherwise this program may be collapsed.
        if lists.endswith(".log"):
            lists = os.path.join(traces_log_dir, lists)
            job = pool.apply_async(worker, (vantage, lists, q))
            jobs.append(job)

    #collect results from the workers through the pool result queue
    for job in jobs:
        job.get()

    #Now we are done, kill the listener
    q.put("TERMINATE")
    pool.close()


if __name__ == "__main__":
    # Record the start time of current script
    start_time = timeit.default_timer()

    # Some advices : it is better to implement a single process version to make sure all other things work well
    # then consider to import multiple process support. Otherwise, it is difficult to debug when in problem.
    # For example, I had committed an error in Round.py (super() method is subclass), in this file, it only shows
    # job.get() is empty or similar.
    # We plan to output all generated CSV into a directory named 'log'
    # First, we need to check the existence of "log" directory, if not, create it
    if not os.path.isdir("log"):
        os.makedirs("log")

    # Now we can make that "log" subdirectory is present in current directory
    # We could accordingly to form the full path for our destination directory
    csv_dst_dir = os.path.dirname(os.path.realpath(__file__))+'/log/'

    for vantage, value in TRACES_LOG.items():
        csv_file = csv_dst_dir+'comparison_time_{0}.csv'.format(vantage)
        main(vantage, TRACES_LOG[vantage])

        # Initially, the generated csv file, such as 'statistic_liege.csv' is unsorted.
        # Thus, we call methods defined in python script : utility/csv_sorter.py to sort initial
        # unsorted csv then overwrite the latter.
        write_csv(csv_file, csv_sort_list(csv_file))

    # Then generate a CSV file for all vantage experimental result
    csv_all = []
    for vantage, value in TRACES_LOG.items():
        # Iterate all statistics CSV file for each vantage and retrieve all csv rows into a separate list
        # named 'csv_all'
        csv_file = csv_dst_dir+'comparison_time_{0}.csv'.format(vantage)
        csv_header = csv_sort_list(csv_file)[0]
        csv_all.extend(csv_sort_list(csv_file)[1])


    # 当对所有观测点文件夹结束之后
    # Still need to sort csv_all
    csv_all = sorted(csv_all, key=lambda item: socket.inet_aton(item[2])+socket.inet_aton(item[3]))
    write_csv(CSV_ALL_FILE, [csv_header, csv_all])

    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time



