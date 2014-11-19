__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt

mrList = np.linspace(1, 13, 13)
negativeList = [-1, -1, -10, -10, -1, -1, -1, -10 ,-1, -1, -1, -10, -10]
noMapReplyList = np.linspace(0, 0, 13)
rlocSet1 = [-10, 1, 1, 1, -10, -10, 1, 1, 1, -10, 1, 1, 1]
rlocSet2 = [-10, 2, 2, 2, 2, 2, 2, 2, 2, -10, 2, 2, 2]
rlocSet3 = [-10, -10, 3, 3, -10, -10, -10, 3, -10, -10, -10, 3, 3]

plt.xlim(0.5, 13.5)
plt.ylim(-1.5, 3.5)

plt.scatter(mrList,negativeList, color = 'pink')
plt.scatter(mrList,noMapReplyList, color = 'red')
plt.scatter(mrList,rlocSet1, color = 'blue')
plt.scatter(mrList,rlocSet2, color = 'green')
plt.scatter(mrList,rlocSet3, color = 'purple')

plt.xlabel("13 different Map Resolvers")
plt.ylabel("Responses from MRs")
plt.title("Responses from 13 MRs for EID-153.16.49.112 in liege(by MR)")

plt.annotate('Negative Reply',xy=(1,-1),xytext=(1,-0.8),arrowprops=dict(arrowstyle="->"))
plt.annotate('No Map Reply',xy=(1,0),xytext=(1,0.2),arrowprops=dict(arrowstyle="->"))
plt.annotate('RLOC-82.121.231.67',xy=(2,1),xytext=(2,1.2),arrowprops=dict(arrowstyle="->"))
plt.annotate('RLOC-192.168.1.66',xy=(2,2),xytext=(2,2.2),arrowprops=dict(arrowstyle="->"))
plt.annotate('RLOC-132.227.85.231',xy=(3,3),xytext=(3,3.2),arrowprops=dict(arrowstyle="->"))


plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_MR/Plot_variable_MR_copy2.pdf")
plt.show()

