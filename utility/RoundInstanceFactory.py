import csv
import sys
sys.path.append('../')

#If we use syntax such as 'import Request', when executing Python
from model.Locator import *
from model.Round import *
from REPattern_opt import *

class RoundInstanceFactory:
    """This is a factory class whose objective is to generate a list of Round instance from a input file"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.rounds = self.roundCollectionGenerate(self.preprocess())
       
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
        round = Round()
        if "No map-reply received" in target:
            '''If substring "No map-reply received is present in target string, we could judge this is Type 1 round record
                we should rely TYPE_1_P regular expression to process this string
            "'''
            try:
                round.date, round.EID, round.resolver, round.req_src, round.req_dst, round.req_for\
                    = infoFieldExtractor(target, TYPE_1_P)[0]
                round.type = 1
            except IndexError:
                print "Error occurred when converting Type I Round from string :\n\t{0}\nThe current file :\t{1}".format(
                    target,self.file_path)
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
                    round.date, round.EID, round.resolver, round.req_src, round.req_dst, round.req_for, \
                        round.rpy_src, round.RTT, round.locator_count, round.mapping_entry,\
                        round.TTL, round.auth, round.mobile, round.result, round.action = infoFieldExtractor(target, TYPE_2_P)[0]
                    if 'forward-native' in round.action:
                        round.type = 20
                    elif 'send-map-request' in round.action:
                        round.type = 21
                    else:
                        round.type = 29
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
                    round.date, round.EID, round.resolver, round.req_src, round.req_dst, round.req_for, \
                        round.rpy_src, round.RTT, round.locator_count, round.mapping_entry,\
                        round.TTL, round.auth, round.mobile = infoFieldExtractor(target, TYPE_3_P)[0]
                    round.type = 3
                    round.warn = "!!!! LCAF AFI print skipped !!!!"
                except IndexError:
                    print "Error occurred when converting TYPE 3 Round from string:"
                    print "\t{0}\nThe file being processed is :{1}".format(target,self.file_path)

            else:
                '''We consider that the last case is to process round record containing locators information'''
                try:
                    round.date, round.EID, round.resolver, round.req_src, round.req_dst, round.req_for, \
                        round.rpy_src, round.RTT, round.locator_count, round.mapping_entry,\
                        round.TTL, round.auth, round.mobile = infoFieldExtractor(target, TYPE_3_P)[0]
                    round.locators = self.locatorGenerate(target)
                    round.type = 0
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
            spamwriter.writerow(
                ['Round Type', 'Date', 'EID', 'Resolver','Request_SRC','Request_DST','Request_FOR','Reply_SRC',
                 'RTT', 'LOCATOR_Count','MAPPING_ENTRY','TTL','AUTH', 'MOBILE'
                ]
            )            
            for round in self.rounds:
                spamwriter.writerow(round.toList())
        
        
    def isLocatorCoherent(self):
        '''This method is uniquely meaningful for file log containg locators information
            By default, we consider that a log file is always coherent in terms of locators count.
            For type I round(No map-reply message), round has no reply, thus we regard it as coherent in terms of locators.
            For type II round(Negative Cache entry), round has reply but has not locators info. locator_count = 0
            For type III round(LCAF AFI print skipped), round has locators info(locator_count > 0), however locators info is not printed
                we still think it is coherent
            For type IV round(has locators list), should judge locator_count and the length of locators
        '''
        flag = True
        locator_set = set()
        locator_count = 0
        for round in self.rounds:
            #Attention! make sure that round.locators is not None type, otherwise an exception will thrown.
            if round.locators:
                locator_set = locator_set | set(round.locators)
                locator_count = len(round.locators)
                if len(locator_set) != locator_count:
                    flag = False
                    #As long as incoherence is found in current log file, break the current for loop and return false
                    break
        return flag
    
    def getRoundTypeSet(self):
        type_set = set()
        for round in self.rounds:
            type_set = type_set | set([round.type])   
        return type_set

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
                    #As long as incoherence is found in current log file, break the current for loop and return false
        return [flag,type_set]
