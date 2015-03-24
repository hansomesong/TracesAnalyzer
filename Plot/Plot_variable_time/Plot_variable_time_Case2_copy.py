__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/log2csv/planetlab1-EID-153.16.3.0-MR-173.36.254.164.log.csv"

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
        elif lines[0] == "PrintSkipped":
            plotData.append(2)
        else:
            plotData.append(10)
print plotData
print plotData.__len__()
for i in plotData:
    if i == 0:
        print i

print (round(plotData.__len__(),5)-6)/plotData.__len__()*100
print float(18700)/float(39846)
# Plot begins here, "2" means !!!! LCAF AFI print skipped !!!!; "0" means No map-reply received
plt.scatter(time, plotData, color='blue', s=0.5)

plt.annotate('LCAF AFI print skipped',xy=(0,2.03),xytext=(0,2.1),arrowprops=dict(arrowstyle="->"))
plt.annotate('No Map Reply',xy=(100,0.03),xytext=(110,0.18),arrowprops=dict(arrowstyle="->"))

plt.xlabel("Experiment number")
plt.ylabel("Number of RLOC set")
plt.title("Response from MR-173.36.254.164 for EID-153.16.3.0 by time")

plt.xlim(-50, 800)
plt.ylim(-0.3, 2.2)

# plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_time/Case2_copy.pdf")
plt.show()