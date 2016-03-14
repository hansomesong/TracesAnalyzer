# -*- coding: utf-8 -*-
__author__ = 'yueli'

import matplotlib.pyplot as plt
from config.config import *
import numpy as np
import math
from collections import Counter

import matplotlib as mpl

mpl.rcParams['text.usetex'] = True
mpl.rcParams.update({'figure.autolayout': True})

def change_num_counter(target_file):
    file_num_counter = 0
    change_num_list = []
    nb_observation = 0.0
    with open(target_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')
            if tmp_list[LOG_TIME_COLUMN['coherence']] != "True":
                file_num_counter += 1
                file_path = tmp_list[LOG_TIME_COLUMN['log_file_name']]

                with open(file_path) as tmp_handler:
                    nb_observation = sum(1 for line in tmp_handler)-1.0
                if tmp_list[15] != '0':
                    change_num_list.append(len(tmp_list[15].split(','))/nb_observation*100.0)
                else:
                    if tmp_list[18] != '0':
                        change_num_list.append(len(tmp_list[18].split(','))/nb_observation*100.0)

    return file_num_counter, change_num_list


def cdf(pdf_list):
    cdf_list = []
    for value in pdf_list:
        if not cdf_list:
            cdf_list.append(value)
        else:
            cdf_list.append(value + cdf_list[-1])

    return cdf_list


# 计算 <EID, MR, VP> csv file 中的 change number / experiment number
# input = <EID, MR, VP> csv file
# output = experiment number
def experiment_number_counter(target_file):
    with open(target_file) as f_handler:
         experiment_number = float(sum(1 for line in f_handler)-1.0)

    return experiment_number



# 此函数用来统计针对一个 comparison time VP CSV file 里 Coherence列为 False 的文件的变化百分比，
# 对应 <EID, MR, VP> csv file 中的 change number / experiment number
# input = comparison time VP CSV file
# output = percentage_list
def instability_occurence(taget_file):

    with open(target_file) as f_handler:
        unstable_file_num_counter = 0.0
        unstable_percentage_list = []
        next(f_handler)
        for line in f_handler:
            lines = line.split(";")
            if lines[LOG_TIME_COLUMN['coherence']] == 'False':
                unstable_file_num_counter = unstable_file_num_counter + 1.0
                change_number = float(len(lines[LOG_TIME_COLUMN['case1_change_time']].split(",")) + len(lines[LOG_TIME_COLUMN['case3_4_change_time']].split(",")))
                file_name = os.path.join(PLANET_CSV_DIR, lines[LOG_TIME_COLUMN['vantage']], "{0}.csv".format(lines[LOG_TIME_COLUMN['log_file_name']].split("/")[-1]))
                unstable_percentage_list.append(change_number / experiment_number_counter(file_name) * 100.0)

    return unstable_file_num_counter, unstable_percentage_list


if __name__ == '__main__':
    # 读取环境变量 ‘PROJECT_LOG_DIR’ (此变量定义在工作目录下.profile或者.bashprofile)
    try:
        PLANET_DIR = os.environ['PLANETLAB']
        CSV_FILE_DESTDIR = os.environ['PROJECT_LOG_DIR']
        PLANET_CSV_DIR = os.environ['PLANETLAB_CSV']
        PLOT_DIR = os.environ['PROJECT_PLOT_DIR']
    except KeyError:
        print "Environment variable PROJECT_LOG_DIR is not properly defined or " \
              "the definition about this variable is not taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"

    # # 创建一个list，用来存储每一个含有NormalReply返回的percentage
    # file_total_num = 0
    # change_num_total_list = []
    #
    # # 遍历VP_LIST里的5个vp
    # for vp in VP_LIST:
    # # for vp in ["wiilab"]:
    #     # Creat a CSV file 来存储 SRC_reply != Locator 的情况
    #     target_file = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))
    #     print target_file
    #     file_num_counter, change_num_list = change_num_counter(target_file)
    #     file_total_num = file_total_num + file_num_counter
    #     change_num_total_list.extend(change_num_list)
    #     print "Unstable number =", len(change_num_list)
    #
    # print "change_num_total_list =", change_num_total_list
    # # # 计算 stable file 的数量有多少
    # # print "file_total_num =", file_total_num
    # # stable_file_num = file_total_num - len(change_num_total_list)
    # # print "stable_file_num =", stable_file_num
    # # 此处默认每次实验次数都是 802
    # # change_num_total_counter = Counter((i/802.0*100.0) for i in change_num_total_list)
    # print "change_num_total_list =", len([math.ceil(i*100) for i in change_num_total_list])
    # change_num_total_counter = Counter(math.ceil(i*100) for i in change_num_total_list)
    # tmp =sorted(change_num_total_counter.items(), key=lambda x: x[0])
    #
    # pdf_x_axis = [list(i)[0] for i in tmp]
    # # pdf_x_axis.insert(0, 0.0)
    # pdf_y_axis = [list(i)[1]/(float(file_total_num))*100 for i in tmp]
    # # pdf_y_axis.insert(0, float(stable_file_num)/float(file_total_num)*100)
    # cdf_y_axis = cdf(pdf_y_axis)
    #
    #
    # print "change_num_total_counter =", change_num_total_counter
    # print "pdf_x_axis =", pdf_x_axis
    # print "pdf_y_axis =", pdf_y_axis
    # print "cdf_y_axis =", cdf_y_axis
    #
    #
    # # Plot part
    # # Modify the size and dpi of picture, default size is (8,6), default dpi is 80
    # plt.gcf().set_size_inches(10,9)
    # # Define font
    # font_label = {
    # 'fontname'   : 'Times New Roman',
    # 'color'      : 'black',
    # 'fontsize'   : 40
    #    }
    # plt.grid(True)

    # # Plot pdf
    # plt.plot(pdf_x_axis, pdf_y_axis, c='black', linewidth=3)
    # plt.scatter(pdf_x_axis, pdf_y_axis, c='black', s=80)
    # plt.xlabel("instability frequency (%)", fontsize=45, fontname='Times New Roman')
    # plt.ylabel("pdf (%)", fontsize=45, fontname='Times New Roman')
    # plt.xlim(0, 50)
    # plt.ylim(0, 8)
    # plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'pdf_instability_occur.eps'), dpi=300, transparent=True)
    # plt.show()

    # # Plot cdf
    # plt.plot(pdf_x_axis, cdf_y_axis, c='black', linewidth=5)
    # # plt.scatter(pdf_x_axis, cdf_y_axis, c='black', s=50)
    # plt.xlabel("instability frequency (%)", font_label)
    # plt.ylabel("cdf (%)", font_label)
    # plt.xticks(fontsize=16)
    # plt.yticks(fontsize=16)
    # #plt.xlim(1, 50)
    # # plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'cdf_instability_occur.eps'), dpi=300, transparent=True)
    # plt.show()

    unstable_total_num = 0.0
    unstable_total_per_list = []
    for vp in VP_LIST:
        target_file = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))
        print target_file
        unstable_file_num, unstable_percentage_list = instability_occurence(target_file)
        unstable_total_num = unstable_total_num + unstable_file_num
        unstable_total_per_list.extend(unstable_percentage_list)

    unstable_total_per_int_list = [math.ceil(i) for i in unstable_total_per_list]
    x_axis = Counter(unstable_total_per_int_list).keys()
    y_pdf_axis = [(float(i) / unstable_total_num * 100) for i in Counter(unstable_total_per_int_list).values()]
    y_cdf_axis = cdf(y_pdf_axis)

    print unstable_total_num
    print Counter(unstable_total_per_int_list)
    print x_axis
    print y_pdf_axis
    print y_cdf_axis

    plt.plot(x_axis, y_cdf_axis, c='black', linewidth=5)
    # plt.scatter(pdf_x_axis, cdf_y_axis, c='black', s=50)
    plt.xlabel(r"instability frequency (\%)", font)
    plt.ylabel(r"cdf (\%)", font)
    plt.xticks(fontsize=40, fontname="Times New Roman")
    plt.yticks(fontsize=40, fontname="Times New Roman")
    plt.xlim(1, len(x_axis))
    plt.grid(True)
    # plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'cdf_instability_occur.eps'), dpi=300, transparent=True)
    plt.show()