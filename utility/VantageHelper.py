from config.config import *
from utility.REPattern_opt import *
from utility.RoundInstanceFactory import *
from csv_sorter import *


def get_eid_resolver_sort_list(vantage_name):
    import os
    import socket
    logDirRoot = traces_log[vantage_name]
    logFilePathList = os.listdir(logDirRoot)
    target = "".join(logFilePathList)
    res = EID_RESOVLER_P.findall(target)
    eid_set = set()
    resolver_set = set()
    for element in res:
        eid_set = eid_set | set([element[0]])
        resolver_set = resolver_set |set([element[1]])
    resolvers = sorted(list(resolver_set), key=lambda item: socket.inet_aton(item))
    eids = sorted(list(eid_set), key=lambda item: socket.inet_aton(item))
    return eids, resolvers




# Test part============================
for vantage_name, value in traces_log.items():
    # Iterate all statistics CSV file for each vantage and retrieve all csv rows into a separate list
    # named 'csv_all'
    eids, resolvers = get_eid_resolver_sort_list(vantage_name)
    csv_file = CSV_FILE_DESTDIR+'statistic_{0}.csv'.format(vantage_name)
    csv_header = csv_sort_list(csv_file)[0]
    csv_body = csv_sort_list(csv_file)[1]

    # Define a set to store RLOC addre
    locator_addr_set = set()
    for eid in eids:
        # For each eid, define a set to store all possible locator addr set
        locator_addr_consistence = False
        eid_locator_addr_set = set(get_locator_list_by_eid_resolver(csv_body, eid, resolvers[0]))
        init_set_length = len(eid_locator_addr_set)
        for resolver in resolvers:
            eid_locator_addr_set = eid_locator_addr_set | set(get_locator_list_by_eid_resolver(csv_body, eid, resolver))
        if init_set_length == len(eid_locator_addr_set):
            locator_addr_consistence = True
        print eid,'------->',locator_addr_consistence



    # Still need to sort csv_all
    csv_all = sorted(csv_all, key=lambda item: socket.inet_aton(item[2])+socket.inet_aton(item[3]))
write_csv(CSV_ALL_FILE, [csv_header, csv_all])









# This is a on liner to sort ip list
# A good tutorial about lambda in python : http://pythonconquerstheuniverse.wordpress.com/2011/08/29/lambda_tutorial/
# Inspired from this link, I managed to sort a IP address list :
# http://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090
# The following link is about usage of sorted() function : https://wiki.python.org/moin/HowTo/Sorting






# For a given EID, if having map-reply, 13 different resolvers return the same suite RLOC for the given EID???
# with open("trial-reduced.csv", 'wb') as csvfile:
#     spamwriter = csv.writer(csvfile, dialect='excel',delimiter=';')
#     for eid in eids:
#         spamwriter.writerow([])
#         for resolver in resovlers:
#             logfilepath = "{0}/planetlab1-EID-{1}-MR-{2}.log".format(logDirRoot, eid, resolver)
#             R = RoundInstanceFactory(logfilepath)
#             if len(R.getLocatorAddrSet()):
#                 csv_row = [eid, resolver, R.getLocatorAddrSet()]
#                 spamwriter.writerow(csv_row)







