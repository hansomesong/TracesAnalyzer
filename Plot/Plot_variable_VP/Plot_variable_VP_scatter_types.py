__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file1 = os.path.join(CSV_FILE_DESTDIR, 'For_different_5_VP/Deleted_database',
                            "liege-EID-153.16.22.216-MR-149.20.48.61.log.csv")

rawCSV_file2 = os.path.join(CSV_FILE_DESTDIR, 'For_different_5_VP/Deleted_database',
                            "temple-EID-153.16.22.216-MR-149.20.48.61.log.csv")

rawCSV_file3 = os.path.join(CSV_FILE_DESTDIR, 'For_different_5_VP/Deleted_database',
                            "ucl-EID-153.16.22.216-MR-149.20.48.61.log.csv")

rawCSV_file4 = os.path.join(CSV_FILE_DESTDIR, 'For_different_5_VP/Deleted_database',
                            "umass-EID-153.16.22.216-MR-149.20.48.61.log.csv")

rawCSV_file5 = os.path.join(CSV_FILE_DESTDIR, 'For_different_5_VP/Deleted_database',
                            "wiilab-EID-153.16.22.216-MR-149.20.48.61.log.csv")


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



allResponse = []
# Define a function to get all different responses from 5 Vantage Points
def getAllResponse(rawCSV_file):
    i = -1
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            continue
        else:
            if lines[0] == "NegativeReply":
                if "-1.-1.-1.-1" in allResponse:
                    continue
                else:
                    allResponse.append("-1.-1.-1.-1")
            elif lines[0] == "RoundNoReply":
                if "0.0.0.0" in allResponse:
                    continue
                else:
                    allResponse.append("0.0.0.0")
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    if lines[15] in allResponse:
                        continue
                    else:
                        allResponse.append(lines[15])
                elif int(lines[9]) == 2:
                    if (lines[15] and lines[20]) in allResponse:
                        continue
                    elif (lines[15] in allResponse) and (lines[20] not in allResponse):
                        allResponse.append(lines[20])
                    elif (lines[15] not in allResponse) and (lines[20] in allResponse):
                        allResponse.append(lines[15])
                    else:
                        allResponse.append(lines[15])
                        allResponse.append(lines[20])
            else:
                allResponse.append("999.999.999.999")
    return allResponse




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
    responseList2 = []
    for line in open(rawCSV_file):
        i = i + 1
        lines = line.split(";")
        if lines[0] == "Round Type":
            print "Round Type"
            continue
        else:
            if lines[0] == "NegativeReply":
                print "Done"
                responseList1.append(-1)
                responseList2.append(-1)
            elif lines[0] == "RoundNoReply":
                responseList1.append(0)
                responseList2.append(0)
            elif lines[0] == "RoundNormal":
                if int(lines[9]) == 1:
                    if allResponse.index(lines[15]) == (allResponse.__len__()-1):
                        responseList1.append(11)
                        responseList2.append(11)
                    else:
                        responseList1.append(allResponse.index(lines[15]))
                        responseList2.append(allResponse.index(lines[15]))
                elif int(lines[9]) == 2:
                    if allResponse.index(lines[15]) == (allResponse.__len__()-1):
                        responseList1.append(11)
                    else:
                        responseList1.append(allResponse.index(lines[15]))
                    if allResponse.index(lines[20]) == (allResponse.__len__()-1):
                        responseList2.append(11)
                    else:
                        responseList2.append(allResponse.index(lines[20]))
                else:
                    print "There are more than 3 RLOCs together"
            else:
                print "Unknown type exists"
    return responseList1, responseList2





time = []
time = getTime(rawCSV_file1)
print "time", time

getAllResponse(rawCSV_file1)
getAllResponse(rawCSV_file2)
getAllResponse(rawCSV_file3)
getAllResponse(rawCSV_file4)
getAllResponse(rawCSV_file5)
print allResponse

