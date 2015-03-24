__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/log2csv/planetlab1-EID-153.16.47.16-MR-149.20.48.61.log.csv"

# In this situation(this file), there is only RoundNormal and NoMapReply, no other types of reply, so the judgement is quite simple
time = []
dataPlot = []
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
                dataPlot.append(1)
            elif lines[15] == "195.59.156.124":
                dataPlot.append(2)
            else:
                dataPlot.append(3)
        elif lines[0] == "RoundNoReply":
            dataPlot.append(0)
        else:
            dataPlot.append(99)

# Plot begins here
plt.plot(time, dataPlot, color="blue")

plt.xlabel("Measurement number", fontsize=16)
plt.ylabel("Response from MR", fontsize=16)
# plt.title("Response from MR-149.20.48.61 for EID-153.16.47.16 in VP liege over time", fontsize=22)
plt.title("Response from MR-149.20.48.61 for EID-153.16.47.16 over time in VP1", fontsize=18)
plt.yticks([0, 1, 2], ['No Map Reply', '195.59.156.123', '195.59.156.124'], fontsize=12)
plt.xlim(0,801)
plt.ylim(-0.2, 2.2)

#plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Case4-1_plot.pdf")
plt.show()