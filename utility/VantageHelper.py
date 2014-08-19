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

    with open(CSV_FILE_DESTDIR+'{0}_RLOC.csv'.format(vantage_name),'wb') as cf:
        spamwriter = csv.writer(cf, dialect='excel', delimiter=';')
        spamwriter.writerow(['Vantage', 'EID', 'Locator Count Consistence'])
        # Define a set to store RLOC addre
        locator_addr_set = set()
        for eid in eids:
            # Initially, we consider locator_addr_consistence is True
            # Then iterate all 13 different resolvers to get respective locator address set
            # If one (eid, resolver) pair returns a different locator address set other than the one returned by
            # pair(eid, resolvers[0]), we change the flag 'locator_addr_consistence' into false ane break.
            locator_addr_consistence = True
            # For each eid, firstly choose the a comparison reference
            eid_locator_addr_set = set(get_locator_list_by_vantage_eid_resolver(csv_body, vantage_name, eid, resolvers[0]))
            for resolver in resolvers:
                if eid_locator_addr_set != set(get_locator_list_by_vantage_eid_resolver(csv_body, vantage_name, eid, resolver)):
                    locator_addr_consistence = False
                    break
            spamwriter.writerow([vantage_name, eid, locator_addr_consistence])



    # Still need to sort csv_all
    #csv_all = sorted(csv_all, key=lambda item: socket.inet_aton(item[2])+socket.inet_aton(item[3]))
#write_csv(CSV_ALL_FILE, [csv_header, csv_all])


# Test method : get_eid_resolver_sort_list(vantage_name)

# eids, resolvers = get_eid_resolver_sort_list('ucl')
#
# print 'ucl', eids
# print 'ucl', resolvers


# Analyze statistic_all.csv to verify that for the same (eid, resolver) pair, all 5 vantage points have seen the
# same result.
target_csv = CSV_FILE_DESTDIR+'statistic_all.csv'
eids, resolvers = get_eid_resolver_sort_list('liege')

csv_body = csv_sort_list(target_csv)[1]

with open(CSV_FILE_DESTDIR+'ALL_RLOC.csv','wb') as cf:
    spamwriter = csv.writer(cf, dialect='excel', delimiter=';')
    spamwriter.writerow(['EID', 'Resolver', 'Locator Count Consistence'])
    # Define a set to store RLOC addre
    locator_addr_set = set()
    for eid in eids:
        # Initially, we consider locator_addr_consistence is True
        # Then iterate all 13 different resolvers to get respective locator address set
        # If one (eid, resolver) pair returns a different locator address set other than the one returned by
        # pair(eid, resolvers[0]), we change the flag 'locator_addr_consistence' into false ane break.
        for resolver in resolvers:
            # choose liege vantage's as comparison reference.
            locator_addr_consistence = True
            #print eid, resolver
            eid_locator_addr_set = set(get_locator_list_by_vantage_eid_resolver(csv_body, 'liege', eid, resolver))
            for vantage_name in traces_log.keys():
                if eid_locator_addr_set != set(get_locator_list_by_vantage_eid_resolver(csv_body, vantage_name, eid, resolver)):
                    locator_addr_consistence = False
                    break
            spamwriter.writerow([eid, resolver, locator_addr_consistence])









