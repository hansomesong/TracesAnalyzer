__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/log2csv/planetlab1-EID-153.16.44.144-MR-173.36.254.164.log.csv"

# In this situation(this file), there is only RoundNormal and NoMapReply, no other types of reply, so the judgement is quite simple
time = []
plotData = []
i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[0] == "Round Type":
        continue
    else:
        time.append(i)
        if lines[0] == "RoundNormal":
            if lines[15] == "85.0.211.101":
                plotData.append(1)
            elif lines[15] == "178.194.96.228":
                plotData.append(2)
            else:
                plotData.append(3)
        elif lines[0] == "RoundNoReply":
            plotData.append(0)
        else:
            plotData.append(99)

# Plot begins here
plt.scatter(time, plotData, color='blue', s=1)

plt.xlabel("Experiment number")
plt.ylabel("Response from MR")
plt.title("Response from MR-173.36.254.164 for EID-153.16.44.144 by time")
plt.yticks([0, 1, 2], ['No Map Reply', '85.0.211.101', '178.194.96.228'])
plt.xlim(0,801)
plt.ylim(-0.2, 2.2)

# plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Case3.pdf")
plt.show()