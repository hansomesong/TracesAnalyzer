__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/log2csv/planetlab1-EID-153.16.47.16-MR-149.20.48.61.log.csv"

# In this situation(this file), there is only RoundNormal and NoMapReply, no other types of reply, so the judgement is quite simple
time = []
rloc1 = []
rloc2 = []
noMapReply = []
i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[0] == "Round Type":
        continue
    else:
        time.append(i)
        if lines[0] == "RoundNormal":
            if lines[15] == "195.59.156.123":
                rloc1.append(1)
                rloc2.append(99)
                noMapReply.append(99)
            elif lines[15] == "195.59.156.124":
                rloc1.append(99)
                rloc2.append(2)
                noMapReply.append(99)
            else:
                rloc1.append(99)
                rloc2.append(99)
                noMapReply.append(99)
        elif lines[0] == "RoundNoReply":
            rloc1.append(99)
            rloc2.append(99)
            noMapReply.append(0)
        else:
            rloc1.append(99)
            rloc2.append(99)
            noMapReply.append(99)

# Plot begins here
plt.scatter(time, rloc1, color="blue", label="RLOCset1", s=1)
plt.scatter(time, rloc2, color="red", label="RLOCset2", s=1)
plt.scatter(time, noMapReply, color="green", label="NoMapReply", s=1)

plt.xlabel("Experiment number")
plt.ylabel("Response from MR")
plt.title("Response from MR-149.20.48.61 for EID-153.16.47.16 over time in VP1")
plt.yticks([0, 1, 2], ['No Map Reply', '195.59.156.123', '195.59.156.124'])
plt.xlim(0,801)
plt.ylim(-0.2, 2.2)

# plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Case4-1_scatter.pdf")
plt.show()