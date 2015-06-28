# -*- coding: utf-8 -*-
# 此script为给IP_Addressing_space_counter.py画执行结果
# 用其运行结果直接作为y轴的数值付给 prefix_number_1st prefix_number_18th ip_addr_number_1st 和 ip_addr_number_18th
author = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
 
n_groups = 5
x = [1, 2, 3, 4, 5]
prefix_number_1st = (17.3, 17.3, 17.3, 17.3, 17.3)
prefix_number_18th = (20.7, 20.8, 20.6, 20.7, 20.7)

ip_addr_number_1st = (40.57, 40.73, 40.73, 40.73, 40.73)
ip_addr_number_18th = (37.54, 37.74, 40.27, 37.70, 37.70)
 
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
 
# opacity = 0.4
rects3 = plt.bar(index, ip_addr_number_1st, bar_width, color='yellow',label='IP address number')
rects4 = plt.bar(index + bar_width, ip_addr_number_18th, bar_width, color='yellow')
rects1 = plt.bar(index, prefix_number_1st, bar_width, color='b',label='prefix number')
rects2 = plt.bar(index + bar_width, prefix_number_18th, bar_width, color='b')

# plt.plot(x, ip_addr_number_1st, color='green',label='ip_addr_number_1st')
# plt.plot(x, ip_addr_number_18th, color='yellow',label='ip_addr_number_18th')
# plt.plot(x, prefix_number_1st, color='b',label='prefix_number_1st')
# plt.plot(x, prefix_number_18th, color='r',label='prefix_number_18th')

plt.xlabel('vantage point', fontsize=18)
plt.ylabel('Number', fontsize=18)
plt.title('Prefix number and possible IP address number', fontsize=22)
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5'))
plt.yticks(np.arange(0,50,10), ('', '', '200', '', '4*10exp10', ''))
plt.ylim(0,50)
plt.legend()

plt.show()