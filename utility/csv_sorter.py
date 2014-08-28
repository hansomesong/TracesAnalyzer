import csv
import socket

import sys
sys.path.append('../')
from config.config import *

#def csv2list(csv_file,delimiter=';'):

def csv_sort_list(csv_file, delimiter=';'):
    '''Read target csv file into a list and return a sorted list to be written'''
    with open(csv_file, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)

        # Do not forget to convert "reader" into list type, sorted works uniquely for list type.
        csv_cont_list = list(reader)

        # Respectively store csv file's header and content into a separate list
        csv_header = csv_cont_list[0]
        csv_body = csv_cont_list[1:]

        # Firstly, sort all csv rows according to (EID, resolver) pair. Here we rely on python lambda technique
        # and socket module's inet_aton function. Ask for google for more information
        csv_body = sorted(csv_body, key=lambda item: socket.inet_aton(item[2])+socket.inet_aton(item[3]))
        return [csv_header, csv_body]

def write_csv(dest_csv, csv_cont):
    """ Writes a semicolon-delimited CSV file."""
    with open(dest_csv, 'wb') as out_file:
        writer = csv.writer(out_file, delimiter=';')
        writer.writerow(csv_cont[0])
        for row in csv_cont[1]:
            writer.writerow(row)


def get_locator_list_by_vantage_eid_resolver(csv_body_list, vantage, eid, resolver):
    for csv_row in csv_body_list:
        # csv_row is a list whose content is like:
        # ['temple','/home/cloud/Documents/PlanetLab/temple/mappings/planetlab2-EID-37.76.0.0-MR-198.6.255.37.log',
        # '37.76.0.0,'198.6.255.37','False',	"['NegativeReply']" ]
        if eid in csv_row and resolver in csv_row and vantage in csv_row:
            # Currently, RLOC set is beginning at index 6 in csv_row list
            # Attention ; if the csv row format changes in the future, do not forget to modify the following instruction
            # Finally, return a locator address list
            return csv_row[6:]



# Test part========================
# target = '/home/cloud/Documents/Codes/TracesAnalyzer/log/statistic_ucl.csv'
# target_ed = target+".sort.csv"
# write_csv(target_ed, csv_sort_list(target))

csv_dst_dir = '/home/cloud/Documents/Codes/TracesAnalyzer/log/'
# csv_all_file = '/home/cloud/Documents/Codes/TracesAnalyzer/log/statistic_all.csv'
#
# csv_all = []
#
# for vantage, value in traces_log.items():
#      csv_file = csv_dst_dir+'statistic_{0}.csv'.format(vantage)
#      csv_all.extend(csv_sort_list(csv_file)[1])
#
#
#
#      # Initially, the generated csv file, such as 'statistic_liege.csv' is unsorted.
#      # Thus, we call methods defined in python script : utility/csv_sorter.py to sort initial
#      # unsorted csv then overwrite the latter.
#
# # Still need to sort csv_all
#
# csv_all = sorted(csv_all, key=lambda item: socket.inet_aton(item[2])+socket.inet_aton(item[3]))
# write_csv(csv_all_file, [['sss'], csv_all])



# Test method get_locator_list_by_eid_resolver


csv_file = csv_dst_dir+'statistic_all.csv'

csv_body = csv_sort_list(csv_file)[1]

eid = '0.0.0.0'
resolver = '149.20.48.61'


print
print get_locator_list_by_vantage_eid_resolver(csv_body,'liege', eid, resolver)

eid_locator_addr_set = set(get_locator_list_by_vantage_eid_resolver(csv_body, 'liege', eid, resolver))
print eid_locator_addr_set




