__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.44.144-MR-173.36.254.164.log.csv')

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
            if lines[14].split(',')[1] == "85.0.211.101":
                plotData.append(1)
            elif lines[14].split(',')[1] == "178.194.96.228":
                plotData.append(2)
            else:
                plotData.append(3)
        elif lines[0] == "RoundNoReply":
            plotData.append(0)
        else:
            plotData.append(99)

# Plot begins here

plt.scatter(time, plotData, color='blue', s=30)

plt.xlabel("Experiment number", fontsize=16)
plt.ylabel("Response from MR", fontsize=16)
plt.title("Response from MR-173.36.254.164 for EID-153.16.44.144 over time in VP1", fontsize=18)
plt.yticks([0, 1, 2], ['No Map Reply', '85.0.211.101', '178.194.96.228'], fontsize=12)
plt.xlim(0,801)
plt.ylim(-0.2, 2.2)

# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_time', 'Case3-1.eps'),
#             dpi=300, transparent=True)
plt.show()