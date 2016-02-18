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


# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(27, 17)

# Define font
font_label = {
    'fontname'   : 'Times New Roman',
    'color'      : 'black',
    'fontsize'   : 70
       }


# Plot begins here
# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
# plt.gcf().set_size_inches(8,6)
# plt.gcf().set_dpi(300)

plt.scatter(time, plotData, color='black', s=200)

plt.xlabel("experiment number", font_label)
plt.ylabel("response from MR", font_label)
# plt.title("Response from MR-173.36.254.164 for EID-153.16.44.144 over time in VP1", fontsize=18)
plt.xticks(fontsize=45, fontname='Times New Roman')
plt.yticks([0, 1, 2], ['No Map-\nReply', 'RLOC1', 'RLOC2'], fontsize=45, fontname='Times New Roman')
plt.xlim(0,801)
plt.ylim(-0.2, 2.2)

plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'Case3-1.eps'),
            dpi=300, transparent=True)
# plt.show()