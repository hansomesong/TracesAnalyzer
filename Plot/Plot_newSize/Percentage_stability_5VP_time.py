# -*- coding: utf-8 -*-
__author__ = 'yueli'
from pylab import *
import matplotlib.pyplot as plt
from config.config import *
import numpy as np

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(8, 6.5)

# Plot the percentage of False
# (which means that the responses from a Map Resolver for a dedicated EID during the whole measurements are different)
# for every vantage point: liege, temple, ucl, umass, wiilab
totalCount = 7969
trueCountList = [(7969-674), (7969-677), (7969-705), (7969-668), (7969-666)]
percentageTrueList = []

for TrueCount in trueCountList:
    percentageTrueList.append(float(TrueCount) / float(totalCount) * 100)

print "Each consistent percentage of VP", percentageTrueList

print "Average of the consistent percentage for 5VPs", np.average(percentageTrueList), "%"

n_groups = 5
indexs = np.arange(n_groups)
bar_width = 0.35

# 画 overall 的红色虚线
x_overall_list = [-0.3, 4.7]
y_overall = np.average(percentageTrueList)
y_overall_list = [y_overall, y_overall]

plt.grid(True)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        print "height:", height
        plt.text(rect.get_x()+rect.get_width()/2-0.15, 1.0001*height, '%s' % round(height,2))

# Control the opacity of the bar color
# opacity = 0.4
# rects1 = plt.bar(index, percentageFalseList, bar_width, alpha=opacity, color='b',label='Men')

# Define font
font_label = {
    'fontname'   : 'Times New Roman',
    'color'      : 'black',
    'fontsize'   : 26.5
       }

plt.xlabel('vantage point', font_label)
plt.ylabel('percentage of stability (%)', font_label)
# plt.title('Percentage of stability for 5 vantage points', fontsize=18)
plt.plot(x_overall_list, y_overall_list, '--', color='black', label='overall')
plt.xticks(indexs + bar_width/2, ('1', '2', '3', '4', '5'), fontsize=16, fontname='Times New Roman')
plt.yticks(fontsize=16, fontname='Times New Roman')
plt.xlim(-0.3, 4.7)
plt.ylim(90.8, 91.8)
rect = plt.bar(indexs, percentageTrueList, bar_width, color='gray')
# autolabel(rect)
plt.legend(loc='upper right')
# plt.savefig(
#     os.path.join(PLOT_DIR, 'Percentage_stability_5VP_time.eps'),
#     dpi=300
# )
plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'Percentage_stability_5VP_time.eps'),
            dpi=300, transparent=True)
plt.tight_layout()
plt.show()