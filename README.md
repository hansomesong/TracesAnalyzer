==============>Introduction

This is a small project in python aiming to process and analyze a bunch of given LISP experimental trace log files.

The 'mp_parser.py' script is the entrance of the whole program, it uses multiple-processing technique to process and
analyze given LISP experimental results(in form of a serial of trace log files), finally output analysis results into
some CSV files situated in the log directory.

===============>Glossary

Vantage: shorthand for LISP experiment vantage point, where people execute queries for 613 different EID and each query
is simultaneously sent to 13 different resolvers. In the context of this program, vantage is simply refereed to as a directory
containing 7696(613*13) logfiles. Currently,this program works only for 5 vantages, respectively : liege, temple, ucl, umass, wiilab.

Logfile: A log file saving all LISP experiment rounds, every 30 minutes, during a dozen days. its name respect the format:
planetlab1-EID-153.16.14.0-MR-193.162.145.50.log.

Round: A session between a certain machine and a resolver to query RLOC-related information for a given EID address.
The following is a example of round:
                
                --- Round ID 1372750223 ----------------------------------->
                Date=2013/07/02 07:30:23
                EID=153.16.32.224
                Resolver=198.6.255.37
                Using source address (ITR-RLOC) 139.165.12.211
                Send map-request to 198.6.255.37 (198.6.255.37) for 153.16.32.224 (153.16.32.224) ...
                RECEIVED_FROM=192.162.230.11
                RTT=0.12000
                LOCATOR_COUNT=4
                MAPPING_ENTRY=153.16.32.224/28
                TTL=1440
                AUTH=1
                MOBILE=0
                LOCATOR0=192.162.230.11
                LOCATOR0_STATE=up
                LOCATOR0_PRIORITY=2
                LOCATOR0_WEIGHT=50
                LOCATOR1=192.162.230.12
                LOCATOR1_STATE=up
                LOCATOR1_PRIORITY=2
                LOCATOR1_WEIGHT=50
                LOCATOR2=192.162.230.13
                LOCATOR2_STATE=up
                LOCATOR2_PRIORITY=1
                LOCATOR2_WEIGHT=100
                LOCATOR3=192.162.230.14
                LOCATOR3_STATE=up
                LOCATOR3_PRIORITY=1
                LOCATOR3_WEIGHT=100

Normally, A round contains the following attributes:

                            date                : the datetime when this session is executed.
                            EID                 :
                            Resolver            :
                            request src         :
                            request dst         : namely the value of Resolver
                            request for         : namely the value of EID
                            reply src           : the address who gives RLOC-related information for a query for EID. It could be different with the Resolver address.
                            RTT                 : Round Trip Time, the delay between the send of a query and the reception of its reply
                            Locator_count       : The length of RLOC Set. It could be simply interpreted that the reply for a EID query contains Locator_count different locator addresses.
                            Mapping_entry       :  ??
                            TTL                 : Time to live
                            Auth                :???
                            Mobile              :???
                            locator             : refer to item for locator.

Round Type : There exists multiple round types according to the content of round's reply:

            RoundNoReply :
            caused by network connection, a round has no reply for EID, for example :
            
                            --- Round ID 1373014821 ----------------------------------->
                            Date=2013/07/05 09:00:21
                            EID=0.0.0.0
                            Resolver=149.20.48.61
                            Using source address (ITR-RLOC) 139.165.12.211
                            Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
                            Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
                            Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
                             No map-reply received 


            RoundResultAction: 
            A round has a reply, but this reply does not include RLOC-related information, for example:
            
                            --- Round ID 1373013038 ----------------------------------->
                            Date=2013/07/05 08:30:38
                            EID=0.0.0.0
                            Resolver=149.20.48.61
                            Using source address (ITR-RLOC) 139.165.12.211
                            Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
                            RECEIVED_FROM=149.20.48.61
                            RTT=0.15000
                            LOCATOR_COUNT=0
                            MAPPING_ENTRY=0.0.0.0/3
                            TTL=15
                            AUTH=0
                            MOBILE=0
                            RESULT="Negative cache entry"
                            ACTION=forward-native
                            
            RoundNormalNoLocatorInfo: 
            A round has a reply, and this reply theoretically contains locator-related information, however, due to some cause unknown, the locators contents are not printed, for example:
                
                            --- Round ID 1372759258 ----------------------------------->
                            Date=2013/07/02 10:00:58
                            EID=153.16.3.0
                            Resolver=149.20.48.61
                            Using source address (ITR-RLOC) 139.165.12.211
                            Send map-request to 149.20.48.61 (149.20.48.61) for 153.16.3.0 (153.16.3.0) ...
                            RECEIVED_FROM=128.122.208.144
                            RTT=0.15500
                            LOCATOR_COUNT=2
                            MAPPING_ENTRY=153.16.3.0/24
                            TTL=1440
                            AUTH=1
                            MOBILE=0
                            !!!! LCAF AFI print skipped !!!!
                            
                Note that locator_count is 2, but we could not check out the content of its included locators information

            
            
            RoundNormal:
            A round contains all information in which we are interested, refer to example given in item 'Round'


Locator: An information collection including locator address, locator state(up or down), locator priority(integer from 1 to 255 ) locator weight. A round's reply may contain multiple locators. Attention: locator address could be in IPV6 format. for example :

                            ...
                            LOCATOR0=192.162.230.11
                            LOCATOR0_STATE=up
                            LOCATOR0_PRIORITY=2
                            LOCATOR0_WEIGHT=50
                            ...
                            or
                            LOCATOR0=87.195.196.77
                            LOCATOR0_STATE=up
                            LOCATOR0_PRIORITY=50
                            LOCATOR0_WEIGHT=100
                            LOCATOR1=95.97.83.93
                            LOCATOR1_STATE=up
                            LOCATOR1_PRIORITY=10
                            LOCATOR1_WEIGHT=100
                            LOCATOR2=2001:9e0:8500:b00::1
                            LOCATOR2_STATE=up
                            LOCATOR2_PRIORITY=50
                            LOCATOR2_WEIGHT=100



Intra-logfile RLOC-Set consistence : This characteristic is defined at logfile level. A logfile is judged Intra-logfile
RLOC-set consistence if and only if the same log file satisfies the following critiera:

        1, The logfile contains uniquely RoundNormal types round.
        2, All rounds inside the logfile has the same value for locator_count
        3, The number of RLOC addresses appeared inside the logfile is same to locator_count.

Inter-logfile RLOC-set consistence : This characteristic is defined in the interior of a vantage directory :


===============>Capacity

This program should be able to realize the following comparison or verification, respectively:

First, the program verifies that in each logfile(in all vantage directory), whether every round is consistent in terms of intra-logfile RLOC set consistence.(Refer to item 'Intra-logfile RLOC-set consistance' in glossary section)

Second, this program is also able to check, in the same vantage, whether for a certain EID, all 13 different resovlers return the same RLOC set.

Third, it should be able to examine that for all the vantage point, for the same EID, all 13 different resolvers give the same reply.



================>Analysis

"/PlanetLab/liege/mappings/planetlab1-EID-153.16.14.0-MR-149.20.48.61.log" file is very representative.

First, at the beginning of file, rounds are always in RoundNoReply type, then locator_count is changed constantly among 1, 2, 3

"/PlanetLab/liege/mappings/planetlab1-EID-37.77.56.32-MR-149.20.48.61.log" contains IPV6 RLOC address.