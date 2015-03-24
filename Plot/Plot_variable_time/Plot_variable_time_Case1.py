__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/log2csv/planetlab1-EID-153.16.30.160-MR-149.20.48.61.log.csv"

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
        if lines[0] == "RoundNoReply":
            plotData.append(0)
        elif lines[0] == "NegativeReply":
            plotData.append(-1)
        elif lines[0] == "RoundNormal":
            if lines[15] == "24.51.210.242":
                plotData.append(1)
            elif lines[15] == "24.51.218.201":
                plotData.append(2)
            else:
                plotData.append(99)
        else:
            plotData.append(99)

# Plot begins here, "-1" means Negative, "0" means No Map Reply, "1" means have 1 RLOC set, "2" means have 2 RLOC sets
plt.scatter(time, plotData, color='blue', s=30)

plt.xlim(-50, 850)
#plt.ylim(-1.5,2.5)

plt.xlabel("Experiment number", fontsize=16)
plt.ylabel("Response from MR", fontsize=16)
plt.title("Response from MR-149.20.48.61 for EID-153.16.30.160 over time in VP1", fontsize=18)
plt.yticks([-1, 0, 1, 2], ['Negative Reply', 'No Map Reply', '24.51.210.242', '24.51.218.201'], fontsize=12)
plt.xlim(0,801)
plt.ylim(-1.5, 2.5)


#plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Case1.pdf")
plt.show()

