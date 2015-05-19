# -* coding:UTF-8 -*
# __author__ = 'yueli'

import numpy as np
import matplotlib.pyplot as plt
# All the codes in this python file can be referenced to
# http://matplotlib.org/1.2.1/examples/pylab_examples/pie_demo.html

# 由于此文件的input文件已不存在，所以此文件已被Pie_chart_v4.py替代

# Import the targeted raw CSV file
rawCSV_file1 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_liege.csv"
rawCSV_file2 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_temple.csv"
rawCSV_file3 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_ucl.csv"
rawCSV_file4 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_umass.csv"
rawCSV_file5 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time_wiilab.csv"
rawCSV_files = [rawCSV_file1, rawCSV_file2, rawCSV_file3, rawCSV_file4, rawCSV_file5]

negativeReplyCount = 0
printSkippedCount = 0
reConfiguration1 = 0
reConfiguration2 = 0
flapping1 = 0
flapping2 = 0
mobility1 = 0
mobility2 = 0
for rawCSV_file in rawCSV_files:

    for line in open(rawCSV_file):
        lines = line.split(";")
        if lines[0] == "Vantage":
            continue
        elif lines[4] == "True":
            continue
        else:
            if "NegativeReply" in lines[5]:
                print "Negative Reply", lines[1]
                negativeReplyCount = negativeReplyCount + 1
            elif "PrintSkipped" in lines[5]:
                printSkippedCount = printSkippedCount + 1
            else:
                # in the 5 comparison_time_vp.csv files, we find out that in the situation of flapping, the max locator_count is 2 and the max locators is 10.
                # So we use lines[6] == 2 and lines[8] == 10 as the boundaries between flappings and mobilities
                if int(lines[6]) <= 2:
                    if int(lines[6]) == 1:
                        if int(lines[8]) <= 11:
                            if lines[11] == "False":
                                reConfiguration1 = reConfiguration1 + 1
                            else:
                                # print "flapping1 happens in:", lines[1]
                                flapping1 = flapping1 + 1
                        else:
                            mobility1 = mobility1 + 1
                    else:
                        if lines[10] == "False":
                            # print "reConfiguration2 happens in:", lines[1]
                            reConfiguration2 = reConfiguration2 + 1
                        else:
                            # print "flapping2 happens in:", lines[1]
                            flapping2 = flapping2 + 1
                else:
                    mobility2 = mobility2 + 1


# The slices will be ordered and plotted counter-clockwise.
labels = 'Negative + Normal Reply', 'PrintSkipped + Normal Reply', 'Reconfiguration I', 'Reconfiguration II',\
         'Flapping I', 'Flapping II', 'Mobility I', 'Mobility II'
fracs = [negativeReplyCount, printSkippedCount, reConfiguration1, reConfiguration2, flapping1, flapping2, mobility1, mobility2]
print fracs
colors = ['red', 'orange', 'yellow', 'green', 'lightskyblue', 'blue', 'purple', 'yellowgreen']
explode=(0, 0, 0, 0, 0, 0, 0, 0)


# autopct='%1.2f%%' means that the pie chart will display 2 decimal points
plt.pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', startangle=345)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.

# plt.title('Percentage of each False case', bbox={'facecolor':'0.8', 'pad':5})
plt.title('Percentage of each inconsistent case by the variable of time')
#plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_time/Pie_chart_2_11.pdf")
plt.show()