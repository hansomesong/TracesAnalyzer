# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 本脚本用来衡量 13个Map resolver在发生new depolyment事件情况下的一致性情况
# 所谓一致性，是指在任一时刻，当
from config.config import *
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
    # 现在需要统计每一个MR，在5个vantage下，613个EID中所有的new deployment的时刻
    # 最理想的情况就是，在任一时刻，13个MR观察到的new deployment数目是一致的
    for vantage_name, log_file in input_logs.iteritems():
        # print vantage_name, log_file
        with open(log_file) as f_handler:
            f_handler.next()
            for line in f_handler:
                tmp = line.split(";")
                # 不考虑时间的秒位
                mp_resolver = tmp[LOG_TIME_COLUMN['resolver']]
                change_time = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                               # 如果只计算 New Deployment 则用第76行而注释掉第78行
                               for x in tmp[LOG_TIME_COLUMN['case1_change_time']].split(",") if x != '0']
                               # 如果要计算所有的变化个数，则用第78行而注释掉第76行
                               # for x in ",".join([tmp[LOG_TIME_COLUMN['case1_change_time']], tmp[LOG_TIME_COLUMN['case3_4_change_time']]]).split(",") if x != '0']
                               # strptime把字符串格式改写成datatime格式；strftime把datatime格式改写成字符串格式
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


    print "############### means ##############", means
    # 快速傅立叶变换，要变换的原始信号为means series
    sig = means
    #最先确定的是采样率，采样率确定意味着两方面的事情。
    #1.时间轴：确定每隔多久对信号采样一次，即离散化的时域轴的间隔确定，但是总长没定。
    #2.频率轴：的总长确定了，为采样率的一半，但是间隔没定。
    Fs = 1.0/1800
    T_interval = 1/Fs
    Freq_max = Fs/2

    #之后要确定的是采样的个数，采样的个数的确定也意味着两件事情。
    #1.时间轴：采样的总时间确定了,配合上面的间隔，也就全定了。
    #2.频率轴：频率轴的间隔定了，配合上面的总长，也就全定了。
    N = fft_size = len(sig)        # 即：FFT_SIZE
    t = np.arange(0,N)*T_interval
    freq = np.linspace(0,Freq_max,N/2+1)

    # 做FFT之后的信号
    fft_sig = np.fft.rfft(sig,N)/N

    # 为了把频谱的X轴由Frequence (Hz)更换为Time (Hour)，生成最终想显示的几个X轴上的数值然后求倒数，
    # 但目前还未用到频谱图上
    freqs_xticks_inverse = []
    for f in freq:
        if f == 0:
            freqs_xticks_inverse.append("endless")
        else:
            freqs_xticks_inverse.append(round(1/f,2))
    print "freqs_xticks_inverse:", len(freqs_xticks_inverse)


    # print len(t), "t:", t
    print len(sig), "sig:", sig
    # print len(freq), "freq:", freq
    # print len(fft_sig), "fft_sig:", fft_sig

    # Modify the size and dpi of picture, default size is (8,6), default dpi is 80
    plt.gcf().set_size_inches(14, 12)
    plt.gcf().set_dpi(300)

    #画出时间域的幅度图
    # pl.subplot(211)
    pl.plot(np.arange(1,N+1),sig,'black')
    pl.xlabel("experiment number", fontsize=50)
    pl.ylabel("change number", fontsize=50)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    pl.xlim(0,len(sig))
    pl.legend()
    # pl.title("Time waveform for mean of overall change number")


    # #画出频域图,你会发现你的横坐标无从下手？虽然你懂了后面的东西后可以返回来解决，但是现在就非常迷惑。现在只能原封不懂的画出频率图
    # # pl.subplot(212)
    # #
    # pl.plot(freq,2*np.abs(fft_sig),'black')#如果用db作单位则20*np.log10(2*np.abs(fft_sig))
    # pl.xlabel('frequency(Hz)', fontsize=50)
    # pl.ylabel('proportion', fontsize=50)
    # pl.xlim(0,Freq_max)
    # # 用于 New Deployment
    # # pl.ylim(0, 0.3)
    # # 用于所有 change number
    # pl.ylim(0, 0.5)
    # plt.xticks(fontsize=25)
    # plt.yticks(fontsize=25)
    # # pl.title('Frenquency spectrum for mean of overall change number')



    # # Autocorrelation
    # def autocorrelation(x,lags): #计算lags阶以内的自相关系数，返回lags个值，分别计算序列均值，标准差
    #     n = len(x)
    #     x = np.array(x)
    #     result = [np.correlate(x[i:]-x[i:].mean(),x[:n-i]-x[:n-i].mean())[0]\
    #         /(x[i:].std()*x[:n-i].std()*(n-i)) \
    #         for i in range(1,lags+1)]
    #     return result
    #
    # # 计算从k＝1 到 k＝experiment number-1 阶的auto-correlation，
    # # 因为 k＝experiment number-1 时计算的已是X(1)和X(n)间的相关性了，
    # # k ＝ experiment number的相关性不存在或无法计算，
    # # 但实际看几阶相关，周期为几时只看 experiment number/2 即可，后半程无意义，因为2个X序列已无交集
    # correlation_result = autocorrelation(means, fft_size-1)
    # print "correlation_result:", correlation_result
    # print "np.arange(1,N) length:", len(np.arange(1,N))
    # print "correlation_result length:", len(correlation_result)
    # plt.plot(np.arange(1,N), correlation_result, 'black')
    # plt.xlim(1, len(np.arange(1,N))/2)
    # plt.ylim(-0.4, 0.61)
    # plt.xlabel("order from 1 to n/2-1", fontsize=50)
    # plt.ylabel("coefficient of Auto-correlation", fontsize=50)
    # plt.xticks(fontsize=25)
    # plt.yticks(fontsize=25)
    # # pl.title('Auto-correlation for mean of overall change number')



    # # 将802个实验时刻对应的 随机变量均值、方差画图
    # plt.figure(1)
    # x_axis = np.arange(1,N+1)
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
    # figure_name_Autocorrelation = pl.figure('Period_verified_by_Autocorrelation.eps')

    # os.path.dirname(__file__) # 用来求得 当前文件所在的路径
    # os.path.join() # 用以生成存储所得图像路径
    plt.savefig(os.path.join(PLOT_DIR, 'Plot_periodicity', 'Change_number_by_exp_num.eps'), dpi = 300)
    # plt.savefig(os.path.join(PLOT_DIR, 'Plot_periodicity', 'Period_verified_by_FFT.eps'), dpi = 300)
    # plt.savefig(os.path.join(PLOT_DIR, 'Plot_periodicity', 'Period_verified_by_Autocorrelation.eps'), dpi = 300)
    # plt.show()















