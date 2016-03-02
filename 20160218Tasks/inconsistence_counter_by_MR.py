# -*- coding: utf-8 -*-
__author__ = 'yueli'


from resolver_comparator import *

import numpy as np




if __name__ == "__main__":

    logging.basicConfig(filename=os.path.join(os.getcwd(), os.path.basename(__file__).split(".")[0]+'execution_log.txt'),
                        level=logging.DEBUG,
                        filemode='w',
                        format='%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)



    eid = "153.16.44.160"
    eids = union_incon_eids()

    result_list = []

    for vp in VP_LIST:
        print incon_ocur_counter(eid, vp, logger)

        # 读取环境变量PLANETLAB_CSV
        try:
            # debug的时候 使用 PLANETLAB_DEBUG
            # 工作的时候 用 PLANETLAB_CSV
            PROJECT_LOG_DIR = os.environ["PROJECT_LOG_DIR"]
            print PROJECT_LOG_DIR
            COM_MAP_RES_CSV = os.path.join(PROJECT_LOG_DIR, 'comparison_MR', "comparison_map_resolver_in_{0}.csv".format(vp))

        except KeyError:

            print "Environment variable PROJECT_LOG_DIR is not properly defined or the definition about this variable is not" \
                  "taken into account."
            print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"


        with open(COM_MAP_RES_CSV) as f_handler:
            f_handler.next()

            incon_num = [incon_ocur_counter(x, vp, logger) for x in eids]

            result_list.append(incon_num)
            # print incon_num
            #
            # l = Counter(incon_num).most_common()
            # print l
            # print sorted(l, key=lambda x:x[0])



    a = np.array(result_list)

    result = [float(x) for x in np.mean(a, axis=0)]
    print result

