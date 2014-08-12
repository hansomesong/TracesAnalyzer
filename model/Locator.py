class Locator:
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
    
    def toList(self):
        return [self.id, self.addr, self.state, self.priority, self.weight]
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return hash(self.id) ^ hash(self.addr) ^ hash(self.state) ^ hash(self.priority) ^ hash(self.weight)

    
    
    