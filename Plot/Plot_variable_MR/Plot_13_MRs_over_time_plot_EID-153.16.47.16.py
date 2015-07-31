__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
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




# Define a function to get the response list from the CSV file and write them in "an index way",
# besides that the "-1" in the list means "Negative Reply", "0" in the list means "No Map Reply", and the other indexs
# indicate the different @IP, in the following way:
#['-1.-1.-1.-1', '0.0.0.0', '192.168.1.66', '132.227.85.238', '2001:660:3302:2826:6cac:405f:8937:719c', '217.8.97.6',
# '2001:660:3302:2826:802d:88c4:ee3b:53d4', '2001:660:3302:2826:1872:e259:79f3:f7ac',
# '2001:660:3302:2826:3082:5d79:9c6f:bab0', '2001:660:3302:2826:24f3:ed5c:1f4e:9bb2', '192.168.1.67',
# '2001:660:3302:2826:78d8:2479:d14f:d2e5', '2001:660:3302:2826:5dd:f3fb:9480:f41f',
# '2001:660:3302:2826:2ca0:8b67:bce1:4453', '2001:660:3302:2826:75e0:6094:2a2d:46da']
def getRlocSet(rawCSV_file):
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
                responseList1.append(None)
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    if lines[14].split(',')[1] == "195.59.156.123":
                        responseList1.append(1)
                    elif lines[14].split(',')[1] == "195.59.156.124":
                        responseList1.append(2)
                else:
                    print "There are more than 2 RLOCs together"
            else:
                print "Unknown type exists"
    return responseList1





time = []
time = getTime(rawCSV_file1)
print "time", time


rlocSet1 = getRlocSet(rawCSV_file1)
print "rlocSet1:", rlocSet1.__len__()
rlocSet2 = getRlocSet(rawCSV_file2)
print "rlocSet2:", rlocSet2.__len__()
rlocSet3 = getRlocSet(rawCSV_file3)
print "rlocSet3:", rlocSet3.__len__()
rlocSet4 = getRlocSet(rawCSV_file4)
print "rlocSet4:", rlocSet4.__len__()
rlocSet5 = getRlocSet(rawCSV_file5)
print "rlocSet5:", rlocSet5.__len__()
rlocSet6 = getRlocSet(rawCSV_file6)
print "rlocSet6:", rlocSet6.__len__()
rlocSet7 = getRlocSet(rawCSV_file7)
print "rlocSet7:", rlocSet7.__len__()
rlocSet8 = getRlocSet(rawCSV_file8)
print "rlocSet8:", rlocSet8.__len__()
rlocSet9 = getRlocSet(rawCSV_file9)
print "rlocSet9:", rlocSet9.__len__()
rlocSet10 = getRlocSet(rawCSV_file10)
print "rlocSet10:", rlocSet10.__len__()
rlocSet11 = getRlocSet(rawCSV_file11)
print "rlocSet11:", rlocSet11.__len__()
rlocSet12 = getRlocSet(rawCSV_file12)
print "rlocSet12:", rlocSet12.__len__()
rlocSet13 = getRlocSet(rawCSV_file13)
print "rlocSet13:", rlocSet13.__len__()


plt.plot(time, rlocSet1)
plt.plot(time, rlocSet2)
plt.plot(time, rlocSet3)
plt.plot(time, rlocSet4)
plt.plot(time, rlocSet5)
plt.plot(time, rlocSet6)
plt.plot(time, rlocSet7)
plt.plot(time, rlocSet8)
plt.plot(time, rlocSet9)
plt.plot(time, rlocSet10)
plt.plot(time, rlocSet11)
plt.plot(time, rlocSet12)
plt.plot(time, rlocSet13)


response = np.linspace(-1, 3, 5)
plt.xlabel("Experiment numbers")
plt.ylabel("Responses from 13 MRs")
plt.title("Responses from 13 different MRs for EID-153.16.47.16 over time")
plt.xlim(0,802)
plt.ylim(0.9, 2.1)
# plt.yticks([-1, 0], ('Negative Reply', 'No Map Reply'))
# plt.yticks(response, ('Negative Reply', 'No Map Reply', '82.121.231.67', '192.168.1.66', '132.227.85.231'))

# plt.legend()

# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_MR', 'Responses_from_13_different_MRs_for_EID-153_16_47_16_over_time.eps'),
#             dpi=300, transparent=True)
plt.show()