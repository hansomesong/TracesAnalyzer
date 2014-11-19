__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/planetlab1-EID-37.77.57.64-MR-149.20.48.61.log.csv"

time = []
plotData = []
i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[0] == "Round Type":
        continue
    else:
        if int(lines[9]) == 2:
            if (lines[15] == "87.195.36.39" and lines[20] == "95.97.176.115") \
                    or (lines[15] == "95.97.176.115" and lines[20] == "87.195.36.39"):
                time.append(i)
                plotData.append(2)
        elif int(lines[9]) == 3:
            if (lines[15] == "87.195.36.39" and lines[20] == "95.97.176.115" and lines[25] == "2001:9e0:8500:c00::1") \
                    or (lines[15] == "95.97.176.115" and lines[20] == "87.195.36.39" and lines[25] == "2001:9e0:8500:c00::1"):
                time.append(i)
                plotData.append(3)
        else:
            plotData.append(0)

print len(time)
# Plot begins here, "2" means have 2 RLOC sets, "3" means have 3 RLOC sets
plt.plot(time, plotData)

plt.xlabel("Experiment number")
plt.ylabel("Numbers of RLOC set")
plt.title("Response from MR-149.20.48.61 for EID-37.77.57.64 by time at liege")
plt.yticks([2, 3], ['2 RLOC sets', '3 RLOC sets'])
plt.xlim(0,755)
plt.ylim(0,4)

plt.annotate('2013/07/10 02:30',xy=(375,3),xytext=(375,3.1),arrowprops=dict(arrowstyle="->"))

plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Case1.pdf")
plt.show()

