# -*- coding: utf-8 -*-
# __author__ = 'yueli'
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
    i = -1
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
responseLists1 = []
responseLists2 = []
mr1 = 1
mr2 = 1
for rawCSV_file in rawCSV_files:
    i = -1
    responseList1 = []
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            if lines[0] == "NegativeReply":
                responseList1.append(-1)
            elif lines[0] == "RoundNoReply":
                responseList1.append(-5)
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    if lines[14].split(",")[1] == "195.59.156.123":
                        responseList1.append(mr1)
                    else:
                        responseList1.append(-10)
            else:
                responseList1.append(-10)
    responseLists1.append(responseList1)
    mr1 = mr1 + 1

for rawCSV_file in rawCSV_files:
    i = -1
    responseList2 = []
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            if lines[0] == "NegativeReply":
                responseList2.append(-1)
            elif lines[0] == "RoundNoReply":
                responseList2.append(-5)
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    if lines[14].split(",")[1] == "195.59.156.124":
                        responseList2.append(mr2)
                    else:
                        responseList2.append(-10)
            else:
                responseList2.append(-10)
    print "responseList2:", responseList2
    print "responseList2.len:", len(responseList2)
    responseLists2.append(responseList2)
    mr2 = mr2 + 1



time = []
time = getTime(rawCSV_file1)
print "time.len", len(time)

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(8,6)
plt.gcf().set_dpi(300)

# To Scatter all 13 Map Replies from 13 MRs, for循环里的才是正经要画的
# 最开始这两条命令只是为了画图出现图例，如果在for循环里加label会导致出现13个重复的RLOC1图例和RLOC2图例
plt.scatter(time, responseLists1[0], marker="*", color='orange', label = "RLOC1")
plt.scatter(time, responseLists2[0], marker="+", color='green', label = "RLOC2")

for responseList in responseLists1:
     plt.scatter(time, responseList, marker="*", color='orange')

for responseList in responseLists2:
     plt.scatter(time, responseList, marker="+", color='green')

response = np.linspace(1, 13, 13)
plt.xlabel("Experiment numbers", fontsize=16)
plt.ylabel("MRs", fontsize=16)
# plt.title("Normal Reply from 13 different MRs for EID-153.16.47.16 over time", fontsize=16)
# plt.xlim(0, 801)
plt.xlim(0, 50)
plt.ylim(0.5, 13.5)
plt.yticks(response, ('MR1', 'MR2', 'MR3', 'MR4', 'MR5', 'MR6', 'MR7', 'MR8', 'MR9', 'MR10', 'MR11', 'MR12', 'MR13'))
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, borderaxespad=0.)

# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_MR', 'Normal_from_13_different_MRs_for_EID-153_16_47_16_over_time.eps'),
#             dpi=300)
# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_MR', 'Normal_from_13_different_MRs_for_EID-153_16_47_16_over_time_label_zoom.eps'),
#             dpi=300)
plt.show()