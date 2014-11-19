__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/planetlab1-EID-153.16.14.0-MR-193.162.145.50.log.csv"

time = []
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
            rlocSet1.append(0)
            rlocSet2.append(0)
            rlocSet3.append(0)
        elif int(lines[9]) == 1:
            if (lines[15] == "166.149.122.123"):
                rlocSet1.append(1)
                rlocSet2.append(0)
                rlocSet3.append(0)
            elif (lines[15] == "166.149.122.124"):
                rlocSet1.append(0)
                rlocSet2.append(2)
                rlocSet3.append(0)
            elif (lines[15] == "166.149.122.125"):
                rlocSet1.append(0)
                rlocSet2.append(0)
                rlocSet3.append(3)
        elif int(lines[9]) == 2:
            if ((lines[15] == "166.149.122.123" and lines[20] == "166.149.122.124")
                or (lines[20] == "166.149.122.123" and lines[15] == "166.149.122.124")):
                rlocSet1.append(1)
                rlocSet2.append(2)
                rlocSet3.append(0)
            elif ((lines[15] == "166.149.122.123" and lines[20] == "166.149.122.125")
                  or (lines[20] == "166.149.122.123" and lines[15] == "166.149.122.125")):
                rlocSet1.append(1)
                rlocSet2.append(0)
                rlocSet3.append(3)
            elif ((lines[15] == "166.149.122.124" and lines[20] == "166.149.122.125")
                  or (lines[20] == "166.149.122.124" and lines[15] == "166.149.122.125")):
                rlocSet1.append(0)
                rlocSet2.append(2)
                rlocSet3.append(3)
        else:
            rlocSet1.append(0)
            rlocSet2.append(0)
            rlocSet3.append(0)



# Plot begins here, "0" means No Map Reply, "1" means the RLOC set is "166.149.122.123", "2" means the RLOC set is
# "166.149.122.124", "2" means the RLOC set is "166.149.122.125"
plt.scatter(time, rlocSet1, color="blue", label="RLOCset1", s=5)
plt.scatter(time, rlocSet2, color="green", label="RLOCset2", s=3)
plt.scatter(time, rlocSet3, color="red", label="RLOCset3", s= 1)

plt.xlabel("Time (2013/07/02 07:30 - 2013/07/18 23:30)")
plt.ylabel("RLOC set")
plt.title("Changes of RLOC sets by time")

plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_time/Case2.png")
plt.show()