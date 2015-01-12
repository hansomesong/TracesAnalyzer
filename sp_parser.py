import os


#Attention! RoundInstanceFactory is in fact a python script where defines uniquely a python class
#If we want to instantiate this class, use its method
#Using syntax like "from RoundInstanceFactory import *" instead of "import RoundInstanceFactory"
from utility.RoundInstanceFactory import *
from config.config import *


#To accelerate execution speed, we plan to firstly store all log entry into a single string, then write to CSV file



def generateMultiCSVRows(logDirRoot):
    res_str = []
    res_str.append(['Log File Name', 'Locator Count Coherence', 'Round Type Set'])
    for lists in os.listdir(logDirRoot):
        if lists.endswith(".log"):
            file_path = os.path.join(logDirRoot,lists)
            R = RoundInstanceFactory(file_path)
            csv_row = [file_path]
            csv_row.extend(R.basicCheck())
            res_str.append(csv_row)
    return res_str

def write2csv(target, resultCSVPath):
    import csv
    with open(resultCSVPath,'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel',delimiter=';')
        spamwriter.writerow(target)

def processLogDirectory(logDirRoot, resultCSVPath):
    '''This methos is used to iterate a given log file directory to process each LISP trace log and write the result to a CSV file'''
    
    #Do not forget to process uniquely log files...
    import csv
    with open(resultCSVPath, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel',delimiter=';')
        spamwriter.writerow(
            [
                'Log File Name',
                'Locator Count Coherence',
                'Round Type Set',
                'Different Locator Count',
                'Different Locator',
                'Locator count flap'
            ]
        )
        for log_file in os.listdir(logDirRoot):
            #Do not forget to verify that the current file to be processed is a real log file
            #Otherwise this program may be collapsed.
            if log_file.endswith(".log"):
                file_path = os.path.join(logDirRoot,log_file)
                R = RoundInstanceFactory(file_path)
                csv_row = [file_path]
                csv_row.append(R.RLOCSetCoherent)
                csv_row.append(R.round_type_list)
                csv_row.append(R.getLocatorCountSet())
                csv_row.append(R.getLocatorSet())
                # csv_row.append(R.isLocatorCountFlap())
                # csv_row.append(R.isLocatorsFlap())
                # Output case
                csv_row.append(R.jugeLogCase())
                csv_row.extend(R.locator_addr_list)
                spamwriter.writerow(csv_row)


csv_file = csv_file_destDir+'sp_statistic_v4.csv'
processLogDirectory(traces_log['liege'], csv_file)
#write2csv(generateMultiCSVRows(traces_log['liege']),csv_file)



