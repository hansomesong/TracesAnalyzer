__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/planetlab1-EID-205.203.201.0-MR-202.214.86.252.log.csv"

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
        elif int(lines[9]) == 0:
            plotData.append(-1)
        elif int(lines[9]) == 1:
            plotData.append(1)
        elif int(lines[9]) == 2:
            plotData.append(2)
        else:
            plotData.append(10)

# Plot begins here, "-1" means Negative, "0" means No Map Reply, "1" means have 1 RLOC set, "2" means have 2 RLOC sets
plt.scatter(time, plotData, color='blue', s=1)

plt.xlim(-50, 850)
#plt.ylim(-1.5,2.5)

plt.xlabel("Experiment number")
plt.ylabel("Response from MR")
plt.title("Response from MR-202.214.86.252 for EID-205.203.201.0 by time")
plt.yticks([-1, 1, 2], ['Forward Native', '1 RLOC sets', '2 RLOC sets'])
plt.xlim(0,755)
plt.ylim(-1.5, 2.5)

# plt.annotate('', xy=(20,-0.9), xytext=(20,-0.85), arrowprops=dict(arrowstyle="->"))
# plt.annotate('', xy=(107,1.9), xytext=(107,1.75), arrowprops=dict(arrowstyle="->"))
# plt.annotate('', xy=(117,2.03), xytext=(117,2.15), arrowprops=dict(arrowstyle="->"))
# plt.annotate('', xy=(283,-0.9), xytext=(283,-0.85), arrowprops=dict(arrowstyle="->"))

plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Case4.pdf")
plt.show()

