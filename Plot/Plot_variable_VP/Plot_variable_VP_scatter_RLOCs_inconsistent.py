# -*- coding: utf-8 -*-
__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file1 = os.path.join(
    CSV_FILE_DESTDIR,
    'For_different_5_VP',
    'Deleted_database',
    'EID-153.16.47.16-MR-198.6.255.37',
    "liege-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file2 = os.path.join(
    CSV_FILE_DESTDIR,
    'For_different_5_VP',
    'Deleted_database',
    'EID-153.16.47.16-MR-198.6.255.37',
    "temple-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file3 = os.path.join(
    CSV_FILE_DESTDIR,
    'For_different_5_VP',
    'Deleted_database',
    'EID-153.16.47.16-MR-198.6.255.37',
    "ucl-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file4 = os.path.join(
    CSV_FILE_DESTDIR,
    'For_different_5_VP',
    'Deleted_database',
    'EID-153.16.47.16-MR-198.6.255.37',
    "umass-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file5 = os.path.join(
    CSV_FILE_DESTDIR,
    'For_different_5_VP',
    'Deleted_database',
    'EID-153.16.47.16-MR-198.6.255.37',
    "wiilab-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

# Define a function to get the experiment number list from the CSV file
def getTime(rawCSV_file):
    i = -2 # 以保证time这个list从0开始，长度为798
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            time.append(i)
    return time


def getRlocSet(rawCSV_file):
    i = -1
    responseList = []
    for line in open(rawCSV_file):
        print line
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            print "Round Type"
            continue
        else:
            if lines[0] == "NegativeReply":
                print "Done"
                responseList.append(-1)
            elif lines[0] == "RoundNoReply":
                responseList.append(0)
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    if lines[14].split(",")[1] == "195.59.156.123":
                        responseList.append(1)
                    elif lines[14].split(",")[1] == "195.59.156.124":
                        responseList.append(2)
                    else:
                        responseList.append(3)
                else:
                    print "There are more than 2 RLOCs together"
            else:
                print "Unknown type exists"
    return responseList



time = []
time = getTime(rawCSV_file1)
print "time", time


rlocSet1 = getRlocSet(rawCSV_file1)
print "rlocSet1:", rlocSet1.__len__()
rlocSet2= getRlocSet(rawCSV_file2)
print "rlocSet2:", rlocSet2.__len__()
rlocSet3 = getRlocSet(rawCSV_file3)
print "rlocSet3:", rlocSet3.__len__()
rlocSet4 = getRlocSet(rawCSV_file4)
print "rlocSet4:", rlocSet4.__len__()
rlocSet5 = getRlocSet(rawCSV_file5)
print "rlocSet5:", rlocSet5.__len__()

inconsistent_list = []
for t in time:
    response_compare = []
    response_compare.append(rlocSet1[t])
    response_compare.append(rlocSet2[t])
    response_compare.append(rlocSet3[t])
    response_compare.append(rlocSet4[t])
    response_compare.append(rlocSet5[t])
    if set(response_compare) == 1:
        inconsistent_list.append(0) #用于plot
        inconsistent_list.append(-99) #用于scatter
    else:
        inconsistent_list.append(1) # 若set(response_compare)不为1，则说明有多个RLOCs


# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
# plt.gcf().set_size_inches(8,6)
plt.gcf().set_dpi(300)

# plt.plot(time, inconsistent_list)
plt.scatter(time, inconsistent_list, s=10, c='blue')
plt.xlabel("experiment numbers", fontsize=16)
# plt.title("Map Replies over time for EID-153.16.47.16 from MR-198.6.255.37 in 5 VPs", fontsize=20)
plt.xlim(0,798)
# plt.ylim(-0.2, 1.2)
# plt.yticks([0,1], ('consistent', 'incon-\nsistent'))
plt.ylim(0, 2)
plt.yticks([0,1,2], ('','incon-\nsistent',''))

# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_VP', 'Plot_variable_VP_different_RLOCs_inconsistent_plot.eps'))
plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_VP', 'Plot_variable_VP_different_RLOCs_inconsistent_scatter.eps'))

plt.show()