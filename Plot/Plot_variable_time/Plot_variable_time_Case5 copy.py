__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/planetlab2-EID-153.16.3.0-MR-173.36.254.164.log.csv"

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
        elif lines[0] == "RoundNormalNoLocatorInfo":
            plotData.append(2)
        else:
            plotData.append(10)
print plotData
# Plot begins here, "2" means !!!! LCAF AFI print skipped !!!!; "0" means No map-reply received
plt.scatter(time, plotData, color='blue', s=0.5)

plt.annotate('LCAF AFI print skipped',xy=(0,2.03),xytext=(0,2.1),arrowprops=dict(arrowstyle="->"))
plt.annotate('No Map Reply',xy=(100,0.03),xytext=(110,0.18),arrowprops=dict(arrowstyle="->"))

plt.xlabel("Time (2013/07/02 07:30 - 2013/07/18 23:30)")
plt.ylabel("Number of RLOC set")
plt.title("Response from MR-173.36.254.164 for EID-153.16.3.0 by time")

plt.xlim(-50, 800)
plt.ylim(-0.3, 2.2)

plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_time/Case5_copy.pdf")
plt.show()