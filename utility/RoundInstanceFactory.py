# -*- coding: utf-8 -*-
# This module is used to compare list, because in method : isLocatorsFlap()
# we need to compare locators list (Locator object as element)
# refer to this link: http://stackoverflow.com/questions/9623114/python-are-two-lists-equal
import csv
import sys
import collections
import re
from operator import itemgetter, attrgetter
sys.path.append('../')
from netaddr import *

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
        self.MAPPING_ENTRY = self.getMappingEntry()

        # round_type_list，list数据类型，包含出现在logfile中所有round的类型
        self.round_type_list = list(
            set([round_obj.type for round_obj in self.rounds])
        )

        # A sorted list including all RLOC address appeared in a logfile.
        # This list could be empty if the target logfile does not contain RoundNormal type round
        # 注意： 因为其中含有IPV6地址，所以排序是个问题
        self.locator_addr_list = list(
            set(
                [locator.addr for round_obj in self.rounds if round_obj.type == 'RoundNormal'
                 for locator in round_obj.locators]
            )
        )

        # locator_list, list 数据类型，存储当前logfile中出现的所有不同的Locator对象
        # for round in self.rounds:
        # 以下if语句避免处理NoReply的情况
        # if round.type == 'RoundNormal':
        #         self.locator_list = self.locator_list.union(set(round.locators))
        #         self.locator_count_list = self.locator_count_list.union(set([round.locator_count]))
        # 其实在python中，大括号(curly braces)不仅可以用来创建dictionary还可以用来创建set,其等效于set()
        # 因为round.locators本身已经list了，如果需要用set comprehension 来创建set的话，就不可以用set([])
        # 实际运行证明：使用list/set comprehension效率确实要比传统的for loop效率高
        self.locator_list = list({
            locator for round_obj in self.rounds if round_obj.type == 'RoundNormal'
                for locator in round_obj.locators
        })

        # 按照locator的attribute id对locator_list进行排序
        # 参考链接：https://docs.python.org/2/howto/sorting.html
        self.locator_list = sorted(self.locator_list, key=attrgetter('id'))

        # locator_count_list, list数据类型，存储着当前logfile中出现的所有的locator_count取值
        self.locator_count_list = list({
            round_obj.locator_count for round_obj in self.rounds if round_obj.type == 'RoundNormal'
        })
        # 定义 RLOCSetCoherent 以及 TECoherent 对象属性
        # 注意 调用isRLOCSetCoherent()之前，self.rounds以及self.round_type_list 应该被创建好
        self.RLOCSetCoherent = self.isRLOCSetCoherent()
        self.TECoherent = self.isTECoherent()
        # self.RLOCSetCoherent 与 self.TECoherent 逻辑与 的结果作为 评判logfile是否为Coherent
        self.coherent = self.RLOCSetCoherent and self.TECoherent
        self.case = self.jugeLogCase()

    # Yue add a function to get MAPPING_ENTRY
    def getMappingEntry(self):
        mappingEntrylist = []

        # 从每一个非RoundNoReply的round里得到一个mapping entry
        # 删除mappingEntrylist_origin中会出现的error，并把 mapping_entry = '0.0.0.0/3'的替换为 '0.0.0.0/0'
        # 此list comprehension之后可得到 mappingEntrylist_withoutError = ['153.16.21.209/32', '0.0.0.0/0', '217.128.0.0/9', '37.77.57.224/27', '153.16.21.209/32', '153.16.21.209/32' ,'153.16.20.209/32']
        # mappingEntrylist_withoutError = [round_obj.mapping_entry.replace('\'0.0.0.0/3', '\'0.0.0.0/0') for round_obj in self.rounds if ((round_obj.type != 'RoundNoReply') and (IPAddress(round_obj.EID) in IPNetwork(round_obj.mapping_entry.replace('\'0.0.0.0/3', '\'0.0.0.0/0'))))]
        mappingEntrylist_withoutError = [
            re.sub(r"^0.0.0.0/3$", "0.0.0.0/0", round_obj.mapping_entry)
            for round_obj in self.rounds
            if ((round_obj.type != 'RoundNoReply') and
                (
                    IPAddress(round_obj.EID)
                        in IPNetwork(
                            re.sub(r"^0.0.0.0/3$", "0.0.0.0/0", round_obj.mapping_entry)
                        )
                )
            )
        ]

        # 统计出 mappingEntrylist_withoutError 中每个不同的mappingEntry出现了几次
        # 循环结束后可以得到类似这样的 counter = Counter({'153.16.21.209/32': 3, '2610:d0:212c::/48': 1, '153.16.20.209/32': 1, '217.128.0.0/9': 1, '37.77.57.224/27': 1})
        # list(counter.items()) = [('153.16.21.209/32', 3), ('2610:d0:212c::/48', 1), ('153.16.20.209/32', 1), ('217.128.0.0/9', 1), ('37.77.57.224/27', 1)]
        counter = collections.Counter()
        for mappingEntry in mappingEntrylist_withoutError:
            counter[mappingEntry] += 1

        return list(str(a) for a in counter.items())

        # # REGEX pattern to match IPv4, for the format: [('153.16.21.209/32', 3), ('153.16.20.209/32', 1), ('217.128.0.0/9', 1), ('37.77.57.224/27', 1)]
        # pattern_IPv4 = "\('\d+.\d+.\d+.\d+/\d+', \d\)"
        # # REGEX pattern to match IPv6, not for all but just for these formats: [('2610:d0:2138::/48', 4), ('2610:d0:2102::/48', 1), ('2610:d0:212c::/48', 1), ('2610:d0:216e::/48', 5), ('2610:d0:2122::/48', 1), ('2610:d0:216d::/48', 1)]
        # pattern_IPv6 = "\('([0-9a-fA-F]{1,4}:){3,3}:/\d+', \d\)"
        #
        # mappingEntryReduced = []
        # # 在mapping entry里去除数量为1的mapping entry，因为这些极有可能为error
        # for a in list(counter.items()):
        #     if re.match(pattern_IPv4, str(a), flags=0) or re.match(pattern_IPv6, str(a), flags=0):
        #         continue
        #     else:
        #         mappingEntryReduced.append(a)

        # 返回一个字符串格式的list，使得mp_parser里的csv_row.append(",".join(R.MAPPING_ENTRY))可用
        # return list(str(a) for a in mappingEntryReduced)


    def preprocess(self):
        '''
            This method is used to preprocess the input file, firstly read all lines into a single string
            then split obtained string into a list of substring(representing a round record).
        '''
        with open(self.file_path) as myfile:
            data = myfile.read().replace('\n', '')
        #Split target string with indicated delimiter then remove possible empty string
        #DELIMITER_P is a compiled pattern object imported from REPattern.py
        round_list = filter(None, DELIMITER_P.split(data))
        return round_list
    
    def roundCollectionGenerate(self, round_list):
        '''
            The element in rould_list parameter may be like this:
                'Date=2013/07/09 17:00:46EID=85.192.0.0Resolver=195.50.116.18Using source address (ITR-RLOC) 139.165.12.211Send map-request to 195.50.116.18 (195.50.116.18) for 85.192.0.0 (85.192.0.0) ...RECEIVED_FROM=195.50.116.18RTT=0.24900LOCATOR_COUNT=0MAPPING_ENTRY=2610:d0:1204::/48TTL=1AUTH=0MOBILE=0RESULT="Negative cache entry"ACTION=forward-native'
            Then we could use regular expression to extract wanted information.
            In fact we could directly use RE to extract interesting information
        '''
        # list comprehension to improve program execution efficiency which is equivalent to the following bloc
        rounds = [self.roundGenerate(target) for target in round_list]
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
        '''
            we suppose that target string always contains substring such as :
                LOCATOR0=129.250.1.255LOCATOR0_STATE=upOCATOR0_PRIORITY=254LOCATOR0_WEIGHT=0LOCATOR1=129.250.26.242LOCATOR1_STATE=upLOCATOR1_PRIORITY=1\n
                LOCATOR1_WEIGHT=100
        '''
        locator_list = [Locator(each[0], each[1], each[2], each[3], each[4]) for each in LOCATORS_P.findall(target)]
        return locator_list

    def write2csv(self, file_path):
        '''
            This function aims to writing all round records stored in given file into a CSV file
            More specifically, you could regard this CSV file as a table simplifying our analysis work
        '''
        with open(file_path, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel', delimiter=';')
            csv_title = self.rounds[0].getAttrList()
            spamwriter.writerow(csv_title)
            for round in self.rounds:
                spamwriter.writerow(round.toList())

    def isRLOCSetCoherent(self):
        """
            By default, RLOC set for a logfile is coherent(True), except for the following situations:
                1, There exists more than one possible values for locator count attribute in this logfile
                2, The only value of locator count attribute of this logfile is different with the length of
                    RLOC address set.
        """
        # By default, we consider RLOC-set consistence is always True
        flag = True

        # if round type list does not include 'RoundNormal', return directly True
        # 如果 NegativeReply 出现在logfile中则直接视为 RLOCSet Coherent false
        if 'RoundNormal' in self.round_type_list:
            # 如果文件中 至少含有 RoundNormal以及negativeReply 或者 roundnormal以及PrintSkipped
            # 注意：曾经这句话是这么写的：
            # if 'NegativeReply' or 'PrintSkipped' in self.round_type_list:
            # 因为if 'NegativeReply' 永远为True且其后跟的是or 所以 flag一直都是False
            if ('NegativeReply' or 'PrintSkipped') in self.round_type_list:
                flag = False
            # 如果文件中 含有RoundNormal却又不包含'NegativeReply'以及'PrintSkipped'（有可能含有NoReply）
            # 这种情况下 需要进一步的判断来确定 RLOC set是否为 Coherent
            if ('NegativeReply' and 'PrintSkipped') not in self.round_type_list:
                # 注意locator_count_list中所有元素均为string类型
                # len(locator_count_list) != 1 can judge whether the number of locator changes
                # list(locator_count_list)[0] != str(len(locator_list)) can judge whether the content of RLOC are same
                if len(self.locator_count_list) != 1 or self.locator_count_list[0] != str(len(self.locator_addr_list)):
                    flag = False
        return flag

    # To get the locator_list
    def getLocatorSet(self):
        # return len(self.locator_list)
        return "#".join([str(element) for element in self.locator_list])


    # Accordin to Yue's demand, add a new method
    # This method is used to detect the flap of locator and locator_count

# 按照宝贝儿要求，先注释掉 Flap相关的函数，用不到
    # def isLocatorCountFlap(self):
    #     # 所谓的 Locator Count Flap 是指 某一个 locator count的值在改变之后，又再次出现。
    #     # 假设 一个文件中出现的 locator count的取值依次是 1，2，3，1 我们说该文件具有 locator count flap的特性。
    #     # 需要注意的是： 只有 含有 RoundNormal型的 Log File 才具有 locator count flap的性质。
    #     # 如果没有Roundnormal 型的round,直接返回 None.
    #
    #     # 思路是： 遍历 rounds 这个list，将其中出现的locator_count值写到另外一个叫做
    #     # locator_count_sequence 的list中。只有在当前locator_count的值不等于 locator_count_sequence[-1]
    #     # 的情况下，才可以写入到目标list中。
    #     # 只遍历含有locator_count这个attribute的Round,也即是 RoundNormal 类型的
    #     # 获取 locator_count list (也许含有重复的元素)，比如 [1,1,1,2,2,2,2,3,3,3,1,1,2,2,3,3]
    #     # 所谓 Locator count flap 就是指 这类列表 [1,1,1,2,2,2,2,3,3,3,1,1,2,2,3,3]
    #
    #     #
    #     locator_count_flap = False
    #     # reduce_rounds = [round for round in self.rounds if round.type == 'RoundNormal']
    #     # locator_count_values = []
    #     # for round in reduce_rounds:
    #     #     locator_count_values.append(round.locator_count)
    #     locator_count_values = [round.locator_count for round in self.rounds if round.type == 'RoundNormal' ]
    #
    #     # 如果当前处理的logfile中不含有RoundNormal类型的Round,那么locator_count_values将会是空list.
    #     # 该方法将直接返回 None, 如果不为空，则继续处理判断是 True or false
    #     if len(locator_count_values) > 0:
    #         locator_count_sequence = list(locator_count_values[0])
    #         for count in locator_count_values[1:]:
    #             if count != locator_count_sequence[-1]:
    #                 locator_count_sequence.append(count)
    #
    #         # 以 [1,1,1,2,2,2,2,3,3,3,1,1,2,2,3,3] 为例, locator_count_sequence = [1,2,3,1,2,3]
    #         # 如果locator_count_sequence去除重复前后, 长度保持不变。说明locator_count_sequence不再有重复元素
    #         # 该logfile也就不具有 locator count flap的性质。
    #         # 该方法将返回 True,否则返回 False
    #         if len(list(set(locator_count_sequence))) != len(locator_count_sequence):
    #             locator_count_flap = True
    #     return locator_count_flap

    # def isLocatorsFlap(self):
    #     # Locator flape 指的是 某一个Locator变化后 再次出现，假设A B C代表三个不同的Locator
    #     # 序列 [A A] [B B] [B C] [C A] [A A] 可以视为 locators flap
    #
    #     # 默认 一个文件(不管包含不包含RoundNormal类型的Round)是不具备的 Locators flap 性质的
    #     # 只有在含有 RoundNormal 并且满足某些条件的情况下 才可以视为是 Locators flap为True的
    #     locators_flap = False
    #     locators = [round.locators for round in self.rounds if round.type == 'RoundNormal']
    #
    #     # 同样的，如果locators为lenght为零的话，说明该logfile中并不包含RoundNormal类型的Round
    #     # Locators flap对该logfile没有意义，该方法直接返回 None
    #     if len(locators) > 0:
    #         # 以locators的第一个元素初始化 locators_sequence
    #         # 注意： 如果是 locators_sequence = list(locators[0])，程序会有问题。。
    #         # 换言之， 操作符[] 和 list() 在某些场合下不等效！！！
    #         locators_sequence = [locators[0]]
    #         # http://stackoverflow.com/questions/9623114/python-are-two-lists-equal
    #         # compare 采用 collections module提供的方法来判断两个list 是否相等。
    #         # 如果两个list含有的元素一致（不考虑顺序）， 则compare(x,y)返回 True
    #         compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    #
    #         # 和isLocatorCountFlap()方法类似，我们遍历所有的 locators，如果当前处理的locators和最近一次添加到locators_sequence
    #         # 的元素不一样，则将locators添加至 locators_sequence 之中
    #         for current in locators[1:]:
    #             # 本来current中的元素都是一个个locator，如果不把这个locator转换成str的话，貌似compare不管用。。。
    #             # current = [str(element) for element in current]
    #             # print current
    #             # target = [str(element) for element in locators_sequence[-1]]
    #             # print target
    #             if not compare(current, locators_sequence[-1]):
    #                 # 如果current和 locators_sequence最后一个元素不同，则将current添加至 locators_sequence 之中
    #                  locators_sequence.append(current)
    #
    #         # Now 序列 序列 [A A] [B B] [B B][B C] [C A] [A A] => [A A] [B B] [B C] [C A] [A A]
    #         # 遍历 locators_sequence 看看 是否有元素 重复出现，如果是 locator_flap = True,并且返回。。
    #         while len(locators_sequence) > 1:
    #             current = locators_sequence.pop()
    #             # print "current", [str(element) for element in current]
    #             # print "locators length", len(locators_sequence)
    #             # print "current locators's content:"
    #             # for x in locators_sequence:
    #             #     print [str(y) for y in x]
    #             if current in locators_sequence:
    #                 locators_flap = True
    #                 #print "In if-condition", [str(element) for element in current]
    #                 break
    #     return locators_flap


    def isTECoherent(self):
        """
            This method is used to verify whether currently processed logfile is coherent in terms of
            traffic engineering. Traffic engineering is meaningful in case RLOC is coherent and reflected by attributes
            such as weight, priority and status in Locator object. Current logfile is regarded as non-TE-coherent if any
             of aforementioned attributes is changed.
        """
        # 解决思路，按照要求：按照定义, Locator对象中，weight,priority 抑或 status只要有任意一项改变即可以视为TE发生了改变。
        # 其实，这要这三项中有一项发生了改变，那么Locator这个对象其实就发生了改变。那么这个问题就可以简化为判断一个Locator在该日志、
        # 记录的一系列实验中是否有发生过改变，如果有，则立即终止遍历，返回判断结果

        # The intial value of flag stems from the reuslt of method isRLOCSetCoherent()
        flag = self.isRLOCSetCoherent()

        # if initial flag value is True, we continue to verify if TE is coherent, else directly return False
        # as result
        # 如果 该日志的 LocatorCoherent属性为True, 我们看看是否有可能 TECoherent会变为False。
        # 如果 LocatorCoherent属性为False, 那么毫无悬念 TECoherent结果为False

        # 方法中定义方法，用以比较Locator,我们只根据 id, state, priority和state(TE相关的参数）来判断比较
        def customized_eq(self, other):
            return self.id == other.id and self.state == other.state and self.priority == other.priority and self.weight == other.weight

        def customized_hash(self):
            return hash(self.id) ^ hash(self.state) ^ hash(self.priority) ^ hash(self.weight)

        Locator.__hash__ = customized_hash
        Locator.__eq__ = customized_eq

        if flag is True:
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
                        flag = False
                        # 如果 存在两个比较元素不一致，则修改flag为False然后退出for循环
                        break
        return flag

    def jugeLogCase(self):
        '''
            This method is used to judge to which case the current logfile belongs under the condition coherent is false.
            Possible case value is following:
                case 1 (New deployment)  : logfile containing Normal and Negative types
                case 2 (Mobility)        : logfile containing certain Round where its attribute "mobile" is set to 1
                case 3 (Reconfiguration) : Occurrence of any change <= 3 in consecutive 24h
                case 4 (Instability)     : Contrary to case 3, occurrence of any change > 3 in consecutive 24h
                case 5                   : other situations
            else
                case 0                   : if logfile is coherent
            Note: Possible changes are:
                Traffic engineering changes (any of weigh, priority and status changes)
                RLOC set changes (Locator count or RLOC address changes)

                但是以上两种变化 可以变化为：
                locator_count 会变化
                locators list发生变化 (包含RLOC address的变化以及诸如weight, priority 还有 status的变化)

                其实我觉得只要看locators list发生的变化就好了。。。因为如果 locator list 从A B C变化到 A B C D那么势必locator_count
                会从3变到4。所以将 locator_count的变化次数和 RLOC变化次数相加没有意
        '''
        # 如果该logfile是coherent的，属于case0
        # 需要定义如何比较Locator对象
        def customized_eq(self, other):
            return self.__dict__ == other.__dict__

        def customized_hash(self):
            return hash(self.id) ^ hash(self.addr) ^ hash(self.state) ^ hash(self.priority) ^ hash(self.weight)

        Locator.__hash__ = customized_hash
        Locator.__eq__ = customized_eq

        if self.coherent:
            return '0'

        # 自然而言，剩下的情况就是 coherent is false的情况， 依据不同的情况，归类于 case 1, 2, 3, 4
        else:
            if ('RoundNormal' and 'NegativeReply') in self.round_type_list:
                return '1' # (New deployment)
            else:
                # 查看是否有mobile为1的情况出现, 即case2
                # 注意除了 RoundNoReply的情况，每种round object都含有mobile这个参数
                for round_obj in [element for element in self.rounds if element.type is not 'RoundNoReply']:
                    if round_obj.mobile is '1':
                        # 如果循环中发现了 mobile=1，立即停止循环并推出程序
                        return '2'
                # 接下来 处理case3和case4的情况

                # 处理case3 case4的时候我们仅考虑Normal类型的round
                rounds_reduced = [round_obj for round_obj in self.rounds if round_obj.type == 'RoundNormal']
                # 刚才跟宝贝儿商量过了，我们就是按照每天（比如0点到24点）的统计范围来计数每天的change数目
                # 第一步，讲rounds按照日期分割为多个子集，每个子集仅包含当日记录的实验结果
                # 对每个子集统计其相应的locator_count以及Locators (包含在Normal类型)变化的总数
                # 第一步 获得当前log中出现过得所有的 date
                # 遍历只含有 RoundNormal类型的 rounds_reduced,获取logfile中出现过的日期,并排序
                date_list = sorted(list(set([round_obj.date.date() for round_obj in rounds_reduced])))
                #print date_list

                ## 测试date_list是否执行正确
                #print [date]

                # 创建round_all_day，其element为包含同一天记录的round的list
                # 采用Nested list comprehension提高程序效率 (可读性则不是太好)
                rounds_all_day = [[round_obj for round_obj in rounds_reduced if round_obj.date.date() == day]
                                  for day in date_list]
                #print rounds_all_day

                # 定义一个名为compare的lambda函数，用来比较 两个list是否相等，这里面list将会是locator list
                # 该compare函数采用collections module提供的方法来判断两个list 是否相等。
                # 如果两个list含有的元素一致（不考虑顺序）， 则compare(x,y)返回 True
                # 该实现吸取了链接： http://stackoverflow.com/questions/9623114/python-are-two-lists-equal
                compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
                # 以下For循环用以填充以上定义的两个空list
                # 填充之后的 比如locators_change 将会是比如[[False, False, True, False], [False, True, False], ...]
                # locator_count_change = []
                locators_change = []

                for round_day in rounds_all_day:
                    # 统计locators(locator list)的变化情况
                    locators_day_list = [round_obj.locators for round_obj in round_day]
                    referent_locators = locators_day_list[0]
                    tmp_list = []
                    for locators in locators_day_list[1:]:
                        # 如果当前locators和参考locators(即当前项的前一项)相比结果为True说明没有发生变化
                        # 是故将False添加进 tmp_list
                        tmp_list.append(compare(locators, referent_locators))
                        # 结束循环之际，记得修改 参考locators,不然每一项都是和第一项相比的
                        referent_locators = locators
                    locators_change.append(tmp_list)

                change_number_day = [element.count(False) for element in locators_change]
                if max(change_number_day) > 3:
                    case = '4'
                else:
                    case = '3'

                return case


    # 2015-04-01：Add new functions to count new deployement number, change time and change pattern
    # New deployment refers to a transition from normal type to negative or from negative to normal
    # at a certain instant (No reply type is skipped)
    def statistics_new_deployment(self):
        if "RoundNormal" in self.round_type_list and "NegativeReply" in self.round_type_list:
            count = 0
            pattern = []
            times = []
            # select the first element whose type is not RoundNoReply as the initial_ref
            initial_ref = self.rounds[0].type
            i = 1
            while initial_ref is 'RoundNoReply':
                initial_ref = self.rounds[i].type
                i = i+1
            pattern.append(self.rounds[i-1].type)

            # 注意 compare the inequality of two string, should use operator '!=' instead of 'is not'
            for j in range(i, len(self.rounds)):
                # print j, entries[j][0], initial_ref, entries[j][0] != initial_ref
                if self.rounds[j].type != 'RoundNoReply' and self.rounds[j].type != initial_ref:
                    count += 1
                    initial_ref = self.rounds[j].type
                    pattern.append(self.rounds[j].type)
                    times.append(self.rounds[j].date.strftime("%d/%m/%Y %H:%M:%S"))

            return [count, ','.join(times), '->'.join(pattern)]
        else:
            return [0, 0, 0]


    # 2015-06-10：Add new functions to count reconfiguration number, change time and change pattern
    # Reconfiguration refers to the times of change are <= 3 times per day
    # No Map Reply type is skipped
    def statistics_reconfiguration(self):
        if "RoundNormal" in self.round_type_list and "NegativeReply" not in self.round_type_list:
            count = 0
            pattern = []
            times = []
            # select the first Locator count and RLOC(s) of RoundNormal as the initial_ref
            # 如果此Round是RoundNoReply，则无法取到初始值，继续查看下一行直到有RoundNormal出现为止
            initial_ref = self.rounds[0].type
            i = 1
            while initial_ref is 'RoundNoReply':
                initial_ref = self.rounds[i].type
                i = i+1
            initial_ref_locator_count = self.rounds[i-1].locator_count
            initial_ref_locators = self.rounds[i-1].locators
            pattern.append(str((self.rounds[i-1].locator_count, self.rounds[i-1].locators)))

            # 从获取初始值的那一行开始向后比较
            for j in range(i, len(self.rounds)):
                # print j, entries[j][0], initial_ref, entries[j][0] != initial_ref
                if self.rounds[j].type == 'RoundNormal' and \
                        (self.rounds[j].locator_count != initial_ref_locator_count or self.rounds[j].locators != initial_ref_locators):
                    count += 1
                    initial_ref_locator_count = self.rounds[j].locator_count
                    initial_ref_locators = self.rounds[j].locators
                    pattern.append(str((self.rounds[j].locator_count, self.rounds[j].locators)))
                    times.append(self.rounds[j].date.strftime("%d/%m/%Y %H:%M:%S"))

            return [count, ','.join(times), '->'.join(pattern)]
        else:
            return [0, 0, 0]


    # 2015-06-10：Add new functions to count RLOCMadness number, change time and change pattern
    # RLOCMadness refers to the times of change are <= 3 times per day
    # No Map Reply type is skipped
    def statistics_RLOCMadness(self):
        if "RoundNormal" in self.round_type_list and "NegativeReply" not in self.round_type_list:
            count = 0
            pattern = []
            times = []
            # select the first Locator count and RLOC(s) of RoundNormal as the initial_ref
            # 如果此Round是RoundNoReply，则无法取到初始值，继续查看下一行直到有RoundNormal出现为止
            initial_ref = self.rounds[0].type
            i = 1
            while initial_ref is 'RoundNoReply':
                initial_ref = self.rounds[i].type
                i = i+1
            initial_ref_locator_count = self.rounds[i-1].locator_count
            initial_ref_locators = self.rounds[i-1].locators
            pattern.append(str((self.rounds[i-1].locator_count, self.rounds[i-1].locators)))

            # 从获取初始值的那一行开始向后比较
            for j in range(i, len(self.rounds)):
                # print j, entries[j][0], initial_ref, entries[j][0] != initial_ref
                if self.rounds[j].type == 'RoundNormal' and \
                        (self.rounds[j].locator_count != initial_ref_locator_count or self.rounds[j].locators != initial_ref_locators):
                    count += 1
                    initial_ref_locator_count = self.rounds[j].locator_count
                    initial_ref_locators = self.rounds[j].locators
                    pattern.append(str((self.rounds[j].locator_count, self.rounds[j].locators)))
                    times.append(self.rounds[j].date.strftime("%d/%m/%Y %H:%M:%S"))

            return [count, ','.join(times), '->'.join(pattern)]
        else:
            return [0, 0, 0]




