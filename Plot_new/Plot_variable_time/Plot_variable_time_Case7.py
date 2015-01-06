__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/log2csv/planetlab1-EID-153.16.14.0-MR-193.162.145.50.log.csv"

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
            rlocSet2.append(-999)
            rlocSet3.append(-999)
        elif int(lines[9]) == 1:
            if (lines[15] == "166.149.122.123"):
                noMapReply.append(-999)
                rlocSet1.append(1)
                rlocSet2.append(-999)
                rlocSet3.append(-999)
            elif (lines[15] == "166.149.122.124"):
                noMapReply.append(-999)
                rlocSet1.append(-999)
                rlocSet2.append(2)
                rlocSet3.append(-999)
            elif (lines[15] == "166.149.122.125"):
                noMapReply.append(-999)
                rlocSet1.append(-999)
                rlocSet2.append(-999)
                rlocSet3.append(3)
        elif int(lines[9]) == 2:
            if ((lines[15] == "166.149.122.123" and lines[20] == "166.149.122.124")
                or (lines[20] == "166.149.122.123" and lines[15] == "166.149.122.124")):
                noMapReply.append(-999)
                rlocSet1.append(1)
                rlocSet2.append(2)
                rlocSet3.append(-999)
            elif ((lines[15] == "166.149.122.123" and lines[20] == "166.149.122.125")
                  or (lines[20] == "166.149.122.123" and lines[15] == "166.149.122.125")):
                noMapReply.append(-999)
                rlocSet1.append(1)
                rlocSet2.append(-999)
                rlocSet3.append(3)
            elif ((lines[15] == "166.149.122.124" and lines[20] == "166.149.122.125")
                  or (lines[20] == "166.149.122.124" and lines[15] == "166.149.122.125")):
                noMapReply.append(-999)
                rlocSet1.append(-999)
                rlocSet2.append(2)
                rlocSet3.append(3)
        else:
            noMapReply.append(-999)
            rlocSet1.append(-999)
            rlocSet2.append(-999)
            rlocSet3.append(-999)



# Plot begins here, "0" means No Map Reply, "1" means the RLOC set is "166.149.122.123", "2" means the RLOC set is
# "166.149.122.124", "2" means the RLOC set is "166.149.122.125"
plt.scatter(time, noMapReply, color="black", label="NoMapReply", s=1)
plt.scatter(time, rlocSet1, color="blue", label="RLOCset1", s=1)
plt.scatter(time, rlocSet2, color="green", label="RLOCset2", s=1)
plt.scatter(time, rlocSet3, color="red", label="RLOCset3", s= 1)

print len(time)

plt.xlim(0,755)
plt.ylim(-0.5, 3.5)

plt.xlabel("Experiment number")
plt.ylabel("Response from MR")
plt.title("Response from MR-193.162.145.50 for EID-153.16.14.0 by time at liege")
plt.yticks([0, 1, 2, 3], ['No Map Reply', '166.149.122.123', '166.149.122.124', '166.149.122.125'])

# plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Case7.png")
plt.show()