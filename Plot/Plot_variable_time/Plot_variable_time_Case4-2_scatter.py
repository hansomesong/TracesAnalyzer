__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.14.0-MR-193.162.145.50.log.csv')

time = []
noMapReply = []
rlocSet1 = []
rlocSet2 = []
rlocSet3 = []
i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[0] == "Round Type":
        continue
    else:
        time.append(i)
        if lines[0] == "RoundNoReply":
            noMapReply.append(0)
            rlocSet1.append(-999)
            # rlocSet2.append(-999)
            rlocSet3.append(-999)
        elif int(lines[9]) == 1:
            if lines[14].split(',')[1] == "166.149.122.123":
                noMapReply.append(-999)
                rlocSet1.append(1)
                # rlocSet2.append(-999)
                rlocSet3.append(-999)
            elif lines[14].split(',')[1] == "166.149.122.124":
                noMapReply.append(-999)
                rlocSet1.append(-999)
                # rlocSet2.append(2)
                rlocSet3.append(-999)
            elif lines[14].split(',')[1] == "166.149.122.125":
                noMapReply.append(-999)
                rlocSet1.append(-999)
                # rlocSet2.append(-999)
                rlocSet3.append(2)
        elif int(lines[9]) == 2:
            if ((lines[14].split(',')[1] == "166.149.122.123" and lines[15].split(',')[1] == "166.149.122.124")
                or (lines[15].split(',')[1] == "166.149.122.123" and lines[14].split(',')[1] == "166.149.122.124")):
                noMapReply.append(-999)
                rlocSet1.append(1)
                # rlocSet2.append(2)
                rlocSet3.append(-999)
            elif ((lines[14].split(',')[1] == "166.149.122.123" and lines[15].split(',')[1] == "166.149.122.125")
                  or (lines[15].split(',')[1] == "166.149.122.123" and lines[14].split(',')[1] == "166.149.122.125")):
                noMapReply.append(-999)
                rlocSet1.append(1)
                # rlocSet2.append(-999)
                rlocSet3.append(2)
            elif ((lines[14].split(',')[1] == "166.149.122.124" and lines[15].split(',')[1] == "166.149.122.125")
                  or (lines[15].split(',')[1] == "166.149.122.124" and lines[14].split(',')[1] == "166.149.122.125")):
                noMapReply.append(-999)
                rlocSet1.append(-999)
                # rlocSet2.append(2)
                rlocSet3.append(2)
        else:
            noMapReply.append(-999)
            rlocSet1.append(-999)
            # rlocSet2.append(-999)
            rlocSet3.append(-999)

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(8,6)

# Plot begins here, "0" means No Map Reply, "1" means the RLOC set is "166.149.122.123", "2" means the RLOC set is
# "166.149.122.124", "2" means the RLOC set is "166.149.122.125"
plt.scatter(time, noMapReply, color="black",  s=30)
plt.scatter(time, rlocSet1, color="blue", label='2 RLOCs', s=30)
# plt.scatter(time, rlocSet2, color="blue", s=30)
plt.scatter(time, rlocSet3, color="red", label='1 RLOC', s=30)

print len(time)

plt.xlim(0,755)
plt.ylim(-0.2, 2.2)

plt.xlabel("experiment number", fontsize=20)
plt.ylabel("response from MR", fontsize=20)
# plt.title("Response from MR-193.162.145.50 for EID-153.16.14.0 over time in VP1", fontsize=18)
plt.yticks([0, 1, 2], ['No Map-\nReply', 'RLOC1,\nRLOC2', 'RLOC3'], fontsize=12)
plt.legend()

plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_time', 'Case4-2_scatter.eps'), dpi=300)
plt.show()