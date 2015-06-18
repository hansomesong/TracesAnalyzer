__author__ = 'yueli'


import numpy as np
import matplotlib.pyplot as plt


n_groups = 7

percentage_1st_day = (69, 1.82, 29.18, 98.53, 1.47, 85.61, 14.39)
percentage_means = (72.36, 20.41, 7.23, 98.34, 1.66, 89.06, 10.94)
percentage_18th_day = (81.3, 10.87, 7.83, 98.53, 1.47, 85.61, 14.39)

fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.25

plt.grid(True)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        print "height:", height
        plt.text(rect.get_x()+rect.get_width()/2-0.1, 1.001*height, '%s' % round(height,2))

opacity = 0.6
rects1 = plt.bar(index, percentage_1st_day, bar_width,alpha=opacity, color='b',label= 'First day')
rects2 = plt.bar(index + bar_width, percentage_means, bar_width,alpha=opacity,color='r',label='Means')
rects3 = plt.bar(index + 2*bar_width, percentage_18th_day, bar_width,alpha=opacity,color='y',label='Last day')

plt.xlabel('Classification', fontsize=16)
plt.ylabel('Percentage (%)', fontsize=16)
plt.title('Percentage of every classification', fontsize=18)
plt.xticks(index + bar_width, ('New Deployment', 'Reconfiguration', 'RLOC Madness',
                               'Neg+RLOC by MR', 'RLOC1+RLOC2 by MR', 'Neg+RLOC by VP', 'RLOC1+RLOC2 by VP'))
plt.ylim(0,101)
plt.legend()

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.show()