# -*- coding: utf-8 -*-
__author__ = 'yueli'

import matplotlib.pyplot as plt
from config.config import *
import numpy as np
import math
from collections import Counter

def change_num_counter(target_file):
    file_num_counter = 0
    change_num_list = []

    with open(target_file) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')
            file_num_counter = file_num_counter + 1
            if tmp_list[15] != '0':
                change_num_list.append(len(tmp_list[15].split(',')))
            else:
                if tmp_list[18] != '0':
                    change_num_list.append(len(tmp_list[18].split(',')))

    return file_num_counter, change_num_list


def cdf(pdf_list):
    cdf_list = []
    for value in pdf_list:
        if not cdf_list:
            cdf_list.append(value)
        else:
            cdf_list.append(value + cdf_list[-1])

    return cdf_list


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

    # 创建一个list，用来存储每一个含有NormalReply返回的percentage
    file_total_num = 0
    change_num_total_list = []

    # 遍历VP_LIST里的5个vp
    for vp in VP_LIST:
        # Creat a CSV file 来存储 SRC_reply != Locator 的情况
        target_file = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))
        print target_file
        file_num_counter, change_num_list = change_num_counter(target_file)
        file_total_num = file_total_num + file_num_counter
        change_num_total_list.extend(change_num_list)
        print "Unstable number =", len(change_num_list)

    print "change_num_total_list =", change_num_total_list
    # 计算 stable file 的数量有多少
    print "file_total_num =", file_total_num
    stable_file_num = file_total_num - len(change_num_total_list)
    print "stable_file_num =", stable_file_num
    # 此处默认每次实验次数都是 802
    # change_num_total_counter = Counter((i/802.0*100.0) for i in change_num_total_list)
    print "change_num_total_list =", [math.ceil((i/802.0*100.0)) for i in change_num_total_list]
    change_num_total_counter = Counter(math.ceil((i/802.0*100.0)) for i in change_num_total_list)
    tmp =sorted(change_num_total_counter.items(), key=lambda x:x[0])

    pdf_x_axis = [list(i)[0] for i in tmp]
    pdf_x_axis.insert(0, 0.0)
    pdf_y_axis = [list(i)[1]/float(file_total_num)*100 for i in tmp]
    pdf_y_axis.insert(0, float(stable_file_num)/float(file_total_num)*100)
    cdf_y_axis = cdf(pdf_y_axis)


    print "change_num_total_counter =", change_num_total_counter
    print "pdf_x_axis =", pdf_x_axis
    print "pdf_y_axis =", pdf_y_axis
    print "cdf_y_axis =", cdf_y_axis


    # Plot part
    # Modify the size and dpi of picture, default size is (8,6), default dpi is 80
    plt.gcf().set_size_inches(10,9)
    # Define font
    font_label = {
    'fontname'   : 'Times New Roman',
    'color'      : 'black',
    'fontsize'   : 70
       }
    plt.grid(True)

    # Plot pdf
    plt.plot(pdf_x_axis, pdf_y_axis, c='black', linewidth=3)
    plt.scatter(pdf_x_axis, pdf_y_axis, c='black', s=80)
    plt.xlabel("Instability occurrence (%)", fontsize=45, fontname='Times New Roman')
    plt.ylabel("pdf (%)", fontsize=45, fontname='Times New Roman')
    plt.xlim(0, 50)
    plt.ylim(0, 8)
    plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'pdf_instability_occur.eps'), dpi=300, transparent=True)
    plt.show()

    # # Plot cdf
    # plt.plot(pdf_x_axis, cdf_y_axis, c='black', linewidth=3)
    # plt.scatter(pdf_x_axis, cdf_y_axis, c='black', s=80)
    # plt.xlabel("Instability occurrence (%)", fontsize=45, fontname='Times New Roman')
    # plt.ylabel("cdf (%)", fontsize=45, fontname='Times New Roman')
    # plt.xlim(0, 50)
    # plt.ylim(90, 100)
    # plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'cdf_instability_occur.eps'), dpi=300, transparent=True)
    # plt.show()