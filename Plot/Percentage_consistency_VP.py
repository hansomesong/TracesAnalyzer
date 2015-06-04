__author__ = 'qsong'
import os

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

    print mp_nb_dict.values()
