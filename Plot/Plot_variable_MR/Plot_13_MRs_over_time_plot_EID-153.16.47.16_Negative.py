__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.figure as fig

# Import the targeted raw CSV file
rawCSV_file1 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-149.20.48.61.log.csv"
rawCSV_file2 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-149.20.48.77.log.csv"
rawCSV_file3 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-173.36.254.164.log.csv"
rawCSV_file4 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-193.162.145.50.log.csv"
rawCSV_file5 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-195.50.116.18.log.csv"
rawCSV_file6 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-198.6.255.37.log.csv"
rawCSV_file7 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-198.6.255.40.log.csv"
rawCSV_file8 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-202.51.247.10.log.csv"
rawCSV_file9 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-202.214.86.252.log.csv"
rawCSV_file10 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-206.223.132.89.log.csv"
rawCSV_file11 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-217.8.97.6.log.csv"
rawCSV_file12 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-217.8.98.42.log.csv"
rawCSV_file13 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/EID-153.16.47.16/planetlab1-EID-153.16.47.16-MR-217.8.98.46.log.csv"



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
                    if lines[15] == "195.59.156.123":
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
                    if lines[15] == "195.59.156.124":
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
plt.gcf().set_size_inches(16,6)
plt.gcf().set_dpi(300)

# To Scatter all 13 Map Replies from 13 MRs
for responseList in responseLists1:
     plt.scatter(time, responseList, marker="*", color='orange')

for responseList in responseLists2:
     plt.scatter(time, responseList, marker="+", color='green')

response = np.linspace(1, 13, 13)
plt.xlabel("Experiment numbers", fontsize=16)
plt.ylabel("13 MRs", fontsize=16)
plt.title("Normal Reply from 13 different MRs for EID-153.16.17.16 over time", fontsize=16)
plt.xlim(0, 801)
# plt.xlim(0, 50)
plt.ylim(0.5, 13.5)
plt.yticks(response, ('MR1', 'MR2', 'MR3', 'MR4', 'MR5', 'MR6', 'MR7', 'MR8', 'MR9', 'MR10', 'MR11', 'MR12', 'MR13'))

plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_MR/Normal_from_13_different_MRs_for_EID-153_16_47_16_over_time_size_double.pdf")
plt.show()