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


# Plot begins here, "-1" means the response is "Negative Reply", "0" means the response is "No Map Reply"
# "1" means the RLOC set is "82.121.231.67", "2" means the RLOC set is "192.168.1.66",
# "3" means the RLOC set is "132.227.85.231", "10" means the RLOC set is others

# plt.plot(time, rlocSet1)
# plt.plot(time, rlocSet2)
# plt.plot(time, rlocSet3)
# plt.plot(time, rlocSet4)
# plt.plot(time, rlocSet5)
# plt.plot(time, rlocSet6)
# plt.plot(time, rlocSet7)
# plt.plot(time, rlocSet8)
# plt.plot(time, rlocSet9)
# plt.plot(time, rlocSet10)
# plt.plot(time, rlocSet11)
# plt.plot(time, rlocSet12)
# plt.plot(time, rlocSet13)

#
plt.scatter(time, rlocSet1, s=1, c=(0.8, 0.8, 0.8))
plt.scatter(time, rlocSet2, s=1, c=(0.0, 0.5019607843137255, 0.0))
plt.scatter(time, rlocSet3, s=1, c=(0.0, 1.0, 1.0))
plt.scatter(time, rlocSet4, s=1, c=(0.75, 0.75, 0.75))
plt.scatter(time, rlocSet5, s=1, c=(0.7372549019607844, 0.7372549019607844, 0.7372549019607844))
plt.scatter(time, rlocSet6, s=1, c=(0.6980392156862745, 0.13333333333333333, 0.13333333333333333))
plt.scatter(time, rlocSet7, s=1, c=(1.0, 0.9294117647058824, 0.43529411764705883))
plt.scatter(time, rlocSet8, s=1, c=(0.27450980392156865, 0.47058823529411764, 0.12941176470588237))
plt.scatter(time, rlocSet9, s=1, c=(0.9333333333333333, 0.9333333333333333, 0.9333333333333333))
plt.scatter(time, rlocSet10, s=1, c=(1.0, 1.0, 0.0))
plt.scatter(time, rlocSet11, s=1, c=(0.6, 0.6, 0.6))
plt.scatter(time, rlocSet12, s=1, c=(0.9411764705882353, 0.8941176470588236, 0.25882352941176473))
plt.scatter(time, rlocSet13, s=1, c=(0.5, 0.5, 0.5))


plt.xlabel("Time (2013/07/02 07:30 - 2013/07/18 23:30)")
plt.ylabel("Responses from MRs")
plt.title("Responses from 13 MRs for EID-153.16.49.112 in liege(by Time)")

plt.xlim(0, 820)
plt.ylim(-1.5, 3.5)
#plt.legend(loc='upper right')

plt.annotate('Negative Reply',xy=(0,-1),xytext=(0,-1.3),arrowprops=dict(arrowstyle="->"))
plt.annotate('No Map Reply',xy=(0,0),xytext=(0,0.1),arrowprops=dict(arrowstyle="->"))
plt.annotate('RLOC-82.121.231.67',xy=(0,1),xytext=(0,1.1),arrowprops=dict(arrowstyle="->"))
plt.annotate('RLOC-192.168.1.66',xy=(0,2),xytext=(0,2.1),arrowprops=dict(arrowstyle="->"))
plt.annotate('RLOC-132.227.85.231',xy=(0,3),xytext=(0,3.1),arrowprops=dict(arrowstyle="->"))

plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_MR/Plot_variable_MR_copy.png")
plt.show()

