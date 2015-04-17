# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 本脚本用来衡量 13个Map resolver在发生new depolyment事件情况下的一致性情况
# 所谓一致性，是指在任一时刻，当

import os
import logging
import collections
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl

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
                               for x in tmp[13].split(",") if x != '0'] # strptime把字符串格式改写成datatime格式；strftime把datatime格式改写成字符串格式
                change_time = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M")
                               for x in change_time]
                MRs[mp_resolver].extend(change_time) # 给13个不同的MR分别加入datatime格式的change time


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
            # lambda x: (int((x[0]-datetime.datetime(2013, 7, 2, 7, 30)).total_seconds()/1800+1), x[1]/613.0/5.0), MRs[mp_resolver]
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
    for i, line in enumerate(tmp):
        logger.debug("{0:4s}:".format(str(i+1))+" ".join(["{0:4s}".format(str(x)) for x in line]) + "| {0:4s}:".format(str(np.mean(line))))

    print len(tmp)


    # 将802个时刻每个时刻的new deployement number视为一个随机变量，每个随机变量有13个sample
    vars = []
    stds = [] ######
    means = []
    for mr_line in tmp:
        vars.append(np.var(mr_line))
        stds.append(np.std(mr_line)) ######
        means.append(np.mean(mr_line))

    stds_p = list(map(lambda x: x[0]+x[1], zip(means, stds)))
    stds_n = list(map(lambda x: x[0]-x[1], zip(means, stds)))

    # To test the periodicity
    print means
    print "Mean_means =", np.mean(means)
    print "Mean_stds =", np.mean(stds)
    print "Mean_means + 2*Mean_stds:", np.mean(means) + 2*np.mean(stds)

    xxx = [index_value+1 for index_value, mean_value in enumerate([np.mean(line) for line in tmp]) if mean_value >= (np.mean(means) + 2*np.mean(stds))]
    print xxx

    mean_means = []
    for i in range(0, 802):
        mean_means.append(np.mean(means))
    print "length of mean_means:", mean_means.__len__()

    mean_stds = []
    for i in range(0, 802):
        mean_stds.append(np.std(means))
    print "length of mean_stds:", mean_stds.__len__()

    mean_2std_blue =[]
    for i in range(0, 802):
        mean_2std_blue.append(np.mean(means) + 2*np.mean(stds))
    print "length of mean_2std_blue:", mean_2std_blue.__len__()
    # mean_2std_blue = list(map(lambda x: x[0]+2*x[1], zip(mean_means, mean_stds)))
    print "mean_2std_blue:", mean_2std_blue

    # 快速傅立叶变换
    sampling_rate = 1
    fft_size = 802
    x_axis = range(1, 803, 1) # 时间点
    means_fourier = np.fft.rfft(means)/fft_size # 对实数信号进行FFT计算, 为了正确显示波形能量，还需要将rfft函数的结果除以fft_size
    freqs = np.linspace(0, 1024, fft_size/2+1) # rfft函数的返回值是N/2+1个复数，分别表示从0(Hz)到sampling_rate/2(Hz)的N/2+1点频率的成分, 频域上的x轴
    # xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100)) # 计算每个频率分量的幅值，并通过 20*np.log10() 将其转换为以db单位的值。为了防止0幅值的成分造成log10无法计算，我们调用np.clip对xf的幅值进行上下限处理
    means_fp = np.abs(means_fourier)


    # pl.figure(figsize=(8,4))
    # pl.subplot(211)
    # pl.plot(x_axis, means, c="red")
    # pl.xlim(0, 802)
    # pl.xlabel("Experiment number")
    # plt.ylabel("Mean of numbers of change")
    # pl.title("Waveform and spectrum for numbers of change")
    #
    # pl.subplot(212)
    # pl.plot(freqs, means_fp, c="blue")
    # pl.xlim(0, 1024)
    # pl.xlabel("Frequency (Hz)")
    # pl.subplots_adjust(hspace=0.4)
    # pl.show()

    # Autocorrelation
    def autocorrelation(x,lags): #计算lags阶以内的自相关系数，返回lags个值，分别计算序列均值，标准差
        n = len(x)
        x = np.array(x)
        result = [np.correlate(x[i:]-x[i:].mean(),x[:n-i]-x[:n-i].mean())[0]\
            /(x[i:].std()*x[:n-i].std()*(n-i)) \
            for i in range(1,lags+1)]
        return result

    correlation_result = autocorrelation(means, fft_size-2)
    print "correlation_result:", correlation_result
    plt.plot(np.linspace(1, 800, 800), correlation_result)
    plt.xlabel("Order from 1 to (experiment number - 1)")
    plt.ylabel("Range of Autocorrelation")
    plt.title("Test of periodicity by using Autocorrelation")



    # # 将802个实验时刻对应的 随机变量均值、方差画图
    # plt.figure(1)
    # x_axis = range(1, 803, 1)
    # plt.plot(x_axis, means, color='red')
    # # # plt.bar(x_axis, stds, color='black', width=0)
    # # plt.plot(x_axis, stds_p, color='black')
    # # plt.plot(x_axis, stds_n, color='black')
    # plt.plot(x_axis, mean_2std_blue, color='blue')
    # # print "means =", means
    # # print "stds =", stds
    # # print "stds_p =", stds_p
    # # print "stds_n =", stds_n
    # # # plt.bar(x_axis, vars, width=0) #####
    # # # plt.ylim(min(stds_n)-1, max(stds_p)+1)
    # plt.xlim(0, x_axis.__len__())
    # plt.xlabel("Experiment number")
    # plt.ylabel("Mean of numbers of change")
    # plt.title("Test of periodicity")
    # plt.grid()
    plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_time/Estimate_MR_Coherence_periodicity_autocorrelation.pdf")
    plt.show()















