__author__ = 'yueli'
from pylab import *
import matplotlib.pyplot as plt

# Plot the percentage of False
# (which means that the responses from a Map Resolver for a dedicated EID during the whole measurements are different)
# for every vantage point: liege, temple, ucl, umass, wiilab
totalCount = 614
trueCountList = [(614-9), (614-7), (614-9), (614-7), (614-8)]
percentageTrueList = []

for TrueCount in trueCountList:
    percentageTrueList.append(float(TrueCount) / float(totalCount) * 100)

print "Each consistent percentage of VP", percentageTrueList

print "Average of the consistent percentage for 5VPs", average(percentageTrueList), "%"

n_groups = 5
indexs = np.arange(n_groups)
bar_width = 0.35

plt.grid(True)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        print "height:", height
        plt.text(rect.get_x()+rect.get_width()/2-0.15, 1.0003*height, '%s' % round(height,2))

# Control the opacity of the bar color
# opacity = 0.4
# rects1 = plt.bar(index, percentageFalseList, bar_width, alpha=opacity, color='b',label='Men')


plt.xlabel('vantage point',fontsize=16)
plt.ylabel('percentage of consistency (%)', fontsize=16)
plt.title('Percentage of consistency for 5 vantage points', fontsize=18)
plt.xticks(indexs + bar_width/2, ('1', '2', '3', '4', '5'), fontsize=16)
plt.xlim(-0.3, 4.7)
plt.ylim(98,99)
# plt.ylim(0,1)
# plt.yticks((0,1), ('0', '1'))
rect = plt.bar(indexs, percentageTrueList, bar_width, color='b')
autolabel(rect)
savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Percentage_consistency_5VP_MR.pdf")
plt.tight_layout()
plt.show()