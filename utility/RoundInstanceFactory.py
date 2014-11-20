# -*- coding: utf-8 -*-
import csv
import sys
# This module is used to compare list, because in method : isLocatorsFlap()
# we need to compare locators list (Locator object as element)
# refer to this link: http://stackoverflow.com/questions/9623114/python-are-two-lists-equal
import collections
sys.path.append('../')

#If we use syntax such as 'import Request', when executing Python
from model.Locator import *
from model.Round import *
from REPattern_opt import *

class RoundInstanceFactory:
    """This is a factory class whose objective is to generate a list of Round instance from a input file"""

    # Maybe in the future, we could define a LogFile class to reduce the volume of the current class
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.rounds = self.roundCollectionGenerate(self.preprocess())

        # It is much more convenient to define some attributes for a log file
        self.EID = self.rounds[0].EID
        self.resolver = self.rounds[0].resolver
        self.round_type_list = self.getRoundTypeList()
        # A sorted list including all locator addressses appeared in a logfile.
        # This list could be empty if the target logfile does not contain RoundNormal type round
        self.locator_addr_list = self.getLocatorAddrSet()
        # Since these 2 variables are also used in another method, we make them as 2 object variables from
        # isLocatorCoherent(self) here
        self.locator_set = set()
        self.locator_count_set = set()
       
    def preprocess(self):
        '''This method is used to preprocess the input file, firstly read all lines into a single string
            then split obtained string into a list of substring(representing a round record).
        '''
        with open(self.file_path) as myfile:
            data = myfile.read().replace('\n','')
        #Split target string with indicated delimiter then remove possible empty string
        #DELIMITER_P is a compiled pattern object imported from REPattern.py
        round_list = filter(None,DELIMITER_P.split(data))
        return round_list
    
    def roundCollectionGenerate(self, round_list):
        ''''The element in rould_list parameter may be like this:
                'Date=2013/07/09 17:00:46EID=85.192.0.0Resolver=195.50.116.18Using source address (ITR-RLOC) 139.165.12.211Send map-request to 195.50.116.18 (195.50.116.18) for 85.192.0.0 (85.192.0.0) ...RECEIVED_FROM=195.50.116.18RTT=0.24900LOCATOR_COUNT=0MAPPING_ENTRY=2610:d0:1204::/48TTL=1AUTH=0MOBILE=0RESULT="Negative cache entry"ACTION=forward-native'
            Then we could use regular expression to extract wanted information.
            In fact we could directly use RE to extract interesting information
        '''
        rounds= []
        for target in round_list:
            rounds.append(self.roundGenerate(target))
        return rounds

    def roundGenerate(self, target):
        '''This method is used to convert an input string(named target) into a Round instance.
            Because the round record is in one of the four known format, firstly we have to determine
            which RE expression to process the input string, and then
        '''
        round = None
        if "No map-reply received" in target:
            '''If substring "No map-reply received is present in target string, we could judge this is Type 1 round record
                we should rely TYPE_1_P regular expression to process this string
            "'''
            try:
                date, EID, resolver, req_src, req_dst, req_for = infoFieldExtractor(target, TYPE_1_P)[0]
                round = RoundNoReply(date, EID, resolver, req_src, req_dst, req_for)
            except IndexError:
                print "Error occurred when converting Type I Round from string :\n\t{0}\nThe current file :\t{1}".format(
                    target, self.file_path)
        else:
            '''When target string does not includ substring as "No map-reply received", we could judge
                this round contains a reply. Thus we could extract some obligatory attributes(rpy_src, RTT,locator_count)
                for Reply instance
            '''
            if "Negative cache entry" in target:
                '''This bloc of code is used to process this kind of reply:
                        RECEIVED_FROM=149.20.48.61
                        RTT=0.15700
                        LOCATOR_COUNT=0
                        MAPPING_ENTRY=0.0.0.0/3
                        TTL=9
                        AUTH=0
                        MOBILE=0
                        RESULT="Negative cache entry"
                        ACTION=forward-native
                    Therefore, we could use TYPE_2_P to process the input target string
                '''
                try:
                    date, EID, resolver, req_src, req_dst, req_for, rpy_src, RTT, locator_count, mapping_entry,\
                        TTL, auth, mobile, result, action = infoFieldExtractor(target, TYPE_2_P)[0]
                    round = NegativeReply(date, EID, resolver, req_src, req_dst, req_for, rpy_src, RTT,
                                              locator_count, mapping_entry,TTL, auth, mobile, result, action)

                except IndexError:
                    print "Error occurred when converting TYPE 2 Round from string:"
                    print "\t{0}\nThe file being processed is :{1}".format(target,self.file_path)

            elif "LCAF AFI print skipped" in target:
                '''The case where a MAP-Reply is recieved, but locators information is not printed.
                    Thus extract basic information such as :
                        RECEIVED_FROM=128.122.208.144
                        RTT=0.15600
                        LOCATOR_COUNT=2
                        MAPPING_ENTRY=153.16.3.0/24
                        TTL=1440
                        AUTH=1
                        MOBILE=0
                    without considering locator
                    we could use TYPE_3_P to process this string
                '''
                try:
                    date, EID, resolver, req_src, req_dst, req_for, rpy_src, RTT, locator_count, mapping_entry,\
                        TTL, auth, mobile = infoFieldExtractor(target, TYPE_3_P)[0]
                    round = PrintSkipped(date, EID, resolver, req_src, req_dst, req_for, rpy_src, RTT, locator_count, mapping_entry,\
                        TTL, auth, mobile)

                except IndexError:
                    print "Error occurred when converting TYPE 3 Round from string:"
                    print "\t{0}\nThe file being processed is :{1}".format(target,self.file_path)

            else:
                '''We consider that the last case is to process round record containing locators information'''
                try:
                    date, EID, resolver, req_src, req_dst, req_for, rpy_src, RTT, locator_count, mapping_entry,\
                        TTL, auth, mobile = infoFieldExtractor(target, TYPE_3_P)[0]
                    round = RoundNormal(date, EID, resolver, req_src, req_dst, req_for, rpy_src, RTT, locator_count, mapping_entry,\
                        TTL, auth, mobile, self.locatorGenerate(target))
                except IndexError:
                    print "Error occurred when converting TYPE 0 Round from string:"
                    print "\t{0}\nThe file being processed is :{1}".format(target,self.file_path)

        return round
    
    def locatorGenerate(self, target):
        '''we suppose that target string always contains substring such as :
                LOCATOR0=129.250.1.255LOCATOR0_STATE=upOCATOR0_PRIORITY=254LOCATOR0_WEIGHT=0LOCATOR1=129.250.26.242LOCATOR1_STATE=upLOCATOR1_PRIORITY=1\n
                LOCATOR1_WEIGHT=100
        '''
        locator_list = []
        for each in LOCATORS_P.findall(target):
            ''''each variable could be in format like ('0', '129.250.1.255', 'up', '254', '0')'''
            locator_list.append(Locator(each[0],each[1],each[2],each[3],each[4]))
        return locator_list
    
    def write2csv(self,file_path):
        '''This function aims to writing all round records stored in given file into a CSV file
            More specifically, you could regard this CSV file as a table simplifying our analysis work
        '''
        with open(file_path,'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel',delimiter=';')
            csv_title = self.rounds[0].getAttrList()
            spamwriter.writerow(csv_title)
            for round in self.rounds:
                spamwriter.writerow(round.toList())
        
        
    # def isLocatorCoherent(self):
    #     '''This method is uniquely meaningful for file log containg locators information'''
    #
    #     # By default, we consider RLOC-set consistence is always false
    #     flag = False
    #     locator_set = set()
    #     locator_count_set = set()
    #     # if round type include types other than RoundNormal, return directly false
    #     if len(self.round_type_list) == 1 and ('RoundNormal' in self.round_type_list):
    #         # All rounds inside the logfile has the same value for locator_count
    #         # According to the above 'if' statement, all rounds in the attribute 'rounds' are in RoundNormal type.
    #         #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    #         for round in self.rounds:
    #             locator_set = locator_set | set(round.locators)
    #             locator_count_set = locator_count_set | set([round.locator_count])
    #         # All rounds inside the logfile has the same value for locator_count
    #         # The number of RLOC addresses appeared inside the logfile is same to locator_count.
    #         # Do not forget element in locator_count_set is in type : string
    #         if len(locator_count_set) == 1 and list(locator_count_set)[0] == str(len(locator_set)):
    #             flag = True
    #     return flag


    def isLocatorCoherent(self):
        #   There exists some quirks about this method
        #   We are not sure about the definition of Locator Set Coherence characteristics. In this method,
        #   we choose a loose condition for locator set coherence.

        # By default, we consider RLOC-set consistence is always True
        flag = True

        # Since these 2 variables are also used in another method, we make them as 2 object variables
        # locator_set = set()
        # locator_count_set = set()

        # if round type list does not include 'RoundNormal', return directly True
        if 'RoundNormal' in self.round_type_list:
            # All rounds inside the logfile has the same value for locator_count
            # According to the above 'if' statement, all rounds in the attribute 'rounds' are in RoundNormal type.
            #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            for round in self.rounds:
                if round.type == 'RoundNormal':
                    self.locator_set = self.locator_set | set(round.locators)
                    self.locator_count_set = self.locator_count_set | set([round.locator_count])
            # All rounds inside the logfile has the same value for locator_count
            # The number of RLOC addresses appeared inside the logfile is same to locator_count.
            # Do not forget element in locator_count_set is in type : string
            # len(locator_count_set) != 1 can judge whether the number of locator changes
            # list(locator_count_set)[0] != str(len(locator_set)) can judge whether the content of RLOC are same
            if len(self.locator_count_set) != 1 or list(self.locator_count_set)[0] != str(len(self.locator_set)):
                flag = False
        return flag


    # To get the locator_count_set
    def getLocatorCountSet(self):
        # return len(self.locator_count_set)
        return list(self.locator_count_set)

    # To get the locator_set
    def getLocatorSet(self):
        # return len(self.locator_set)
        return [str(element) for element in list(self.locator_set)]


    def getRoundTypeList(self):
        type_set = set()
        for round in self.rounds:
            type_set = type_set | set([round.type])
        # Finally convert a set into list and return the latter.
        return list(type_set)

    def getLocatorAddrSet(self):
        # Attention : RLOC Address set may contain some IPV6 addresses, which bring some difficulties when sorting
        import socket
        reduced_rounds = [round for round in self.rounds if round.type == 'RoundNormal']
        locatorAddrList = []
        for round in reduced_rounds:
            for locator in round.locators:
                locatorAddrList.append(locator.addr)
        res_set = set(locatorAddrList)
        #return sorted(list(res_set), key=lambda item: socket.inet_aton(item))
        return list(res_set)


    # Accordin to Yue's demand, add a new method
    # This method is used to detect the flap of locator and locator_count

    def isLocatorCountFlap(self):
        # 所谓的 Locator Count Flap 是指 某一个 locator count的值在改变之后，又再次出现。
        # 假设 一个文件中出现的 locator count的取值依次是 1，2，3，1 我们说该文件具有 locator count flap的特性。
        # 需要注意的是： 只有 含有 RoundNormal型的 Log File 才具有 locator count flap的性质。
        # 如果没有roundnormal 型的round,直接返回 None.

        # 思路是： 遍历 rounds 这个list，将其中出现的locator_count值写到另外一个叫做
        # locator_count_sequence 的list中。只有在当前locator_count的值不等于 locator_count_sequence[-1]
        # 的情况下，才可以写入到目标list中。
        # 只遍历含有locator_count这个attribute的Round,也即是 RoundNormal 类型的
        # 获取 locator_count list (也许含有重复的元素)，比如 [1,1,1,2,2,2,2,3,3,3,1,1,2,2,3,3]
        # 所谓 Locator count flap 就是指 这类列表 [1,1,1,2,2,2,2,3,3,3,1,1,2,2,3,3]

        #
        locator_count_flap = False
        # reduce_rounds = [round for round in self.rounds if round.type == 'RoundNormal']
        # locator_count_values = []
        # for round in reduce_rounds:
        #     locator_count_values.append(round.locator_count)
        locator_count_values = [round.locator_count for round in self.rounds if round.type == 'RoundNormal' ]

        # 如果当前处理的logfile中不含有RoundNormal类型的Round,那么locator_count_values将会是空list.
        # 该方法将直接返回 None, 如果不为空，则继续处理判断是 True or false
        if len(locator_count_values) > 0:
            locator_count_sequence = list(locator_count_values[0])
            for count in locator_count_values[1:]:
                if count != locator_count_sequence[-1]:
                    locator_count_sequence.append(count)

            # 以 [1,1,1,2,2,2,2,3,3,3,1,1,2,2,3,3] 为例, locator_count_sequence = [1,2,3,1,2,3]
            # 如果locator_count_sequence去除重复前后, 长度保持不变。说明locator_count_sequence不再有重复元素
            # 该logfile也就不具有 locator count flap的性质。
            # 该方法将返回 True,否则返回 False
            if len(list(set(locator_count_sequence))) != len(locator_count_sequence):
                locator_count_flap = True
        return locator_count_flap

    def isLocatorsFlap(self):
        # Locator flape 指的是 某一个Locator变化后 再次出现，假设A B C代表三个不同的Locator
        # 序列 [A A] [B B] [B C] [C A] [A A] 可以视为 locators flap

        # 默认 一个文件(不管包含不包含RoundNormal类型的Round)是不具备的 Locators flap 性质的
        # 只有在含有 RoundNormal 并且满足某些条件的情况下 才可以视为是 Locators flap为True的
        locators_flap = False
        locators = [round.locators for round in self.rounds if round.type == 'RoundNormal']

        # 同样的，如果locators为lenght为零的话，说明该logfile中并不包含RoundNormal类型的Round
        # Locators flap对该logfile没有意义，该方法直接返回 None
        if len(locators) > 0:
            # 以locators的第一个元素初始化 locators_sequence
            # 注意： 如果是 locators_sequence = list(locators[0])，程序会有问题。。
            # 换言之， 操作符[] 和 list() 在某些场合下不等效！！！
            locators_sequence = [locators[0]]
            # http://stackoverflow.com/questions/9623114/python-are-two-lists-equal
            # compare 采用 collections module提供的方法来判断两个list 是否相等。
            # 如果两个list含有的元素一致（不考虑顺序）， 则compare(x,y)返回 True
            compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

            # 和isLocatorCountFlap()方法类似，我们遍历所有的 locators，如果当前处理的locators和最近一次添加到locators_sequence
            # 的元素不一样，则将locators添加至 locators_sequence 之中
            for current in locators[1:]:
                # 本来current中的元素都是一个个locator，如果不把这个locator转换成str的话，貌似compare不管用。。。
                # current = [str(element) for element in current]
                # print current
                # target = [str(element) for element in locators_sequence[-1]]
                # print target
                if not compare(current, locators_sequence[-1]):
                    # 如果current和 locators_sequence最后一个元素不同，则将current添加至 locators_sequence 之中
                     locators_sequence.append(current)

            # Now 序列 序列 [A A] [B B] [B B][B C] [C A] [A A] => [A A] [B B] [B C] [C A] [A A]
            # 遍历 locators_sequence 看看 是否有元素 重复出现，如果是 locator_flap = True,并且返回。。
            while len(locators_sequence) > 1:
                current = locators_sequence.pop()
                # print "current", [str(element) for element in current]
                # print "locators length", len(locators_sequence)
                # print "current locators's content:"
                # for x in locators_sequence:
                #     print [str(y) for y in x]
                if current in locators_sequence:
                    locators_flap = True
                    #print "In if-condition", [str(element) for element in current]
                    break
        return locators_flap




