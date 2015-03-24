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

plt.scatter(mrList,negativeList, color = 'blue')
plt.scatter(mrList,noMapReplyList, color = 'yellow')
plt.scatter(mrList,rlocSet1, color = 'purple')
plt.scatter(mrList,rlocSet2, color = 'red')
plt.scatter(mrList,rlocSet3, color = 'green')

plt.xlabel("13 different Map Resolvers")
plt.ylabel("Responses from MRs")
plt.title("Responses from 13 MRs for EID-153.16.49.112 at liege(by MR)")
plt.xticks(mrList, ['MR1', 'MR2', 'MR3', 'MR4', 'MR5', 'MR6', 'MR7', 'MR8', 'MR9', 'MR10', 'MR11', 'MR12', 'MR13', 'MR14', 'MR15'])
plt.yticks([-1, 0, 1, 2, 3], ['Negative Reply', 'No Map Reply', '82.121.231.67', '192.168.1.66', '132.227.85.231'])


# plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot_new/Plot_variable_MR/Plot_variable_MR.pdf")
plt.show()

