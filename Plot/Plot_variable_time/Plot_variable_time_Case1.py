__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.30.160-MR-149.20.48.61.log.csv')

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
            if lines[14].split(',')[1] == "24.51.210.242":
                plotData.append(1)
            elif lines[14].split(',')[1] == "24.51.218.201":
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
# plt.title("Response from MR-149.20.48.61 for EID-153.16.30.160 over time in VP1", fontsize=18)
plt.yticks([-1, 0, 1, 2], ['Negative Reply', 'No Map Reply', 'RLOC1', 'RLOC2'], fontsize=12)
plt.xlim(0,801)
plt.ylim(-1.5, 2.5)
# plt.figure(figsize=(100,100))
# plt.gif().set_size_inches(18.5,10.5)

# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_time', 'Case1.eps'), dpi=300, transparent=True)
plt.show()

