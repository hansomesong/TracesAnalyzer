__author__ = 'yueli'
from pylab import *

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

xlim(0.5, 5.5)
X = [1, 2, 3, 4, 5]
plt.scatter(X,percentageFalseList)
plt.grid(True)

plt.annotate('liege 95.997%',xy=(1,95.995),xytext=(0.7, 95.97),arrowprops=dict(arrowstyle="->"))
plt.annotate('temple 95.972%',xy=(2,95.97),xytext=(2.25, 95.955),arrowprops=dict(arrowstyle="->"))
plt.annotate('ucl 96.198%',xy=(3,96.197),xytext=(2.7, 96.172),arrowprops=dict(arrowstyle="->"))
plt.annotate('umass 96.173%',xy=(4,96.173),xytext=(3.7, 96.15),arrowprops=dict(arrowstyle="->"))
plt.annotate('wiilab 96.210%',xy=(5,96.21),xytext=(4.58, 96.185),arrowprops=dict(arrowstyle="->"))

xlabel("vantage point")
ylabel("percentage of consistency (%)")
plt.title("Percentage of consistency for 5 Vantage Point")
savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Percentage_consistency_5VP_copy.pdf")
plt.show()