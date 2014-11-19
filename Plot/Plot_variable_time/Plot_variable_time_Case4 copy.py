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
plt.plot(time, plotData, color='blue')

plt.xlim(-50, 850)
#plt.ylim(-1.5,2.5)

plt.xlabel("Time (2013/07/02 07:30 - 2013/07/18 23:30)")
plt.ylabel("Number of RLOC set")
plt.title("Response from MR-202.214.86.252 for EID-205.203.201.0 by time")

plt.annotate('2013/07/02 20:00:16',xy=(20,-0.97),xytext=(20,-0.85),arrowprops=dict(arrowstyle="->"))
plt.annotate('02/07/2013 23:30:28',xy=(27,1.03),xytext=(27,1.15),arrowprops=dict(arrowstyle="->"))
plt.annotate('04/07/2013 20:30:43',xy=(110,2.03),xytext=(110,2.15),arrowprops=dict(arrowstyle="->"))
plt.annotate('04/07/2013  21:30:07',xy=(120,0.97),xytext=(120,0.75),arrowprops=dict(arrowstyle="->"))
plt.annotate('2013/07/08 07:30:51',xy=(283,-0.97),xytext=(283,-0.85),arrowprops=dict(arrowstyle="->"))
plt.annotate('08/07/2013  08:30:15',xy=(285,1.03),xytext=(285,1.15),arrowprops=dict(arrowstyle="->"))


plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_time/Case4_copy.png")
plt.show()

