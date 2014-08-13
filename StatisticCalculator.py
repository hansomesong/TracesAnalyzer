__author__ = 'cloud'
import numpy as np
import re
from scipy.stats import rv_continuous


import matplotlib.pyplot as plt


rv_data_file = '/home/cloud/Documents/RTTValues.txt'

with open(rv_data_file) as f:
    rv_list = filter(None,re.compile(r'\n').split(f.read()))
    # Inspired from the following post :
    # http://stackoverflow.com/questions/3877209/how-to-convert-an-array-of-strings-to-an-array-of-floats-in-numpy
    rv_array = np.array(map(float, rv_list))

# for i in range(100):
#     print rv_array[i]

# Inspired by the following link to write the child class:
# http://stackoverflow.com/questions/17676710/create-a-continuous-distribution-in-python

# useful link : http://zhidao.baidu.com/question/567845757.html
class rvc(rv_continuous):
    pass

# Maybe this small program is very useful :http://zhidao.baidu.com/question/1829877996411545700.html
#rtt_cdf = rv_continuous().cdf(rv_array)


# sorted = np.sort(rv_array)
# yvals = np.arange(len(sorted))/float(len(sorted))
# #
# #
# print float(len(sorted))
# plt.plot(sorted, yvals)
# plt.show(1)
# #
# # plt.show(2)
# print float(sorted.max())


## Filename: ecdf.py

import numpy as np
import matplotlib.pyplot as plt

class ECDF:

    def __init__(self, observations):
        self.observations = observations

    def __call__(self, x):
        counter = 0.0
        for obs in self.observations:
            if obs <= x:
                counter += 1
        return counter / len(self.observations)

    def plot(self, a=None, b=None):
        if a == None:
            # Set up some reasonable default
            a = self.observations.min() - self.observations.std()
        if b == None:
            # Set up some reasonable default
            b = self.observations.max() + self.observations.std()
        X = np.linspace(a, b, 100)
        f = np.vectorize(self.__call__)
        plt.plot(X, f(X))
        plt.show()


ECDF(rv_array).plot()
