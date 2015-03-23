# -*- coding: utf-8 -*-
# 利用多进程技术, 批量转化log traces为CSV格式的traces
__author__ = 'qsong'

import os
import glob
import time
import multiprocessing as mp
from utility.RoundInstanceFactory import *

def worker(csv_traces_dir, log_file_full_path):

    r = RoundInstanceFactory(log_file_full_path)
    csv_file_path = csv_traces_dir+"/"+os.path.basename(log_file_full_path)+".csv"
    r.write2csv(csv_file_path)


def main(csv_traces_dir, traces_log_dir):
    pool = mp.Pool(mp.cpu_count()+12)
    jobs = []
    for csv_file_name in glob.glob(traces_log_dir+'/*.log'):
            #print csv_file_name
            job = pool.apply_async(worker, (csv_traces_dir, csv_file_name,))
            jobs.append(job)

    #collect results from the workers through the pool result queue
    for job in jobs:
        job.get()

    pool.close()


if __name__ == '__main__':

    # 获取程序开始时间
    start_time = time.clock()

    try:
        PLANETLAB_DEV = os.environ['PLANETLAB_CSV']
        PLANETLAB  = os.environ['PLANETLAB']

    except KeyError:
        print "Environment variable PLANETLAB_CSV is not properly defined or the definition about this variable is not" \
              "taken into account."
        print "If PLANETLAB_CSV is well defined, restart Pycharm to try again!"


    # 构造字典，存储所有指向CSV格式的traces的路径
    TRACES_CSV ={
        'liege':   "/".join([PLANETLAB_DEV, 'liege']),
        'temple':   "/".join([PLANETLAB_DEV, 'temple']),
        'ucl':   "/".join([PLANETLAB_DEV, 'ucl']),
        'umass':   "/".join([PLANETLAB_DEV, 'umass']),
        'wiilab':   "/".join([PLANETLAB_DEV, 'wiilab'])
    }

    TRACES_LOG ={
        'liege':   "/".join([PLANETLAB, 'liege/mappings']),
        'temple':   "/".join([PLANETLAB, 'temple/mappings']),
        'ucl':   "/".join([PLANETLAB, 'ucl/mappings']),
        'umass':   "/".join([PLANETLAB, 'umass/mappings']),
        'wiilab':   "/".join([PLANETLAB, 'wiilab/mappings'])
    }

    for vantage, log_traces_dir in TRACES_LOG.iteritems():
        csv_traces_dir = TRACES_CSV[vantage]
        print "Start to process:", log_traces_dir
        print "Convert log files into csv stored in:", csv_traces_dir
        main(csv_traces_dir, log_traces_dir)

    # 获取程序结束时间
    end_time = time.clock()

    print "Elapsed time:", (end_time-start_time)



