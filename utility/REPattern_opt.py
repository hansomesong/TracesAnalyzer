# This file contains uniquely all used regular expression pattern
# Compared with REPattern.py, this script bring some improvement to accelerate the execution of RE
import re

# delimiter is a string representing the pattern delimiting all round records in a log file.
# A delimiter in a log file could be, for example, "--- Round ID 1372750223 ----------------------------------->"
delimiter = "[-+_*]+\s*Round\s*ID\s*\d+\s*[-+*_]*>"


# To get a better performance, we choose to place all RE pattern in a separate python script
# and compile it once time into a pattern object by calling re.compile() method.
DELIMITER_P = re.compile(r'{0}'.format(delimiter))


def infoFieldExtractor(target_string, pattern):
    '''This method takes a target string and a compile pattern object as input arguments, to extract substring who
        matches the given pattern, return the mentioned substring in a list.
     '''
    return pattern.findall(target_string)


#=======================================================================================================================
# The first Round format possibly appeared in a log file
    # --- Round ID 1372750223 ----------------------------------->
    # Date=2013/07/02 07:30:23
    # EID=0.0.0.0
    # Resolver=173.36.254.164
    # Using source address (ITR-RLOC) 139.165.12.211
    # Send map-request to 173.36.254.164 (173.36.254.164) for 0.0.0.0 (0.0.0.0) ...
    # Send map-request to 173.36.254.164 (173.36.254.164) for 0.0.0.0 (0.0.0.0) ...
    # Send map-request to 173.36.254.164 (173.36.254.164) for 0.0.0.0 (0.0.0.0) ...
    # *** No map-reply received ***
TYPE_1_P = re.compile(r"""
    Date\s*=\s*(\d{2,4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}[:-]\d{1,2}[:-]\d{1,2})  # To extract date information
    EID=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) #To extract EID address. Attention!! it supports only IPV4 address
    Resolver=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) # To extract Resolver address
    Using\s+source\s+address\s+\(ITR-RLOC\)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    #Attention : For string such as Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
    #we use .+ at the end to match "(0.0.0.0) ..."
    Send\s+map-request\s+to\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+for\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+
""", re.I | re.VERBOSE)


# The second Round format:
    #--- Round ID 1372750223 ----------------------------------->
    #Date=2013/07/02 07:30:23
    #EID=0.0.0.0
    #Resolver=149.20.48.61
    #Using source address (ITR-RLOC) 139.165.12.211
    #Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
    #RECEIVED_FROM=149.20.48.61
    #RTT=0.15700
    #LOCATOR_COUNT=0
    #MAPPING_ENTRY=0.0.0.0/3
    #TTL=9
    #AUTH=0
    #MOBILE=0
    #RESULT="Negative cache entry"
    #ACTION=forward-native
TYPE_2_P = re.compile(r"""
    Date\s*=\s*(\d{2,4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}[:-]\d{1,2}[:-]\d{1,2})  # To extract date information
    EID=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    Resolver=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    Using\s+source\s+address\s+\(ITR-RLOC\)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    #Attention : For string such as Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
    #we use .+ at the end to match "(0.0.0.0) ..."
    Send\s+map-request\s+to\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+for\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+
    RECEIVED_FROM\s*=\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    RTT\s*=\s*(\d+\.\d+)
    LOCATOR_COUNT\s*=\s*(\d+)
    MAPPING_ENTRY\s*=\s*(.+)
    TTL\s*=\s*(\d+)
    AUTH\s*=\s*(\d+)
    MOBILE\s*=\s*(\d+) #MOBILE=0
    RESULT\s*=\s*(.+)
    ACTION\s*=\s*(.+)$
""", re.I | re.VERBOSE)


TYPE_3_P = re.compile(r"""
    Date\s*=\s*(\d{2,4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}[:-]\d{1,2}[:-]\d{1,2})  # To extract date information
    EID=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    Resolver=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    Using\s+source\s+address\s+\(ITR-RLOC\)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    #attention : For string such as Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
    #we use .+ at the end to match "(0.0.0.0) ..."
    Send\s+map-request\s+to\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+for\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+
    RECEIVED_FROM\s*=\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    RTT\s*=\s*(\d+\.\d+)
    LOCATOR_COUNT\s*=\s*(\d+)
    MAPPING_ENTRY\s*=\s*(.+)
    TTL\s*=\s*(\d+)
    AUTH\s*=\s*(\d+)
    MOBILE\s*=\s*(\d+) #MOBILE=0
""", re.I | re.VERBOSE)


