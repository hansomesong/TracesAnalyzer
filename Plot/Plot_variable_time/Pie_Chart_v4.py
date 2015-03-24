__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
# All the codes in this python file can be referenced to
# http://matplotlib.org/1.2.1/examples/pylab_examples/pie_demo.html

# Import the targeted raw CSV file
rawCSV_file1 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_liege.csv"
rawCSV_file2 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_temple.csv"
rawCSV_file3 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_ucl.csv"
rawCSV_file4 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_umass.csv"
rawCSV_file5 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_wiilab.csv"
rawCSV_files = [rawCSV_file1, rawCSV_file2, rawCSV_file3, rawCSV_file4, rawCSV_file5]

stability = 0
newDeployment = 0
mobility = 0
reConfiguration = 0
RLOCMadness = 0
elseCase = 0
for rawCSV_file in rawCSV_files:

    with open(rawCSV_file) as f:
        next(f)
        for line in f:
        #for line in next(open(rawCSV_file)):
            lines = line.rstrip('\r\n').split(";")
            if lines[12] == "0":
                stability = stability + 1
            elif lines[12] == "1":
                newDeployment = newDeployment + 1
            elif lines[12] == "2":
                mobility = mobility + 1
            elif lines[12] == "3":
                reConfiguration = reConfiguration + 1
            elif lines[12] == "4":
                RLOCMadness = RLOCMadness + 1
            else:
                elseCase = elseCase + 1

print "True: ", stability
print "Percentage of True: ", float(stability)/float((stability + newDeployment + mobility + reConfiguration + RLOCMadness + elseCase))*100, "%"
# The slices will be ordered and plotted counter-clockwise.
labels = 'New Deployment', 'Mobility', 'Reconfiguration', 'RLOC Madness'
fracs = [newDeployment, mobility, reConfiguration, RLOCMadness]
print fracs
colors = ['lightskyblue', 'red', 'yellow', 'green']
explode=(0, 0, 0, 0)


# autopct='%1.2f%%' means that the pie chart will display 2 decimal points
plt.pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', startangle=345)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.

# plt.title('Percentage of each False case', bbox={'facecolor':'0.8', 'pad':5})
plt.title('Percentage of each instable case by the variable of time')
plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Pie_chart_v4.pdf")
plt.show()