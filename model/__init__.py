# About the role of __init__.py
# The __init__.py files are required to make python treat the directories as packages.
# This is done to prevent directories with a common name, such as string, from unintentionally hiding
# valid modules that occur later on the module search path. In the simplest case,__init__.py could
# just be an empty file
# Without the current file. the syntax like "from model.Locator import * does not work

# The model directory(package) stores all designed data structure for this small project
# First, we need to know the format of log file to be processed
# The first Round format possibly appeared in a log file
    # --- Round ID 1372750223 ----------------------------------->
    # Date=2013/07/02 07:30:23
    # EID=0.0.0.0
    # Resolver=173.36.254.164

    # Using source address (ITR-RLOC) 139.165.12.211
    # Send map-request to 173.36.254.164 (173.36.254.164) for 0.0.0.0 (0.0.0.0) ...
    # Send map-request to 173.36.254.164 (173.36.254.164) for 0.0.0.0 (0.0.0.0) ...
    # Send map-request to 173.36.254.164 (173.36.254.164) for 0.0.0.0 (0.0.0.0) ...
    # *** No map-reply received ***

# The second Round format:
    #--- Round ID 1372750223 ----------------------------------->
    #Date=2013/07/02 07:30:23
    #EID=0.0.0.0
    #Resolver=149.20.48.61

    #Using source address (ITR-RLOC) 139.165.12.211
    #Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
    #RECEIVED_FROM=149.20.48.61
    #RTT=0.15700
    #LOCATOR_COUNT=0
    #MAPPING_ENTRY=0.0.0.0/3
    #TTL=9
    #AUTH=0
    #MOBILE=0
    #RESULT="Negative cache entry"
    #ACTION=forward-native

# A variant of second Round format(the only different is in ACTION field):
    #--- Round ID 1372750223 ----------------------------------->
    #Date=2013/07/02 07:30:23
    #EID=0.0.0.0
    #Resolver=149.20.48.61

    #Using source address (ITR-RLOC) 139.165.12.211
    #Send map-request to 149.20.48.61 (149.20.48.61) for 0.0.0.0 (0.0.0.0) ...
    #RECEIVED_FROM=149.20.48.61
    #RTT=0.15700
    #LOCATOR_COUNT=0
    #MAPPING_ENTRY=0.0.0.0/3
    #TTL=9
    #AUTH=0
    #MOBILE=0
    #RESULT="Negative cache entry"
    #ACTION=send-map-request

# The third Round Type format:
    # --- Round ID 1372759258 ----------------------------------->
    # Date=2013/07/02 10:00:58
    # EID=153.16.3.0
    # Resolver=149.20.48.61
    #
    # Using source address (ITR-RLOC) 139.165.12.211
    # Send map-request to 149.20.48.61 (149.20.48.61) for 153.16.3.0 (153.16.3.0) ...
    # RECEIVED_FROM=128.122.208.144
    # RTT=0.15500
    # LOCATOR_COUNT=2
    # MAPPING_ENTRY=153.16.3.0/24
    # TTL=1440
    # AUTH=1
    # MOBILE=0
    # !!!! LCAF AFI print skipped !!!!

# The forth Round Type format:
    # --- Round ID 1372755632 ----------------------------------->
    # Date=2013/07/02 09:00:32
    # EID=153.16.1.0
    # Resolver=149.20.48.61
    #
    # Using source address (ITR-RLOC) 139.165.12.211
    # Send map-request to 149.20.48.61 (149.20.48.61) for 153.16.1.0 (153.16.1.0) ...
    # RECEIVED_FROM=129.250.26.242
    # RTT=0.16500
    # LOCATOR_COUNT=2
    # MAPPING_ENTRY=153.16.1.0/24
    # TTL=1440
    # AUTH=1
    # MOBILE=0
    # LOCATOR0=129.250.1.255
    # LOCATOR0_STATE=up
    # LOCATOR0_PRIORITY=254
    # LOCATOR0_WEIGHT=0
    # LOCATOR1=129.250.26.242
    # LOCATOR1_STATE=up
    # LOCATOR1_PRIORITY=1
    # LOCATOR1_WEIGHT=100


# Second, we could extract and deduce data structure from above four types round format
# *Round could be represented by a class
# *Round is composed by its own attributes(Date, EID, Resolver), a request and its reply
# *Request information could be abstracted as Request instance which contains attributes: request source@ dst@ and for@
# *Similarily, Reply information could be stored in an instance of Reply Class
# *Reply instance is various: it may be None, may contains RLOC information(locator information)

# Although separating a

#