# There is no RE for the forth this round type :
    # --- Round ID 1372755632 ----------------------------------->
    # Date=2013/07/02 09:00:32
    # EID=153.16.1.0
    # Resolver=149.20.48.61
    #
    # Using source address (ITR-RLOC) 139.165.12.211
    # Send map-request to 149.20.48.61 (149.20.48.61) for 153.16.1.0 (153.16.1.0) ...
    # RECEIVED_FROM=129.250.26.242
    # RTT=0.16500
    # LOCATOR_COUNT=2
    # MAPPING_ENTRY=153.16.1.0/24
    # TTL=1440
    # AUTH=1
    # MOBILE=0
    # LOCATOR0=129.250.1.255
    # LOCATOR0_STATE=up
    # LOCATOR0_PRIORITY=254
    # LOCATOR0_WEIGHT=0
    # LOCATOR1=129.250.26.242
    # LOCATOR1_STATE=up
    # LOCATOR1_PRIORITY=1
    # LOCATOR1_WEIGHT=100
#However, we could user TYPE_3_P and the following LOCATORS_P to treat this kind of round record
#Attention : Locator address could be in formant IPV6, such as 'LOCATOR2=2001:9e0:8500:b00::1' for example in file :
#/home/cloud/Documents/PlanetLab/liege/mappings/planetlab1-EID-37.77.56.32-MR-149.20.48.61.log
LOCATORS_P = re.compile(r"""
    LOCATOR[-_:]*(\d+)\s*=\s*([a-f0-9:.]+)
    \s*LOCATOR[-_:]*\d+_STATE\s*=\s*(\w+)
    LOCATOR[-_:]*\d+_PRIORITY\s*=\s*(\d+)
    LOCATOR[-_:]*\d+_WEIGHT\s*=\s*(\d+)
""", re.I | re.VERBOSE)





#======================The following strings are just the target our defined RE process
type_1 = 'Date=2013/07/09 17:00:46EID=85.192.0.0Resolver=195.50.116.18Using source address (ITR-RLOC) 139.165.12.211Send map-request to 195.50.116.18 (195.50.116.18) for 85.192.0.0 (85.192.0.0) ...RECEIVED_FROM=195.50.116.18RTT=0.24900LOCATOR_COUNT=0MAPPING_ENTRY=2610:d0:1204::/48TTL=1AUTH=0MOBILE=0RESULT="Negative cache entry"ACTION=forward-native'
type_2 = 'Date=2013/07/02 07:30:23EID=0.0.0.0Resolver=149.20.48.61Using source address (ITR-RLOC) 139.165.12.211Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...RECEIVED_FROM=149.20.48.61RTT=0.15700LOCATOR_COUNT=0MAPPING_ENTRY=0.0.0.0/3TTL=9AUTH=0MOBILE=0RESULT="Negative cache entry"ACTION=forward-native'
type_3 = 'Date=2013/07/02 09:30:16EID=153.16.3.0Resolver=149.20.48.61Using source address (ITR-RLOC) 139.165.12.211Send map-request to 149.20.48.61 (149.20.48.61) for 153.16.3.0 (153.16.3.0) ...RECEIVED_FROM=128.122.208.144RTT=0.16800LOCATOR_COUNT=2MAPPING_ENTRY=153.16.3.0/24TTL=1440AUTH=1MOBILE=0!!!! LCAF AFI print skipped !!!!'

type_4 = """Date=2013/07/02 09:00:32\nEID=153.16.1.0\nResolver=149.20.48.61\n\nUsing source address (ITR-RLOC) 139.165.12.211\n
Send map-request to 149.20.48.61 (149.20.48.61) for 153.16.1.0 (153.16.1.0) ...\n
RECEIVED_FROM=129.250.26.242\nRTT=0.16500\nLOCATOR_COUNT=2\nMAPPING_ENTRY=153.16.1.0/24\n
TTL=1440\nAUTH=1\nMOBILE=0\nLOCATOR0=129.250.1.255\nLOCATOR0_STATE=up\nLOCATOR0_PRIORITY=254\nLOCATOR0_WEIGHT=0\n
LOCATOR1=129.250.26.242\nLOCATOR1_STATE=up\nLOCATOR1_PRIORITY=1\nLOCATOR1_WEIGHT=100\n""".replace("\n",'')
# print TYPE_1_P.findall(type_1)[0]
# #
# #
# print TYPE_2_P.findall(type_2)[0]
# # #print TYPE_3_P.findall(type_3)[0]
# # print LOCATORS_P.findall(type_4)[0]



# RE to extract EID and Resolver address in log file

name1 = 'onelab1-EID-205.203.0.0-MR-149.20.48.77.log'
name2 ='planetlab1-EID-205.203.0.0-MR-149.20.48.77.logplanetlab1-EID-153.16.23.48-MR-149.20.48.77.logplanetlab1-EID-153.16.21.0-MR-202.51.247.10.log'

EID_RESOVLER_P = re.compile(r'\w+lab\d+-EID-(\d+\.\d+\.\d+\.\d+)-MR-(\d+\.\d+\.\d+\.\d+)\.log', re.VERBOSE)


# res = EID_RESOVLER_P.findall(name1)
# print res
#
# res = EID_RESOVLER_P.findall(name2)
# print res