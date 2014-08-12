import csv
#Attention! RoundInstanceFactory is in fact a python script where defines uniquely a python class
#If we want to instantiate this class, use its method
#Using syntax like "from RoundInstanceFactory import *" instead of "import RoundInstanceFactory"
from utility.RoundInstanceFactory import *
from config.config import *

file_path = '/home/cloud/Documents/PlanetLab/Liege/mappings/planetlab1-EID-153.16.2.0-MR-173.36.254.164.log'
file_path2 = '/home/cloud/Documents/PlanetLab/Liege/mappings/planetlab1-EID-153.16.2.0-MR-217.8.98.42.log'

file_path3 ='/home/cloud/Documents/PlanetLab/Liege/mappings/planetlab1-EID-85.192.0.0-MR-195.50.116.18.log'

#This file contains action=send-map-request
file_path4 = "/home/cloud/Documents/PlanetLab/liege/mappings/planetlab1-EID-153.16.50.32-MR-202.51.247.10.log"
target_path = csv_file_destDir+"error.csv"

RoundInstanceFactory(file_path4).write2csv(target_path)