rlocSet1_1, rlocSet1_2 = getRlocSet(rawCSV_file1)
print "rlocSet1_1:", rlocSet1_1.__len__()
print "rlocSet1_2:", rlocSet1_2.__len__()
rlocSet2_1, rlocSet2_2 = getRlocSet(rawCSV_file2)
print "rlocSet2_1:", rlocSet2_1.__len__()
print "rlocSet2_2:", rlocSet2_2.__len__()
rlocSet3_1, rlocSet3_2 = getRlocSet(rawCSV_file3)
print "rlocSet3_1:", rlocSet3_1.__len__()
print "rlocSet3_2:", rlocSet3_2.__len__()
rlocSet4_1, rlocSet4_2 = getRlocSet(rawCSV_file4)
print "rlocSet4_1:", rlocSet4_1.__len__()
print "rlocSet4_2:", rlocSet4_2.__len__()
rlocSet5_1, rlocSet5_2 = getRlocSet(rawCSV_file5)
print "rlocSet5_1:", rlocSet5_1.__len__()
print "rlocSet5_2:", rlocSet5_2.__len__()

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(16,8)
# plt.gcf().set_dpi(300)

# Plot begins here, "-1" means the response is "Negative Reply", "0" means the response is "No Map Reply"
# "1" means the RLOC set is "82.121.231.67", "2" means the RLOC set is "192.168.1.66",
# "3" means the RLOC set is "132.227.85.231", "10" means the RLOC set is others
plt.scatter(time, rlocSet1_1, color='purple', marker="o", label="VP1", s=100)
plt.scatter(time, rlocSet1_2, color='purple', marker='o', s=100)
plt.scatter(time, rlocSet2_1, color='green', marker='>', label="VP2", s=100)
plt.scatter(time, rlocSet2_2, color='green', marker='>', s=100)
plt.scatter(time, rlocSet3_1, color='red', marker=(5,0), label = "VP3", s=100)
plt.scatter(time, rlocSet3_2, color='red', marker=(5,0), s=100)
plt.scatter(time, rlocSet4_1, color='orange', marker='*', label = "VP4", s=100)
plt.scatter(time, rlocSet4_2, color='orange', marker='*', s=100)
plt.scatter(time, rlocSet5_1, color='blue', marker='+', label = "VP5", s=100)
plt.scatter(time, rlocSet5_2, color='blue', marker='+', s=100)

response = np.linspace(-1, 14, 16)
plt.xlabel("Experiment numbers", fontsize=18)
plt.ylabel("Different Map Replies", fontsize=18)
# plt.title("Map Replies over time for EID-153.16.22.216 from MR-149.20.48.61 in 5 VPs", fontsize=22)
plt.xlim(0,750)
# plt.yticks([-1, 0], ('Negative Reply', 'No Map Reply'))
# plt.yticks(response, ('Negative Reply', 'No Map Reply', '192.168.1.66', '132.227.85.238',
#                       '2001:660:3302:2826:6cac:405f:8937:719c', '217.8.97.6', '2001:660:3302:2826:802d:88c4:ee3b:53d4',
#                       '2001:660:3302:2826:1872:e259:79f3:f7ac', '2001:660:3302:2826:3082:5d79:9c6f:bab0',
#                       '2001:660:3302:2826:24f3:ed5c:1f4e:9bb2', '192.168.1.67',
#                       '2001:660:3302:2826:78d8:2479:d14f:d2e5', '0.0.0.0', '2001:660:3302:2826:2ca0:8b67:bce1:4453',
#                       '2001:660:3302:2826:75e0:6094:2a2d:46da', '2001:660:3302:2826:5dd:f3fb:9480:f41f'))
plt.yticks(response, ('Negative Reply', 'No Map Reply', 'RLOC 1', 'RLOC 2', 'RLOC 3', 'RLOC 4',
                      'RLOC 5', 'RLOC 6', 'RLOC 7', 'RLOC 8', 'RLOC 9', 'RLOC 10',
                      'RLOC 11', 'RLOC 12', 'RLOC 13'), fontsize=14)

plt.legend()

plt.savefig(
    os.path.join(PLOT_DIR, 'Plot_variable_VP', 'Plot_variable_VP_different_types.eps'),
    dpi=300,
    # transparent=True
)
plt.show()

