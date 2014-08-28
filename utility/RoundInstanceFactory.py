import csv
import sys
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

        # It is much more pratique to define some attributes for a log file
        self.EID = self.rounds[0].EID
        self.resolver = self.rounds[0].resolver
        self.round_type_list = self.getRoundTypeList()
        # A sorted list including all locator addressses appeared in a logfile.
        # This list could be empty if the target logfile does not contain RoundNormal type round
        self.locator_addr_list = self.getLocatorAddrSet()
       
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
        '''This method is used to convert a input string(named target) into a Round instance.
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
        
        
    def isLocatorCoherent(self):
        '''This method is uniquely meaningful for file log containg locators information'''

        # By default, we consider RLOC-set consistence is always false
        flag = False
        locator_set = set()
        locator_count_set = set()
        # if round type include types other than RoundNormal, return directly false
        if len(self.round_type_list) == 1 and ('RoundNormal' in self.round_type_list):
            # All rounds inside the logfile has the same value for locator_count
            # According to the above 'if' statement, all rounds in the attribute 'rounds' are in RoundNormal type.
            #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            for round in self.rounds:
                locator_set = locator_set | set(round.locators)
                locator_count_set = locator_count_set | set([round.locator_count])
            # All rounds inside the logfile has the same value for locator_count
            # The number of RLOC addresses appeared inside the logfile is same to locator_count.
            # Do not forget element in locator_count_set is in type : string
            if len(locator_count_set) == 1 and list(locator_count_set)[0] == str(len(locator_set)):
                flag = True
        return flag
    
    def getRoundTypeList(self):
        type_set = set()
        for round in self.rounds:
            type_set = type_set | set([round.type])
        # Finally convert a set into list and return the latter.
        return list(type_set)

    def basicCheck(self):
        type_set = set()
        flag = True
        locator_set = set()
        locator_count = 0
        for round in self.rounds:
            type_set = type_set | set([round.type])
            if round.locators:
                locator_set = locator_set | set(round.locators)
                locator_count = len(round.locators)
                if len(locator_set) != locator_count:
                    flag = False
                    #As long as incoherence is found in current log file, break the current for loop and return false$
        return [flag, list(type_set)]

    def getLocatorAddrSet(self):
        import socket
        reduced_rounds = [round for round in self.rounds if round.type == 'RoundNormal']
        locatorAddrList = []
        for round in reduced_rounds:
            for locator in round.locators:
                locatorAddrList.append(locator.addr)
        res_set = set(locatorAddrList)
        return sorted(list(res_set), key=lambda item: socket.inet_aton(item))

