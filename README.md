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


Locator: An information collection including locator address, locator state(up or down), locator priority(integer from 1 to 255 )
locator weight. for example :

                            ...
                            LOCATOR0=192.162.230.11
                            LOCATOR0_STATE=up
                            LOCATOR0_PRIORITY=2
                            LOCATOR0_WEIGHT=50
                            ...


Intra-logfile RLOC-Set consistence : This characteristic is defined at logfile level. A logfile is judged Intra-logfile
RLOC-set consistence if and only if the same log file satisfies the following critiera:

        1, The logfile contains uniquely RoundNormal types round.
        2, All rounds inside the logfile has the same value for locator_count
        3, The number of RLOC addresses appeared inside the logfile is same to locator_count.

Inter-logfile RLOC-set consistence : This characteristic is defined in the interior of a vantage directory :


===============>Capacity

This program should be able to realize the following comparison, respectively:


这个脚本应该具备执行三种比较的能力,分别是:

第一, 同一个logfile中， 以时间为变量，比较并确认，每一个Round的关于RLOC（即Locator）的信息都是一致的，具体说来

我们认为，一个目标文件，需满足严格的条件才能具有，在RLOC Set(即 Locator address set)层面一致性的性质。当且仅当，该目标logfile中仅含有Normal Round（Normal型Round是指，在向某一Resolver问询某一EID的exchange中，该request收到了Reply，并且Reply中y必定包含Locator相关的信息域，例如locator_addr, locator_priority,etc.）， 并且所有Round中的locator_count信息域的值均一致（不能出现某一次Round的locator_count为1，另一次locator_count为2或其他取值。），该logfile中出现的locator addr的数目也跟locator_count一致
如果目标logfile中含有多种Round类型，则判定该实验结果，在RLOC上不一致
如果目标logfile中
