# -*- coding: utf-8 -*-
class Locator(object):
    """This data structure is used to represent the locator contained  in a LISP map-reply.
    Its format could be like:
        LOCATOR0=129.250.1.255
        LOCATOR0_STATE=up
        LOCATOR0_PRIORITY=254
        LOCATOR0_WEIGHT=0
        LOCATOR1=129.250.26.242
        LOCATOR1_STATE=up
        LOCATOR1_PRIORITY=1
        LOCATOR1_WEIGHT=100  
    """
    #code
    def __init__(self, id, addr, state, priority, weight):
        self.id = id
        self.addr = addr
        self.state = state
        self.priority = priority
        self.weight = weight
        
    def toString(self):
        res = "LOCATOR{0}={1}\nLOCATOR{0}_STATE={2}\nLOCATOR{0}_PRIORITY={3}\nLOCATOR{0}_WEIGHT={4}\n".format(self.id,self.addr,self.state,self.priority,self.weight)
        return res
    
    # def toList(self):
    #     return [self.id, self.addr, self.state, self.priority, self.weight]

    def toList(self):
        return ",".join([self.id, self.addr, self.state, self.priority, self.weight])

    # 重大修改：
    # 为了能灵活的比较Locator对象，比如仅按照addr或者id来比较，我们决定在运行的时候再定义__hash__以及__eq__
    # def __eq__(self, other):
    #     print "__eq__ is called"
    #     print self.__dict__
    #     return self.__dict__ == other.__dict__
    #
    # def __hash__(self):
    #     print "I was called!!"
    #     return hash(self.id) ^ hash(self.addr) ^ hash(self.state) ^ hash(self.priority) ^ hash(self.weight)


    def __str__(self):
        # Just return the Locator's address
        # return self.addr

        # Return the Locator's all the infomation
        res = "LOCATOR{0}={1},LOCATOR{0}_STATE={2},LOCATOR{0}_PRIORITY={3},LOCATOR{0}_WEIGHT={4}".format(
            self.id,
            self.addr,
            self.state,
            self.priority,
            self.weight
        )
        return res

## Test for Locator

if __name__ == '__main__':
    l1 = Locator('0', "129.250.1.255", 'up', '100', '0')
    l2 = Locator('1', "129.250.2.255", 'up', '100', '0')
    l3 = Locator('0', "129.250.2.255", 'down', '100', '0')
    l4 = Locator('3', "129.250.3.255", 'up', '100', '0')
    l5 = Locator('1', "129.250.3.255", 'up', '100', '30')
    l6 = Locator('1', "129.250.23.255", 'up', '100', '90')
    l6 = Locator('1', "129.250.13.255", 'up', '100', '90')
    l7 = Locator('1', "129.250.9.255", 'up', '10', '0')

    # if l1 == l2:
    #     print True
    # else:
    #     print False

    def hash_id(self):
        print "customized hash_id is called and id is ", hash(self.id)
        return hash(self.id)^ hash(self.state) ^ hash(self.priority) ^ hash(self.weight)
    def equal_id(self, other):
        return self.id == other.id and self.state == other.state and self.priority == other.priority and self.weight == other.weight


    Locator.__hash__ = hash_id
    Locator.__eq__ = equal_id

    locator_set = {l1, l2, l3, l4, l5, l6, l7}
    # print "when creating with l2, which function between __eq__ and __hash__ will be called?"
    # locator_list = set([l2])
    # print "Then, try to add l1 into target set"
    # locator_list.union([l1])
    # print "Then, try to add l3 into target set"
    # locator_list.union([l3])
    # print "Then, try to add l7 into target set"
    # locator_list.union([l7])
    # print "Then, try to add l6 into target set"
    # locator_list.union([l6])
    # print ""
    # print len(locator_list)
    for locator in locator_set:
        print locator

    import sys
    print sys.getsizeof(l1)
    print sys.getsizeof(locator_set)
    print sys.getsizeof(set([1,2,3,4,8,8,8,8]))
    print sys.getsizeof(list())



    