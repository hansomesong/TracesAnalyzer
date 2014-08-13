#We need to the two following module to convert a datetime string to a timestamp
import time
import datetime


# Attention, if you forget to choose object as the parent class of base class
# you will encounter some problems when invoking super() in subclass
class Round(object):
    #The string below is a brief introduction about current class, it could be retrieved by calling Class.__doc__ 
    """Class Round is a data structure used to represent a request-reply pair"""
    type = 999
    locators = None

    def __init__(self, date, EID, resolver,req_src, req_dst, req_for):
    # The parent class Round always contais attributes as following:
    # date, EID, resolver, request_source@, request_destination@, request_for@
        self.date = date
        self.EID = EID
        self.resolver = resolver
        self.req_src = req_src
        self.req_dst = req_dst
        self.req_for = req_for
        # Amazing,in subclass, when super().__init__ is called, self.type will take the appropriate type for subclass...
        # Amazing! Amazing! Amazing!
        self.type = self.__class__.__name__

    def toList(self):
    # Whatever the round type is, it always contains the following basic attributes.
        round_attribute_list = [
             self.type, self.date, self.EID, self.resolver, self.req_src, self.req_dst, self.req_for
         ]
        return round_attribute_list

    def getAttrList(self):
        return ['Round Type', 'Date', 'EID', 'Resolver', 'Request_SRC', 'Request_DST', 'Request_FOR']



    


# To leverage the polymorphic of OOP, we plan use different subclass to represent every found type.
class RoundNoReply(Round):
    def __init__(self,date, EID, resolver, req_src, req_dst, req_for):

        super(RoundNoReply,self).__init__(date, EID, resolver, req_src, req_dst, req_for)
        self.error = "*** No map-reply received ***"
        self.type = self.__class__.__name__

    def toList(self):

        round_attribute_list = super(RoundNoReply, self).toList()
        round_attribute_list.append(self.error)
        return round_attribute_list

    def getAttrList(self):
        res = super(RoundNoReply, self).getAttrList()
        res.extend(['Error'])
        return res


class RoundResultAction(Round):

    def __init__(self, date, EID, resolver,req_src, req_dst, req_for,rpy_src, RTT, locator_count, mapping_entry,
             TTL, auth, mobile, result, action):
        super(RoundResultAction, self).__init__(date, EID, resolver, req_src, req_dst, req_for)
        self.rpy_src = rpy_src
        self.RTT = RTT
        self.locator_count = locator_count
        self.mapping_entry = mapping_entry
        self.TTL = TTL
        self.auth = auth
        self.mobile = mobile
        self.result = result
        self.action = action

    def toList(self):
        round_attribute_list = super(RoundResultAction, self).toList()
        round_attribute_list.extend(
                [self.rpy_src, self.RTT, self.locator_count, self.mapping_entry,
                 self.TTL, self.auth, self.mobile, self.result, self.action]
        )
        return round_attribute_list

    def getAttrList(self):
        res = super(RoundResultAction, self).getAttrList()
        res.extend(['Reply_SRC', 'RTT', 'LOCATOR_Count','MAPPING_ENTRY', 'TTL', 'AUTH', 'MOBILE', 'Result', 'Action'])
        return res

class RoundNormalNoLocatorInfo(Round):

    def __init__(self, date, EID, resolver,req_src, req_dst, req_for,rpy_src, RTT, locator_count, mapping_entry,
             TTL, auth, mobile):
        super(RoundNormalNoLocatorInfo, self).__init__(date, EID, resolver, req_src, req_dst, req_for)
        self.rpy_src = rpy_src
        self.RTT = RTT
        self.locator_count = locator_count
        self.mapping_entry = mapping_entry
        self.TTL = TTL
        self.auth = auth
        self.mobile = mobile

        self.warn= '!!!! LCAF AFI print skipped !!!!'

    def toList(self):
        round_attribute_list = super(RoundNormalNoLocatorInfo, self).toList()
        round_attribute_list.extend(
                [self.rpy_src, self.RTT, self.locator_count, self.mapping_entry,
                 self.TTL, self.auth, self.mobile, self.warn]
        )
        return round_attribute_list

    def getAttrList(self):
        res = super(RoundNormalNoLocatorInfo, self).getAttrList()
        res.extend(['Reply_SRC', 'RTT', 'LOCATOR_Count','MAPPING_ENTRY', 'TTL', 'AUTH', 'MOBILE'])
        return res

class RoundNormal(Round):

    def __init__(self, date, EID, resolver, req_src, req_dst, req_for, rpy_src, RTT, locator_count, mapping_entry,
                 TTL, auth, mobile, locators):
        super(RoundNormal, self).__init__(date, EID, resolver, req_src, req_dst, req_for)
        self.rpy_src = rpy_src
        self.RTT = RTT
        self.locator_count = locator_count
        self.mapping_entry = mapping_entry
        self.TTL = TTL
        self.auth = auth
        self.mobile = mobile
        self.locators = locators


    def toList(self):

        round_attribute_list = super(RoundNormal, self).toList()
        round_attribute_list.extend(
                [self.rpy_src, self.RTT, self.locator_count, self.mapping_entry,
                 self.TTL, self.auth, self.mobile]
        )
        for locator in self.locators:
            round_attribute_list.extend(locator.toList())
        return round_attribute_list


    def getAttrList(self):
        res = super(RoundNormal, self).getAttrList()
        res.extend(['Reply_SRC', 'RTT', 'LOCATOR_Count','MAPPING_ENTRY', 'TTL', 'AUTH', 'MOBILE',
                    'Locator_Number','Locator_Addr','Locator_State', 'Locator_Priority', 'Locator_Weight'])
        return res



