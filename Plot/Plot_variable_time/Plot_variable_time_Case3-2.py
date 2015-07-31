__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-37.77.57.64-MR-149.20.48.61.log.csv')

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
            if (lines[14].split(',')[1] == "87.195.36.39" and lines[15].split(',')[1] == "95.97.176.115") \
                    or (lines[14].split(',')[1] == "95.97.176.115" and lines[20] == "87.195.36.39"):
                time.append(i)
                plotData.append(2)
        elif int(lines[9]) == 3:
            if (lines[14].split(',')[1] == "87.195.36.39" and lines[15].split(',')[1] == "95.97.176.115" and lines[16].split(',')[1] == "2001:9e0:8500:c00::1") \
                    or (lines[14].split(',')[1] == "95.97.176.115" and lines[15].split(',')[1] == "87.195.36.39" and lines[16].split(',')[1] == "2001:9e0:8500:c00::1"):
                time.append(i)
                plotData.append(3)
        else:
            plotData.append(0)

print len(time)
# Plot begins here, "2" means have 2 RLOC sets, "3" means have 3 RLOC sets
plt.scatter(time, plotData, color='blue', s=25)

plt.xlabel("Experiment number", fontsize=16)
plt.ylabel("Numbers of Locator", fontsize=16)
# plt.title("Response from MR-149.20.48.61 for EID-37.77.57.64 over time in VP1", fontsize=18)
plt.yticks([2, 3], ['2 Locators', '3 Locators'], fontsize=12)
plt.xlim(0,755)
plt.ylim(1.5, 3.5)

# plt.annotate('2013/07/10 02:30',xy=(375,3),xytext=(375,3.1),arrowprops=dict(arrowstyle="->"))

# plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_time', 'Case3-2.eps'),
#             dpi=300, transparent=True)
plt.show()

