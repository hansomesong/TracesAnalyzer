#Attention! RoundInstanceFactory is in fact a python script where defines uniquely a python class
#If we want to instantiate this class, use its method
#Using syntax like "from RoundInstanceFactory import *" instead of "import RoundInstanceFactory"


# Inspired from this post : http://pymotw.com/2/argparse/, we add unix-like command line argument
from utility.RoundInstanceFactory import *
from config.config import *
import os
import argparse

parser = argparse.ArgumentParser(description='This utility is devoted to convert a input LISP trace log file into a formatted CSV file.')
parser.add_argument('log', action="store", help='indicate the LISP trace log file path.')
parser.add_argument('--dst', action="store",dest='destination', default="log/", help='indicate which directory stores the generated files.' )

args = parser.parse_args()
print '**************************The summary of provided arguments for this utility shown as following:**********************'
print 'logfile                          =', args.log
print 'output generated csv directory   =', args.destination

default_csv_name = os.path.basename(args.log)+'.csv'


# The following variable stores the full path for generated CSV file.
csv_file_path = os.path.join(args.destination, default_csv_name)
print 'generated csv file\'s full path   =', csv_file_path


RoundInstanceFactory(args.log).write2csv(csv_file_path)
