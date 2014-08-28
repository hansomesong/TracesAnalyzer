from Round import *
from Locator import *


type_4 = """Date=2013/07/02 09:00:32\nEID=153.16.1.0\nResolver=149.20.48.61\n\nUsing source address (ITR-RLOC) 139.165.12.211\n
Send map-request to 149.20.48.61 (149.20.48.61) for 153.16.1.0 (153.16.1.0) ...\n
RECEIVED_FROM=129.250.26.242\nRTT=0.16500\nLOCATOR_COUNT=2\nMAPPING_ENTRY=153.16.1.0/24\n
TTL=1440\nAUTH=1\nMOBILE=0\nLOCATOR0=129.250.1.255\nLOCATOR0_STATE=up\nLOCATOR0_PRIORITY=254\nLOCATOR0_WEIGHT=0\n
LOCATOR1=129.250.26.242\nLOCATOR1_STATE=up\nLOCATOR1_PRIORITY=1\nLOCATOR1_WEIGHT=100\n""".replace("\n",'')


# Test Part ===========================================
# type_1 = '2013/07/09 17:00:46
# EID=85.192.0.0
# Resolver=195.50.116.18
# Using source address (ITR-RLOC) 139.165.12.211
# Send map-request to 195.50.116.18 (195.50.116.18) for 85.192.0.0 (85.192.0.0) ...
# RECEIVED_FROM=195.50.116.18
# RTT=0.24900
# LOCATOR_COUNT=0
# MAPPING_ENTRY=2610:d0:1204::/48
# TTL=1
# AUTH=0
# MOBILE=0
# RESULT="Negative cache entry"
# ACTION=forward-native'

date = '2013/07/09 17:00:46'
EID = '85.192.0.0'
resolver = '195.50.116.18'
req_src = '139.165.12.211'
req_dst = '195.50.116.18'
req_for = '85.192.0.0'
rpy_src = '195.50.116.18'
RTT = '0.3120'
locator_count='0'
mapping_entry='2610:d0:1204::/48'
TTL='1'
auth='0'
mobile='0'
result="Negative cache entry"
action='forward-native'


print "Test Round:"
print Round(date, EID,resolver, req_src, req_dst, req_for).toList()
print "Test RoundNoReply"
print RoundNoReply(date, EID,resolver, req_src, req_dst, req_for).toList()
print "Test NegativeReply"
print NegativeReply(date, EID, resolver,req_src, req_dst, req_for,rpy_src, RTT, locator_count, mapping_entry,
                 TTL, auth, mobile, result, action).toList()
print NegativeReply(date, EID, resolver,req_src, req_dst, req_for,rpy_src, RTT, locator_count, mapping_entry,
                 TTL, auth, mobile, result, action).__dict__.keys()
print NegativeReply(date, EID, resolver,req_src, req_dst, req_for, rpy_src, RTT, locator_count, mapping_entry,
                 TTL, auth, mobile, result, action).__getattribute__('date')

print NegativeReply.__dict__

print "Test RoundNormal"

print NegativeReply(date, EID, resolver,req_src, req_dst, req_for,rpy_src, RTT, locator_count, mapping_entry,
                 TTL, auth, mobile, result, action).toList()
