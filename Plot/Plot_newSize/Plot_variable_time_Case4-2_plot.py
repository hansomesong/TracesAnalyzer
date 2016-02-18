__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.14.0-MR-193.162.145.50.log.csv')

time = []
noMapReply = []
dataplot = []
i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[0] == "Round Type":
        continue
    else:
        time.append(i)
        if lines[0] == "RoundNoReply":
            dataplot.append(0)
        elif int(lines[9]) == 1:
            if lines[14].split(',')[1] == "166.149.122.123":
                dataplot.append(1)
            elif lines[14].split(',')[1] == "166.149.122.124":
                dataplot.append(1)
            elif lines[14].split(',')[1] == "166.149.122.125":
                dataplot.append(2)
        elif int(lines[9]) == 2:
            if ((lines[14].split(',')[1] == "166.149.122.123" and lines[15].split(',')[1] == "166.149.122.124")
                or (lines[15].split(',')[1] == "166.149.122.123" and lines[14].split(',')[1] == "166.149.122.124")):
                dataplot.append(1)

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(27, 17)

# Define font
font_label = {
    'fontname'   : 'Times New Roman',
    'color'      : 'black',
    'fontsize'   : 70
       }

# Plot begins here, "0" means No Map Reply, "1" means the RLOC set is "166.149.122.123", "2" means the RLOC set is
# "166.149.122.124", "2" means the RLOC set is "166.149.122.125"
plt.plot(time, dataplot, color="black")

print len(time)

plt.xlim(0, len(time))
plt.ylim(-0.2, 2.2)

plt.xlabel("experiment number", font_label)
plt.ylabel("response from MR", font_label)
# plt.title("Response from MR-193.162.145.50 for EID-153.16.14.0 over time in VP1", fontsize=18)
plt.xticks(fontsize=45, fontname='Times New Roman')
plt.yticks([0, 1, 2], ['No Map-\nReply', 'RLOC1,\nRLOC2', 'RLOC3'], fontsize=45, fontname='Times New Roman')
# plt.legend()

plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'Case4-2_plot.eps'), dpi=300)
# plt.show()