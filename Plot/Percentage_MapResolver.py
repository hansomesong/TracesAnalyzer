__author__ = 'yueli'
from pylab import *

# Plot the percentage of False
# (which means that the responses from the different Map Resolvers for a dedicated EID during the whole measurements are different)
# for every vantage point: liege, temple, ucl, umass, wiilab
totalCount = 614
falseCountList = [9, 7, 9, 7, 8]
percentageFalseList = []

for falseCount in falseCountList:
    percentageFalseList.append(float(falseCount) / float(totalCount) * 100)

#print percentageFalseList

xlim(0.5, 5.5)
X = [1, 2, 3, 4, 5]
plt.scatter(X, percentageFalseList)
xlabel("vantage point")
ylabel("percentage of False (%)")
plt.title("Percentage of False according to the Map Resolver")
# savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Percentage of False according to the Map Resolver.png")
plt.show()