# This class is used to abstract a log file whose name is in format such as :
# planetlab1-EID-153.16.18.176-MR-217.8.98.46.log


class LogFile(object):
    def __init__(self, vantage, file_path, rounds):
        # Instance attribute 'vantage' stores the name of the vantage point
        self.vantage = vantage

        # Instance attribute 'file_path' stores the absolute path to this log file
        self.file_path = file_path

        # Instance attribute 'rounds' is a list including all round type instances in this log file.
        # Other utility script, LogFileHelper (previously named RoundInstanceFactory), is in charge of providing round list.
        self.rounds = rounds

        self.EID = self.rounds[0].EID
        self.resolver = self.rounds[0].resolver


        self.round_type_list = self.getRoundTypeList()
        # A sorted list including all locator addressses appeared in a logfile.
        # This list could be empty if the target logfile does not contain RoundNormal type round
        self.locator_addr_list = self.getLocatorAddrSet()

# Test part==========================
