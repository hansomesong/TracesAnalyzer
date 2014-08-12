#We need to the two following module to convert a datetime string to a timestamp
import time
import datetime

class Round:
    #The string below is a brief introduction about current class, it could be retrieved by calling Class.__doc__ 
    """Class Round is a data structure used to represent a request-reply pair"""
    type = 999
    locators = None
    def __init__(self):
        pass

    def toString(self):
        res = "--- Round ID {4}-------------->\nDate={0}\nEID={1}\nResolver={2}\n{3}\n".format(
            self.date, self.EID, self.resolver, self.request.toString(),self.timestamp
            )
        if self.reply:
            res+=self.reply.toString()
        else:
            res+= "*** No map-reply received ***\n"
        return res
    
    # def toList(self):
    #
    #     round_attribute_list = [
    #         self.type,self.date, self.resolver, self.request.req_src,self.request.req_dst,
    #         self.request.req_for
    #     ]
    #
    #     if self.reply:
    #         ''''If current round contains reply, round_attribute_list to be written into target CSV file should be
    #             extended with reply's attribute list.
    #         '''
    #         round_attribute_list.extend(self.reply.toList())
    #
    #     return round_attribute_list

    def toList(self):

        # Whatever the round type is, it always contains the following basic attributes.
        round_attribute_list = [
            self.type, self.date,self.EID, self.resolver, self.req_src,  self.req_dst, self.req_for
        ]

        if self.type in range(20,30):
            round_attribute_list.extend(
                [self.rpy_src, self.RTT, self.locator_count, self.mapping_entry,
                 self.TTL, self.auth, self.mobile, self.result, self.action]
            )
        elif self.type == 3:
            round_attribute_list.extend(
                [self.rpy_src, self.RTT, self.locator_count, self.mapping_entry,
                 self.TTL, self.auth, self.mobile, self.warn]
            )

        elif self.type == 0:
            round_attribute_list.extend(
                [self.rpy_src, self.RTT, self.locator_count, self.mapping_entry,
                 self.TTL, self.auth, self.mobile])
            for locator in self.locators:
                round_attribute_list.extend(locator.toList())

        elif self.type == 1:
            round_attribute_list.append("No map-reply received")

        return round_attribute_list
    


