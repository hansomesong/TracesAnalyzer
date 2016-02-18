__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
import socket
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.18.176-MR-217.8.98.46.log.csv')

time = []
unsortedRlocList = []

i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[LOG_COLUMN['round_type']] == "Round Type":
        continue
    else:
        #time.append(i)
        if lines[LOG_COLUMN['round_type']] == "RoundNoReply":
            if "0.0.0.0" in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append("0.0.0.0")
        elif int(lines[LOG_COLUMN['locator_count']]) == 1:
            if lines[LOG_COLUMN['locator_id']].split(',')[1] in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append(lines[LOG_COLUMN['locator_id']].split(',')[1])
        else:
            if "-999.999.999.999" in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append("-999.999.999.999")

#print unsortedRlocList
#sortedRlocList = sorted(unsortedRlocList, key=lambda item: socket.inet_aton(item))
#print sortedRlocList

sortedRlocList =[]
sortedRlocList.append("0.0.0.0")
for k in unsortedRlocList:
    if k == "0.0.0.0":
        continue
    else:
        sortedRlocList.append(k)

#print "sortedRlocList:", sortedRlocList
#print "sortedRlocList.__len__():", sortedRlocList.__len__()

j = -1
rlocList = []
for line1 in open(rawCSV_file):
    j = j + 1
    lines1 = line1.split(";")
    if lines1[LOG_COLUMN['round_type']] == "Round Type":
        continue
    else:
        time.append(j)
        if lines1[LOG_COLUMN['round_type']] == "RoundNoReply":
            rlocList.append(sortedRlocList.index("0.0.0.0"))
        elif int(lines1[LOG_COLUMN['locator_count']]) == 1:
            rlocList.append(sortedRlocList.index(lines1[LOG_COLUMN['locator_id']].split(',')[1]))
        else:
            rlocList.append(sortedRlocList.index("-999.999.999.999"))

print "time.__len__():", time.__len__()
print "rlocList:", rlocList
print "rlocList.__len__():", rlocList.__len__()


# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(22, 14)

#Plot begins here
plt.scatter(time, rlocList, color="black", label="RLOCset", s=5)

plt.xlim(-50,800)
plt.ylim(-5,75)

plt.xlabel("experiment number", fontsize=50)
plt.ylabel("responses from MR", fontsize=50)
# plt.title("Response from MR-217.8.98.46 for EID-153.16.18.176 over time in VP1")
plt.xticks(fontsize=35)
plt.yticks(np.linspace(0, 70, 8), ['No Map-\nReply', 'RLOC10', 'RLOC20', 'RLOC30', 'RLOC40', 'RLOC50', 'RLOC60', 'RLOC70'], fontsize=32)

# plt.annotate('No Map Reply',xy=(300,0),xytext=(300,4),arrowprops=dict(arrowstyle="->"))

plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_time', 'Case4-3.eps'), dpi=300, transparent=True)
# plt.show()