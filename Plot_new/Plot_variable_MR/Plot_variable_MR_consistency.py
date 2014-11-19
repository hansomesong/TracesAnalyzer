__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file1 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-149.20.48.61.log.csv"
rawCSV_file2 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-149.20.48.77.log.csv"
rawCSV_file3 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-173.36.254.164.log.csv"
rawCSV_file4 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-193.162.145.50.log.csv"
rawCSV_file5 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-195.50.116.18.log.csv"
rawCSV_file6 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-198.6.255.37.log.csv"
rawCSV_file7 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-198.6.255.40.log.csv"
rawCSV_file8 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-202.51.247.10.log.csv"
rawCSV_file9 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-202.214.86.252.log.csv"
rawCSV_file10 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-206.223.132.89.log.csv"
rawCSV_file11 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-217.8.97.6.log.csv"
rawCSV_file12 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-217.8.98.42.log.csv"
rawCSV_file13 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/For_MR/planetlab1-EID-153.16.49.112-MR-217.8.98.46.log.csv"



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

# Define a function to get the RLOC list from the CSV file
def getRlocSet(rawCSV_file):
    i = -1
    rlocSet = []
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            if lines[0] == "NegativeReply":
                rlocSet.append(-1)
            elif lines[0] == "RoundNoReply":
                rlocSet.append(0)
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    if lines[15] == "82.121.231.67":
                        rlocSet.append(1)
                    elif lines[15] == "192.168.1.66":
                        rlocSet.append(2)
                    elif lines[15] == "132.227.85.231":
                        rlocSet.append(3)
                elif int(lines[9]) == 2:
                    print "There are 2 RLOCs together"
                elif int(lines[9]) == 3:
                    print "There are 2 RLOCs together"
                else:
                    rlocSet.append(10)
            else:
                print "Unknown type exists"
    return rlocSet

time = []

time = getTime(rawCSV_file1)
rlocSet1 = getRlocSet(rawCSV_file1)
print rlocSet1.__len__()
rlocSet2 = getRlocSet(rawCSV_file2)
rlocSet3 = getRlocSet(rawCSV_file3)
rlocSet4 = getRlocSet(rawCSV_file4)
rlocSet5 = getRlocSet(rawCSV_file5)
rlocSet6 = getRlocSet(rawCSV_file6)
rlocSet7 = getRlocSet(rawCSV_file7)
rlocSet8 = getRlocSet(rawCSV_file8)
rlocSet9 = getRlocSet(rawCSV_file9)
rlocSet10 = getRlocSet(rawCSV_file10)
rlocSet11 = getRlocSet(rawCSV_file11)
rlocSet12 = getRlocSet(rawCSV_file12)
rlocSet13 = getRlocSet(rawCSV_file13)


consistency = []
inconsistency = []
for i in range(0, 801):
    if rlocSet1[i] == rlocSet2[i] == rlocSet3[i] == rlocSet4[i] == rlocSet5[i] == rlocSet6[i] == \
            rlocSet7[i] == rlocSet8[i] == rlocSet9[i] == rlocSet10[i] == rlocSet11[i] == rlocSet12[i] == rlocSet13[i]:
        consistency.append(1)
        inconsistency.append(-1)
    else:
        consistency.append(-1)
        inconsistency.append(2)

# Calculate the times of consistency
k = 0
for j in consistency:
    if j == 1:
        k = k + 1

print "There are", k, "times of consistency over", consistency.__len__(), "times of experiments"



# Plot part
plt.scatter(time, consistency, color='blue', s=20)
plt.scatter(time, inconsistency, color='red', s=1)

plt.xlabel("Experiment numbers")
plt.ylabel("Consistency / Inconsistency")
plt.title("Consistency of the responses from 13 MRs for EID-153.16.49.112 in liege")

plt.xlim(0, 801)
plt.ylim(0, 3)
plt.yticks((1, 2), ('Consistency', 'Inconsistency'))

#plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_MR/Plot_variable_MR_consistency.pdf")
plt.show()

