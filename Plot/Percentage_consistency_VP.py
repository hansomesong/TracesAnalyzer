__author__ = 'yueli'
import os
import matplotlib.pyplot as plt
from config.config import *
import numpy as np

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        print "height:", height
        plt.text(rect.get_x()+rect.get_width()/2-0.45, 1.0003*height, '%s' % round(height,2))

if __name__ == "__main__":

    try:
       LOG_DIR = os.environ['PROJECT_LOG_DIR']
    except KeyError:
        print "Environment variable PROJECT_LOG_DIR is not properly defined or " \
              "the definition about this variable is not taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"

    TARGET_FILE_NAME = 'comparison_among_vantage_point.csv'

    # Define a dict whose key-value is map_resolver_ip-number of occurrence, to store the final statistical result
    # It finally may be in format as following:
    # mp_nb_dict = {
    #   '1.1.1.1'   : 3,
    #   '2.2.2.2'   : 4,
    #   ...
    # }
    mp_nb_dict = {}
    with open(os.path.join(LOG_DIR, TARGET_FILE_NAME)) as f_handler:
        next(f_handler)
        for line in f_handler:
            tmp_list = line.split(";")[0].replace("('", "").replace("')", "").replace("'", '').replace(" ", "")\
                .split(",")
            mp_resovler =  tmp_list[-1]
            # mp_nb_dict[tmp_list[-1]] = mp_nb_dict.get(tmp_list[-1], default=0) + 1
            if mp_resovler not in mp_nb_dict:
                mp_nb_dict[mp_resovler] = 1
            else:
                mp_nb_dict[mp_resovler] += 1


    # Plot part begins here:
    X_axis = np.arange(13)
    Y_axis = [(613-float(value))/613*100 for value in mp_nb_dict.values()]
    bar_width = 0.5

    print "Overall average of consistency by the variable of VP:", np.average(Y_axis)

    rect = plt.bar(X_axis, Y_axis, bar_width, color='b')
    autolabel(rect)

    plt.xlabel('Map Resolver',fontsize=16)
    plt.ylabel('percentage of consistent mappings (%)', fontsize=16)
    plt.title('Percentage of consistency for 13 MRs', fontsize=18)
    plt.xticks(X_axis + bar_width/2, X_axis + 1, fontsize=16)
    plt.xlim(-0.4, 12.8)
    plt.ylim(80, 100)
    plt.grid(True)

    plt.savefig(os.path.join(PLOT_DIR, 'Percentage_consistency_13MR_VP.eps'),
                dpi=300, transparent=True)
    plt.show()