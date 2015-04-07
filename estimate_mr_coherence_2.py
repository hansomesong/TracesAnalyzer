# -*- coding: utf-8 -*-
__author__ = 'qsong'
# 本脚本用来衡量 13个Map resolver在发生new depolyment事件情况下的一致性情况
# 所谓一致性，是指在任一时刻，当

import os
import logging
import collections
import datetime
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    # 读取环境变量 ‘PROJECT_LOG_DIR’ (此变量定义在工作目录下.profile或者.bashprofile)
    try:
        LOG_DIR = os.environ['PROJECT_LOG_DIR']
    except KeyError:
        print "Environment variable PROJECT_LOG_DIR is not properly defined or " \
              "the definition about this variable is not taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"

    # 定义字典，存储需要读入的文件
    # 注意：所以本脚本的执行依赖于读入文件(comparison_time_liege.csv,etc.)的格式
    # 如果有朝一日，csv文件格式改变，本脚本也许需要做些修改
    input_logs = {
        'liege': os.path.join(LOG_DIR, 'comparison_time_liege.csv'),
        'temple': os.path.join(LOG_DIR, 'comparison_time_temple.csv'),
        'ucl': os.path.join(LOG_DIR, 'comparison_time_ucl.csv'),
        'umass': os.path.join(LOG_DIR, 'comparison_time_umass.csv'),
        'wiilab': os.path.join(LOG_DIR, 'comparison_time_wiilab.csv')
    }

    # 利用Python logging模块，记录脚本运行信息，有利于debug...
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), 'execution_log.txt'),
        level=logging.DEBUG,
        filemode='w',
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.debug(input_logs)

    # 定义字典MRs, 键值是13个Map resolver的IP地址
    MRs = {
        '149.20.48.61': [],
        '149.20.48.77': [],
        '173.36.254.164': [],
        '193.162.145.50': [],
        '195.50.116.18': [],
        '198.6.255.37': [],
        '198.6.255.40': [],
        '202.51.247.10': [],
        '202.214.86.252': [],
        '206.223.132.89': [],
        '217.8.97.6': [],
        '217.8.98.42': [],
        '217.8.98.46': []
    }

    # 以下循环，是本脚本的关键部分
    # 基本想法是： 因为诸如comparison_time_<VANTAGE_NAME>.csv之类的文件中，已经记录了每个文件中发生new deployement的时刻
    # 现在需要统计每一个MP resolver，在5个vantage下，613个EID中所有的new deployment的时刻
    # 最理想的情况就是，在任一时刻，13个MR观察到的new deployment数目是一致的
    for vantage_name, log_file in input_logs.iteritems():
        # print vantage_name, log_file
        with open(log_file) as f_handler:
            f_handler.next()
            for line in f_handler:
                tmp = line.split(";")
                # tmp =
                # vantage, file_name, eid, resovler, coherence, RLOC_set,
                # print tmp[3]
                # 不考虑时间的秒位
                mp_resolver = tmp[3]
                change_time = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                               for x in tmp[13].split(",") if x != '0']
                change_time = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M")
                               for x in change_time]
                MRs[mp_resolver].extend(change_time)

        # MRs[mp_resolver] = map(
        #     lambda x: (int((x[0]-datetime.datetime(2013, 7, 2, 7, 30)).total_seconds()/1800+1), x[1]), MRs[mp_resolver]
        # )


    # 填充那些没有 new deployment的时间点
    for mp_resolver in MRs:
        MRs[mp_resolver] = sorted(collections.Counter(MRs[mp_resolver]).most_common(), key=lambda t: t[0])
        print MRs[mp_resolver]
        logger.debug("Date time format")
        logger.debug(mp_resolver+'-->'+", ".join([x.strftime("%d/%m/%Y %H:%M") for x in [y[0] for y in MRs[mp_resolver]]]))
        MRs[mp_resolver] = map(
            lambda x: (int((x[0]-datetime.datetime(2013, 7, 2, 7, 30)).total_seconds()/1800+1), x[1]), MRs[mp_resolver]
        )
        logger.debug("Experiment number format")
        logger.debug(mp_resolver+'-->'+", ".join([str(x[0]) for x in MRs[mp_resolver]]))

        nd_exp_number = set([x[0] for x in MRs[mp_resolver]])
        diff_exp_number = list(set(range(1, 803, 1)).difference(nd_exp_number))
        diff_time_nb_pair = [(x, 0) for x in diff_exp_number]
        MRs[mp_resolver].extend(diff_time_nb_pair)
        MRs[mp_resolver] = sorted(MRs[mp_resolver], key=lambda t: t[0])
        logger.debug("After fullfilment")
        logger.debug(mp_resolver+'-->'+", ".join([str(x[0]) for x in MRs[mp_resolver]]))

    # 将MRs的value转化为numpy.array类型，以便于求均值方差
    tmp = []
    for mr in MRs:
        tmp.append([x[1] for x in MRs[mr]])
    tmp = np.array(tmp).transpose()
    for line in tmp:
        logger.debug(" ".join(["{0:2s}".format(str(x)) for x in line]))

    print len(tmp)

    # 将802个时刻每个时刻的new deployement number视为一个随机变量，每个随机变量有13个sample
    vars = []
    means = []
    for mr_line in tmp:
        vars.append(np.var(mr_line))
        means.append(np.mean(mr_line))

    # 将802个实验时刻对应的 随机变量均值、方差画图
    plt.figure(1)
    x_axis = range(1, 803, 1)
    plt.plot(x_axis, means, 'r')
    plt.bar(x_axis, vars, width=0)
    plt.xlim(0, max(x_axis)+4)
    plt.ylim(0, max(vars)+5)
    plt.grid()
    plt.show()
















