# -*- coding: utf-8 -*-
__author__ = 'yueli'


from vantage_comparator import *

import pprint

if __name__ == "__main__":

    logging.basicConfig(filename=os.path.join(os.getcwd(), os.path.basename(__file__).split(".")[0]+'execution_log.txt'),
                        level=logging.WARN,
                        filemode='w',
                        format='%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)


    # 读取环境变量PROJECT_LOG_DIR
    try:
        PROJECT_LOG_DIR = os.environ['PROJECT_LOG_DIR']
        COM_VP_CSV = os.path.join(PROJECT_LOG_DIR, 'comparison_VP', "comparison_among_vantage_point.csv")
        logger.debug("The departure file is :{0}".format(COM_VP_CSV))
    except KeyError:

        print "Environment variable PROJECT_LOG_DIR is not properly defined or the definition about this variable is not" \
              "taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"

    with open(COM_VP_CSV) as f_handler:
        f_handler.next()
        # eid_mr_p is a list holding the EID-Resolver pairs, namely the first column in departure file
        eid_mr_p = [line.split(";")[0] for line in f_handler]
        # since now EID-Resolver pari is still in format of string, such as "('153.16.3.0', '202.214.86.252')"
        # need to do string strim
        eid_mr_p = [x.split("'") for x in eid_mr_p]
        # now each element (of type list) in eid_mr_p is in format such as ["(", "153.16.3.0", "', '", "202.214.86.252", ")"]
        # we just need the element of index 1 and 3 of each element list
        eid_mr_p = [[x[1], x[3]] for x in eid_mr_p]
        # Now eid_mr_p has a format such as:
        # eid_mr_p = [
        #     ['153.16.3.0', '202.214.86.252']
        #     ['37.77.57.64', '217.8.98.42']
        #     ['153.16.22.216', '198.6.255.37']
        #     ['153.16.47.208', '198.6.255.40']
        #     ['153.16.32.0', '173.36.254.164']
        #     ['153.16.18.0', '206.223.132.89']
        #     ['153.16.38.0', '198.6.255.40']
        #     ['153.16.48.96', '202.214.86.252']
        #     ['153.16.17.64', '149.20.48.61']
        #     ['153.16.49.192', '217.8.97.6']
        #     ['153.16.17.224', '202.51.247.10']
        #     ['153.16.32.0', '195.50.116.18']
        #     ['153.16.13.208', '206.223.132.89']
        #     ['153.16.66.64', '206.223.132.89']
        #     ['153.16.44.120', '195.50.116.18']
        #  ]
        # We need to convert eid_mr_p to a dictionary with EID as key and the list of MRs with corresponding value.
        eid_mr_p_d = {}
        for element in eid_mr_p:
            curr_eid = element[0]
            if curr_eid not in eid_mr_p_d.keys():
                eid_mr_p_d[curr_eid] = []
                eid_mr_p_d[curr_eid].append(element[1])
            else:
                eid_mr_p_d[curr_eid].append(element[1])

        # Now eid_mr_p_d has format such as:
        # eid_mr_p_d = {
        #   '153.16.0.0': ['195.50.116.18', '217.8.98.42', '193.162.145.50'],
        #   '153.16.1.0': ['217.8.97.6'],
        #   '153.16.13.0': ['149.20.48.77', '217.8.97.6', '202.214.86.252', '198.6.255.40', '149.20.48.61'
        #                  '198.6.255.37',
        #                  '195.50.116.18'],
        #   '153.16.13.144': ['195.50.116.18', '198.6.255.40', '193.162.145.50', '217.8.97.6', '149.20.48.77'],
        # }


        result = []
        for eid, mp_list in eid_mr_p_d.iteritems():
            tmp = [incon_ocur_counter_inter_vp(eid, mp, logger) for mp in mp_list]
            print eid, mp_list, tmp
            result.append(sum(tmp)/len(MR_LIST))

        print result











