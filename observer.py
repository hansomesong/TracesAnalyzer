__author__ = 'cloud'



import os
import socket
from config.config import *
from utility.REPattern_opt import *
from utility.RoundInstanceFactory import *

logDirRoot = traces_log['liege']

logFilePathList = os.listdir(logDirRoot)
target = "".join(logFilePathList)

res = EID_RESOVLER_P.findall(target)

eid_set = set()
resovler_set = set()

for element in res:
    eid_set = eid_set | set([element[0]])
    resovler_set = resovler_set |set([element[1]])


print len(logFilePathList)
print len(eid_set)
print len(resovler_set)




# This is a on liner to sort ip list
# A good tutorial about lambda in python : http://pythonconquerstheuniverse.wordpress.com/2011/08/29/lambda_tutorial/
# Inspired from this link, I managed to sort a IP address list :
# http://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090
# The following link is about usage of sorted() function : https://wiki.python.org/moin/HowTo/Sorting
resovlers = sorted(list(resovler_set), key=lambda item: socket.inet_aton(item))



eids = sorted(list(eid_set), key=lambda item: socket.inet_aton(item))





# For a given EID, if having map-reply, 13 different resolvers return the same suite RLOC for the given EID???
with open("trial-reduced.csv", 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel',delimiter=';')
    for eid in eids:
        spamwriter.writerow([])
        for resolver in resovlers:
            logfilepath = "{0}/planetlab1-EID-{1}-MR-{2}.log".format(logDirRoot, eid, resolver)
            R = RoundInstanceFactory(logfilepath)
            if len(R.getLocatorAddrSet()):
                csv_row = [eid, resolver, R.getLocatorAddrSet()]
                spamwriter.writerow(csv_row)







