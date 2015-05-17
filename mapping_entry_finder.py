__author__ = 'yueli'
# -*- coding: utf-8 -*-

from config.config import *
import logging
# 借助第三方 package: netaddr来实现 IP subnetwork的排序
from netaddr import *
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # 读取环境变量 ‘PROJECT_LOG_DIR’ (此变量定义在工作目录下.profile或者.bashprofile)
    try:
        LOG_DIR = os.environ['PROJECT_LOG_DIR']
    except KeyError:
        print "Environment variable PROJECT_LOG_DIR is not properly defined or " \
              "the definition about this variable is not taken into account."
        print "If PROJECT_LOG_DIR is well defined, restart Pycharm to try again!"


    # 定义字典，存储需要读入的文件
    # 注意：所以本脚本的执行依赖于读入文件(comparison_time_liege.csv,etc.)的格式
    # 如果有朝一日，csv文件格式改变，本脚本也许需要做些修改
    input_logs = {
        'liege': os.path.join(LOG_DIR, 'comparison_time_liege.csv'),
        'temple': os.path.join(LOG_DIR, 'comparison_time_temple.csv'),
        'ucl': os.path.join(LOG_DIR, 'comparison_time_ucl.csv'),
        'umass': os.path.join(LOG_DIR, 'comparison_time_umass.csv'),
        'wiilab': os.path.join(LOG_DIR, 'comparison_time_wiilab.csv')
    }


    # 利用Python logging模块，记录脚本运行信息，有利于debug...
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), '{0}.log'.format(__file__)),
        level=logging.INFO,
        filemode='w',
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.debug(input_logs)


    result_dict = {}

    for vantage_name, log_file in input_logs.iteritems():
        result_dict[vantage_name] = {'neg_no': [], 'neg_nor': []}
        with open(log_file) as f_handler:
            next(f_handler)
            for line in f_handler:
                tmp_list = line.split(';')
                target_type_list = [
                    x for x in tmp_list[LOG_TIME_COLUMN['round_type_set']].split(',') if x != 'RoundNoReply'
                ]
                logging.debug(target_type_list)
                if 'NegativeReply' in target_type_list and 'RoundNormal' not in target_type_list:
                    result_dict[vantage_name]['neg_no'].extend(tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(','))
                if 'NegativeReply' in target_type_list and 'RoundNormal' in target_type_list:
                    result_dict[vantage_name]['neg_nor'].extend(tmp_list[LOG_TIME_COLUMN['mapping_entry']].split(','))
        # 对IP地址进行去重处理
        result_dict[vantage_name]['neg_no'] = list(set(result_dict[vantage_name]['neg_no']))
        print result_dict[vantage_name]['neg_no']
        # 将字符串转化为 IPNetwork对象，以便排序。。。
        result_dict[vantage_name]['neg_no'] = sorted([IPNetwork(x) for x in result_dict[vantage_name]['neg_no']])
        # IP地址转换回 字符串类型
        # result_dict[vantage_name]['neg_no'] = [str(x).format() for x in result_dict[vantage_name]['neg_no']]


        # 对IP地址进行去重处理
        result_dict[vantage_name]['neg_nor'] = list(set(result_dict[vantage_name]['neg_nor']))
        # 将字符串转化为 IPNetwork对象，以便排序。。。
        result_dict[vantage_name]['neg_nor'] = sorted([IPNetwork(x) for x in result_dict[vantage_name]['neg_nor']])
        # IP地址转换回 字符串类型


    logger.info('Case: Neg + No')
    for vantage_name, ip_address in result_dict.iteritems():
        logger.info("{0:8}: {1}".format(vantage_name, ['{0:20}'.format(str(x)) for x in ip_address['neg_no']]))
        logger.info("{0:8}: {1}".format(vantage_name, ['{0:20}'.format(str(x)) for x in cidr_merge(ip_address['neg_no'])]))

    logger.info('Case: Neg + Normal')
    for vantage_name, ip_address in result_dict.iteritems():
        logger.info("{0:8}: {1}".format(vantage_name, ['{0:20}'.format(str(x)) for x in ip_address['neg_nor']]))
        logger.info("{0:8}: {1}".format(vantage_name, ['{0:20}'.format(str(x)) for x in cidr_merge(ip_address['neg_nor'])]))


    # G = nx.Graph()
    #
    # G.add_node(1)
    #
    # G.add_nodes_from(result_dict['liege']['neg_nor'])



    G=nx.Graph()
    G.add_nodes_from(result_dict['liege']['neg_no'])

    pos=nx.spring_layout(G) # positions for all nodes

    nx.draw(G, pos)

    plt.show() # display










