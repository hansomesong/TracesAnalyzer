__author__ = 'yueli'
from pylab import *
import matplotlib.pyplot as plt

# Plot the percentage of False
# (which means that the responses from a Map Resolver for a dedicated EID during the whole measurements are different)
# for every vantage point: liege, temple, ucl, umass, wiilab
totalCount = 7969
falseCountList = [(7969-319), (7969-321), (7969-303), (7969-305), (7969-302)]
percentageFalseList = []

for falseCount in falseCountList:
    percentageFalseList.append(float(falseCount) / float(totalCount) * 100)

print "Each consistent percentage of VP", percentageFalseList

print "Average of the consistent percentage for 5VPs", average(percentageFalseList), "%"

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


plt.xlabel('vantage point')
plt.ylabel('percentage of consistency (%)')
plt.title('Percentage of consistency for 5 vantage points')
plt.xticks(indexs + bar_width/2, ('liege', 'temple', 'ucl', 'umass', 'wiilab'))
plt.xlim(-0.3, 4.7)
plt.ylim(95.5,96.5)
rect = plt.bar(indexs, percentageFalseList, bar_width, color='b')
autolabel(rect)
savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Percentage_consistency_5VP_copy.pdf")
plt.tight_layout()
plt.show()