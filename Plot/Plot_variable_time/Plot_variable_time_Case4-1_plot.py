__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.47.16-MR-149.20.48.61.log.csv')

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
            if lines[14].split(',')[1] == "195.59.156.123":
                dataPlot.append(1)
            elif lines[14].split(',')[1] == "195.59.156.124":
                dataPlot.append(2)
            else:
                dataPlot.append(3)
        elif lines[0] == "RoundNoReply":
            dataPlot.append(0)
        else:
            dataPlot.append(99)

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(22, 14)

# Plot begins here
plt.plot(time, dataPlot, color="black")

plt.xlabel("experiment number", fontsize=50)
plt.ylabel("response from MR", fontsize=50)
# plt.title("Response from MR-149.20.48.61 for EID-153.16.47.16 over time in VP1", fontsize=18)
plt.xticks(fontsize=35)
plt.yticks([0, 1, 2], ['No Map-\nReply', 'RLOC1', 'RLOC2'], fontsize=32)
plt.xlim(0,801)
plt.ylim(-0.2, 2.2)

plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_time', 'Case4-1_plot.eps'), dpi=300)
# plt.show()