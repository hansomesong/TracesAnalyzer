__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file1 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-149.20.48.61.log.csv"
rawCSV_file2 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-149.20.48.77.log.csv"
rawCSV_file3 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-173.36.254.164.log.csv"
rawCSV_file4 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-193.162.145.50.log.csv"
rawCSV_file5 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-195.50.116.18.log.csv"
rawCSV_file6 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-198.6.255.37.log.csv"
rawCSV_file7 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-198.6.255.40.log.csv"
rawCSV_file8 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-202.51.247.10.log.csv"
rawCSV_file9 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-202.214.86.252.log.csv"
rawCSV_file10 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-206.223.132.89.log.csv"
rawCSV_file11 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-217.8.97.6.log.csv"
rawCSV_file12 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-217.8.98.42.log.csv"
rawCSV_file13 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.49.112/planetlab1-EID-153.16.49.112-MR-217.8.98.46.log.csv"

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
                if (lines[15] == "82.121.231.67"):
                    rlocSet1 = rlocSet1 + 1
                elif (lines[15] == "192.168.1.66"):
                    rlocSet2 = rlocSet2 + 1
                elif (lines[15] == "132.227.85.231"):
                    rlocSet3 = rlocSet3 + 1

            elif int(lines[9]) == 2:
                if (lines[15] == "82.121.231.67") or (lines[20] == "82.121.231.67"):
                    rlocSet1 = rlocSet1 + 1
                elif (lines[15] == "192.168.1.66") or (lines[20] == "192.168.1.66"):
                    rlocSet2 = rlocSet2 + 1
                elif (lines[15] == "132.227.85.231") or (lines[20] == "132.227.85.231"):
                    rlocSet3 = rlocSet3 + 1

            elif int(lines[9]) == 3:
                if (lines[15] == "82.121.231.67") or (lines[20] == "82.121.231.67") or (lines[25] == "82.121.231.67"):
                    rlocSet1 = rlocSet1 + 1
                elif (lines[15] == "192.168.1.66") or (lines[20] == "192.168.1.66") or (lines[25] == "192.168.1.66"):
                    rlocSet2 = rlocSet2 + 1
                elif (lines[15] == "132.227.85.231") or (lines[20] == "132.227.85.231") or (lines[25] == "132.227.85.231"):
                    rlocSet3 = rlocSet3 + 1

    # total = negativeReply + noMapReply + rlocSet1 + rlocSet2 + rlocSet3

    return negativeReply, negativeReply + noMapReply, \
           negativeReply + noMapReply + rlocSet1, \
           negativeReply + noMapReply + rlocSet1 + rlocSet2, \
           negativeReply + noMapReply + rlocSet1 + rlocSet2 + rlocSet3

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
# percentage = np.linspace(0, 801, 11)
# percentage90 = np.linspace(720.9, 801, 11)
percentage95 = np.linspace(760.95, 801, 6)
plt.bar(mr, listResult_trans[4], bar_width, color="green", label="Locator 3")
plt.bar(mr, listResult_trans[3], bar_width, color="red", label="Locator 2")
plt.bar(mr, listResult_trans[2], bar_width, color="purple", label="Locator 1")
plt.bar(mr, listResult_trans[1], bar_width, color="yellow", label="No Map Reply")
plt.bar(mr, listResult_trans[0], bar_width, color="blue", label="Negative Reply")
plt.xlabel('13 map resolvers')
plt.ylabel('percentage of every Map Reply (%)')
plt.title('Percentage of every Map Reply for 13 MRs')
# plt.yticks(percentage, ('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'))
# plt.yticks(percentage90, ('90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100'))
plt.yticks(percentage95, ('95', '96', '97', '98', '99', '100'))
plt.xticks(mr + bar_width*0.5, ('MR1', 'MR2', 'MR3', 'MR4', 'MR5', 'MR6', 'MR7', 'MR8', 'MR9', 'MR10', 'MR11', 'MR12', 'MR13'))
plt.xlim(0, 13)
# plt.ylim(0,801)
# plt.ylim(720.9,801)
plt.ylim(760.95, 801)
plt.legend(loc='lower right')
# plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_MR/Plot_variable_MR_percentage95.pdf")
plt.show()

