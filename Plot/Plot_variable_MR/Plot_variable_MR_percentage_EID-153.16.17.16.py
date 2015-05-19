# -* coding:UTF-8 -*
__author__ = 'yueli'

import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file1 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-149.20.48.61.log.csv')
rawCSV_file2 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-149.20.48.77.log.csv')
rawCSV_file3 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-173.36.254.164.log.csv')
rawCSV_file4 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-193.162.145.50.log.csv')
rawCSV_file5 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-195.50.116.18.log.csv')
rawCSV_file6 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-198.6.255.37.log.csv')
rawCSV_file7 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-198.6.255.40.log.csv')
rawCSV_file8 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-202.51.247.10.log.csv')
rawCSV_file9 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-202.214.86.252.log.csv')
rawCSV_file10 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-206.223.132.89.log.csv')
rawCSV_file11 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-217.8.97.6.log.csv')
rawCSV_file12 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-217.8.98.42.log.csv')
rawCSV_file13 = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.17.16-MR-217.8.98.46.log.csv')

def getResult(rawCSV):

    rawCSV_file = rawCSV
    negativeReply = 0
    noMapReply = 0
    rlocSet1 = 0 # rlocSet1 means that the RLOC is "82.121.231.67"
    rlocSet2 = 0 # rlocSet2 means that the RLOC is "192.168.1.66"
    rlocSet3 = 0 # rlocSet3 means that the RLOC is "132.227.85.231"
    negativeReplyList = []
    noMapReplyList = []
    rlocSet1List = [] # rlocSet1 means that the RLOC is "82.121.231.67"
    rlocSet2List = [] # rlocSet2 means that the RLOC is "192.168.1.66"
    rlocSet3List = []
    total = 0
    i = -1
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            if lines[0] == "RoundNoReply":
                noMapReply = noMapReply + 1

            elif lines[0] == "NegativeReply":
                negativeReply = negativeReply + 1

            elif int(lines[9]) == 1:
                # 因为CSV文件发生变化，所以用下面一条语句从“0,24.94.15.214,up,1,1”中只提取出Locator
                if (lines[14].split(",")[1] == "24.94.15.214"):
                    rlocSet1 = rlocSet1 + 1
                else:
                    rlocSet2 = rlocSet2 + 1

    # total = negativeReply + noMapReply + rlocSet1 + rlocSet2 + rlocSet3

    return rlocSet1, rlocSet1 + rlocSet2,\
           rlocSet1 + rlocSet2 +negativeReply,\
           rlocSet1 + rlocSet2 +negativeReply + noMapReply

# listResult[0] contains all the responses by the order of negativeReply, noMapReply, rlocSet1, rlocSet2 and rlocSet3 from MR1
listResult = []
listResult.append(getResult(rawCSV_file1))
listResult.append(getResult(rawCSV_file2))
listResult.append(getResult(rawCSV_file3))
listResult.append(getResult(rawCSV_file4))
listResult.append(getResult(rawCSV_file5))
listResult.append(getResult(rawCSV_file6))
listResult.append(getResult(rawCSV_file7))
listResult.append(getResult(rawCSV_file8))
listResult.append(getResult(rawCSV_file9))
listResult.append(getResult(rawCSV_file10))
listResult.append(getResult(rawCSV_file11))
listResult.append(getResult(rawCSV_file12))
listResult.append(getResult(rawCSV_file13))

print "listResult", listResult

# listResult_trans[0] contains the value of negativeReply from 13 MRs,
# listResult_trans[1] contains the value of noMapReply from 13 MRs,
# listResult_trans[2] contains the value of rlocSet1 from 13 MRs,
# listResult_trans[3] contains the value of rlocSet2 from 13 MRs,
# listResult_trans[4] contains the value of rlocSet3 from 13 MRs,
listResult_trans = np.transpose(listResult)
print "listResult_trans", listResult_trans

n_groups = 13
mr = np.arange(n_groups)
bar_width = 1
# percentage = np.linspace(0, 753, 11)
# percentage90 = np.linspace(677.7, 753, 11)
# percentage95 = np.linspace(715.35, 753, 6)
percentage98 = np.linspace(737.94, 753, 3)


plt.bar(mr, listResult_trans[3], bar_width, color="lightskyblue", label="No Map Reply")
plt.bar(mr, listResult_trans[2], bar_width, color="green", label="Negative Reply")
plt.bar(mr, listResult_trans[0], bar_width, color="yellow", label="RLOC-24.94.15.214")
plt.xlabel('13 map resolvers')
plt.ylabel('percentage of every Map Reply (%)')
plt.title('Percentage of different Map Replies for EID-153.16.17.16 from 13 MRs')
# plt.yticks(percentage, ('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'))
# plt.yticks(percentage90, ('90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100'))
# plt.yticks(percentage95, ('95', '96', '97', '98', '99', '100'))
plt.yticks(percentage98, ('98', '99', '100'))
plt.xticks(mr + bar_width*0.5, ('MR1', 'MR2', 'MR3', 'MR4', 'MR5', 'MR6', 'MR7', 'MR8', 'MR9', 'MR10', 'MR11', 'MR12', 'MR13'))
plt.xlim(0, 13)
# plt.ylim(0, 753)
# plt.ylim(677.7,753)
# plt.ylim(715.35, 753)
plt.ylim(737.94, 753)
plt.legend(loc='lower right')
# plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_MR/Plot_variable_MR_percentage98_EID-153_16_17_16.pdf")
plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_MR', 'Plot_variable_MR_percentage98_EID-153_16_17_16.eps'),
            dpi=300, transparent=True)
plt.show()

