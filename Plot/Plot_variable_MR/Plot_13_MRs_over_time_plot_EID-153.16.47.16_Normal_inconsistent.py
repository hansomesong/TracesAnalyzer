# -*- coding: utf-8 -*-
__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.figure as fig
from config.config import *

# Import the targeted raw CSV file
rawCSV_file1 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-149.20.48.61.log.csv')
rawCSV_file2 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-149.20.48.77.log.csv')
rawCSV_file3 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-173.36.254.164.log.csv')
rawCSV_file4 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-193.162.145.50.log.csv')
rawCSV_file5 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-195.50.116.18.log.csv')
rawCSV_file6 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-198.6.255.37.log.csv')
rawCSV_file7 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-198.6.255.40.log.csv')
rawCSV_file8 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-202.51.247.10.log.csv')
rawCSV_file9 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-202.214.86.252.log.csv')
rawCSV_file10 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-206.223.132.89.log.csv')
rawCSV_file11 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-217.8.97.6.log.csv')
rawCSV_file12 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-217.8.98.42.log.csv')
rawCSV_file13 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-217.8.98.46.log.csv')


# Define a function to get the Time list from the CSV file
def getTime(rawCSV_file):
    i = -2 # 以保证time这个list从0开始，长度为801
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            time.append(i)
    return time

rawCSV_files = []
rawCSV_files.append(rawCSV_file1)
rawCSV_files.append(rawCSV_file2)
rawCSV_files.append(rawCSV_file3)
rawCSV_files.append(rawCSV_file4)
rawCSV_files.append(rawCSV_file5)
rawCSV_files.append(rawCSV_file6)
rawCSV_files.append(rawCSV_file7)
rawCSV_files.append(rawCSV_file8)
rawCSV_files.append(rawCSV_file9)
rawCSV_files.append(rawCSV_file10)
rawCSV_files.append(rawCSV_file11)
rawCSV_files.append(rawCSV_file12)
rawCSV_files.append(rawCSV_file13)
response_list = []
inconsistent_list = []
for rawCSV_file in rawCSV_files:
    i = -1
    response_mr_list = []
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            if lines[0] == ("NegativeReply" or "RoundNoReply"):
                response_mr_list.append(lines[0])
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    response_mr_list.append(lines[14].split(",")[1])
            else:
                response_mr_list.append("MultiRLOCs")
    response_list.append(response_mr_list)


time = []
time = getTime(rawCSV_file1)

for t in time:
    response_compare = []
    for i in range(0,13):
        response_compare.append(response_list[i][t])
    if len(set(response_compare)) == 1:
        inconsistent_list.append(0) #用于plot
        # inconsistent_list.append(-99) #用于scatter
    else:
        inconsistent_list.append(1) #如果set的长度大于1，说明13个MRs的结果不一致

print "length of inconsistent_list:", len(inconsistent_list)
print inconsistent_list

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
# plt.gcf().set_size_inches(8,6)
plt.gcf().set_dpi(300)

# plt.plot(time, inconsistent_list)
plt.scatter(time, inconsistent_list, s=1, c='blue')

plt.xlabel("experiment numbers", fontsize=16)
# plt.ylabel("consistency", fontsize=16)
plt.xlim(0, 801)
# plt.ylim(-0.2, 1.2)
# plt.yticks([0,1], ('consistent','incon-\nsistent',''))
plt.ylim(0.5, 1.5)
plt.yticks([0.5,1,1.5], ('','incon-\nsistent',''))

# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_MR', 'Normal_from_13_different_MRs_for_EID-153_16_47_16_over_time_inconsistency_plot.eps'))
plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_MR', 'Normal_from_13_different_MRs_for_EID-153_16_47_16_over_time_inconsistency_scatter.eps'))
plt.show()