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
    i = -1
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


plt.scatter(time, rlocSet1, color='purple', marker="o", label="VP1", s=100)
plt.scatter(time, rlocSet2, color='green', marker='>', label="VP2", s=100)
plt.scatter(time, rlocSet3, color='red', marker=(5,0), label = "VP3", s=100)
plt.scatter(time, rlocSet4, color='orange', marker='*', label = "VP4", s=100)
plt.scatter(time, rlocSet5, color='blue', marker='+', label = "VP5", s=100)


response = np.linspace(-1, 2, 4)
plt.xlabel("Experiment numbers", fontsize=16)
plt.ylabel("Different Map Replies", fontsize=16)
plt.title("Map Replies over time for EID-153.16.47.16 from MR-198.6.255.37 in 5 VPs", fontsize=20)
# plt.xlim(0,798)
plt.xlim(550, 600)
plt.ylim(-2, 3)
plt.yticks(response, ('Negative Reply', 'No Map Reply', 'RLOC 1', 'RLOC 2'), fontsize=12)

# loc=1 makes legend locating at right-up;
# loc=2 makes legend locating at left-up;
# loc=3 makes legend locating at left-down
# loc=4 makes legend locating at right-down
plt.legend(loc=4)

plt.savefig(
    os.path.join(PLOT_DIR, 'Plot_variable_VP', 'Plot_variable_VP_different_RLOCs.eps'),
    dpi=300,
    transparent=True
)

plt.show()