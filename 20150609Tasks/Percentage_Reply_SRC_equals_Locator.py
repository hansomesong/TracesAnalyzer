# -*- coding: utf-8 -*-
__author__ = 'yueli'
# 此脚本用于计算所有PlanetLab CSV文件中的Reply_SRC是否是Map Reply中的one of RLOC
# 因此，只有Normal Map Reply的情况予以考虑
# 因为1.No Map Reply不含有任何mapping回复信息； 2. Negative Reply中不会含有Locator set的任何信息

from config.config import *
import os
import timeit
import re
import numpy as np
import matplotlib.pyplot as plt
import csv


# 首先定义一个method，它针对一个csv文件进行处理，返回值为Reply_SRC是Map Reply中的one of RLOC的percentage
def percentage_yes_in_one_csv(csv_file, per_0_output):
    # 定义2个变量，count_yes用来记录在此csv file中Reply_SRC是Map Reply中的one of RLOC的个数，
    # count_no用来记录不是的个数，最后count_yes/(count_yes+count_no)即可算出概率
    count_yes = 0
    count_no =0

    with open(csv_file) as f_handler:

        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(';')

            # 先对Round type进行判断，只有RoundNormal才有考虑的必要
            if tmp_list[LOG_COLUMN['round_type']] == 'RoundNormal':
                # 得到此Map Reply中共有几个RLOC，即LOCATOR_Count的值
                locator_count = int(tmp_list[LOG_COLUMN['locator_count']])
                # 当locator_count>1时，tmp_list[LOG_COLUMN['locator_count']＋1]直到
                # tmp_list[LOG_COLUMN['locator_count']＋locator_count - 1]列都会有Locator的存在
                # 因而需要遍历所有的Locator，因为REPLY_Src不一定刚好等于第一个Locator
                j = 0
                for i in range(0,locator_count):
                    # 再进行验证，如果Reply_SRC是Map Reply中的one of RLOC，count_yes＋1，否则count_no+1
                    if re.findall(tmp_list[LOG_COLUMN['reply_src']], tmp_list[LOG_COLUMN['locator_id']+i]):
                        count_yes = float(count_yes + 1)
                        j = j + 1

                if j == 0:
                    count_no = float(count_no + 1)


    # 针对此csv file没有一行是RoundNormal的情况，那么此值将不影响main里最后计算平均概率
    if count_yes+count_no == 0:
        return None
    else:
        if count_yes/(count_yes+count_no)*100 != 100:
            print csv_file
            print count_yes/(count_yes+count_no)*100
            # 写入文件
            with open(per_0_output, 'wb') as f_output:
                writer = csv.writer(f_output, dialect='excel', delimiter=';')
                writer.writerow(['percentage', 'file_path'])
                writer.writerow([count_yes/(count_yes+count_no)*100, csv_file])

        return count_yes/(count_yes+count_no)*100




# Main
if __name__ == '__main__':
    start_time = timeit.default_timer()
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
    percentage_yes_list = []

    # 遍历VP_LIST里的5个vp
    for vp in VP_LIST:
        # Creat a CSV file 来存储 SRC_reply != Locator 的情况
        per_0_output = os.path.join(CSV_FILE_DESTDIR, 'src_reply_not_is_locator_{0}.csv'.format(vp))
        percentage_yes_list_vp = []
        # 遍历此vp下的所有csv file
        for lists in os.listdir(os.path.join(PLANET_CSV_DIR, vp)):
            csv_file = os.path.join(PLANET_CSV_DIR, vp, lists)

            if percentage_yes_in_one_csv(csv_file, per_0_output) != None:
                percentage_yes_list_vp.append(percentage_yes_in_one_csv(csv_file, per_0_output))

        percentage_yes_list.extend(percentage_yes_list_vp)
        print "percentage_yes_list in {0}:".format(vp), percentage_yes_list_vp
        print "overall percentage_yes_list in {0}:".format(vp), np.average(percentage_yes_list_vp)



    overall_percentage_yes = np.average(percentage_yes_list)
    print "overall_percentage_yes", overall_percentage_yes


    # # 此处画个图，把5个vp得到的percentage画成柱状图，overall percentage画成一条横虚线
    # # 画图所需数据为此script算得的数据，直接给出用以画图，否则太慢了
    # y_list = [89.23, 88.10, 89.45, 88.54, 88.70]
    # x_overall_list = [-0.3, 4.7]
    # y_overall_list = [88.8, 88.8]
    #
    # n_groups = 5
    # indexs = np.arange(n_groups)
    # bar_width = 0.35
    #
    # plt.grid(True)
    #
    # def autolabel(rects):
    #     for rect in rects:
    #         height = rect.get_height()
    #         print "height:", height
    #         plt.text(rect.get_x()+rect.get_width()/2-0.15, 1.0003*height, '%s' % round(height,2))
    #
    # # Control the opacity of the bar color
    # # opacity = 0.4
    # # rects1 = plt.bar(index, percentageFalseList, bar_width, alpha=opacity, color='b',label='Men')
    #
    #
    # plt.xlabel('vantage point',fontsize=20)
    # plt.ylabel('percentage(%)', fontsize=20)
    # # plt.title('Percentage of Reply_SRC equals one of RLOC set', fontsize=18)
    # plt.xticks(indexs + bar_width/2, ('1', '2', '3', '4', '5'), fontsize=16)
    # plt.plot(x_overall_list, y_overall_list, '--', color='r', label='overall')
    # plt.xlim(-0.3, 4.7)
    # plt.ylim(85,90)
    # rect = plt.bar(indexs, y_list, bar_width, color='b')
    # autolabel(rect)
    # plt.legend(loc='upper right')
    #
    # plt.savefig(
    #     os.path.join(PLOT_DIR, 'Percentage_Reply_SRC_equals_Locator.eps'),
    #     dpi=300,
    #     transparent=True
    # )
    #
    # plt.show()



    stop_time = timeit.default_timer()
    print "Execution time (in unit of second) of this script: ", stop_time - start_time
