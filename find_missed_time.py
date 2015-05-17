__author__ = 'yueli'

from config.config import *
import datetime



rawCSV_file1 = os.path.join(
    PLANET_CSV_DIR, 'liege', "planetlab1-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file2 = os.path.join(
    PLANET_CSV_DIR, 'temple', "planetlab2-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file3 = os.path.join(
    PLANET_CSV_DIR, 'ucl', "onelab1-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file4 = os.path.join(
    PLANET_CSV_DIR, 'umass', "planetlab2-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

rawCSV_file5 = os.path.join(
    PLANET_CSV_DIR, 'wiilab', "planetlab2-EID-153.16.47.16-MR-198.6.255.37.log.csv"
)

f1_exp_time = []
with open(rawCSV_file1) as f_handler:
    next(f_handler)
    for line in f_handler:
        tmp_list = line.split(";")
        tmp_dt = datetime.datetime.strptime(tmp_list[1], "%Y-%m-%d %H:%M:%S")
        f1_exp_time.append(
            datetime.datetime(tmp_dt.year, tmp_dt.month, tmp_dt.day, tmp_dt.hour, tmp_dt.minute)
        )
print f1_exp_time

f2_exp_time = []
with open(rawCSV_file2) as f_handler:
    next(f_handler)
    for line in f_handler:
        tmp_list = line.split(";")
        tmp_dt = datetime.datetime.strptime(tmp_list[1], "%Y-%m-%d %H:%M:%S")
        f2_exp_time.append(
            datetime.datetime(tmp_dt.year, tmp_dt.month, tmp_dt.day, tmp_dt.hour, tmp_dt.minute)
        )
print f2_exp_time

f3_exp_time = []
with open(rawCSV_file3) as f_handler:
    next(f_handler)
    for line in f_handler:
        tmp_list = line.split(";")
        tmp_dt = datetime.datetime.strptime(tmp_list[1], "%Y-%m-%d %H:%M:%S")
        f3_exp_time.append(
            datetime.datetime(tmp_dt.year, tmp_dt.month, tmp_dt.day, tmp_dt.hour, tmp_dt.minute)
        )
print f3_exp_time

f4_exp_time = []
with open(rawCSV_file4) as f_handler:
    next(f_handler)
    for line in f_handler:
        tmp_list = line.split(";")
        tmp_dt = datetime.datetime.strptime(tmp_list[1], "%Y-%m-%d %H:%M:%S")
        f4_exp_time.append(
            datetime.datetime(tmp_dt.year, tmp_dt.month, tmp_dt.day, tmp_dt.hour, tmp_dt.minute)
        )
print f4_exp_time

f5_exp_time = []
with open(rawCSV_file5) as f_handler:
    next(f_handler)
    for line in f_handler:
        tmp_list = line.split(";")
        tmp_dt = datetime.datetime.strptime(tmp_list[1], "%Y-%m-%d %H:%M:%S")
        f5_exp_time.append(
            datetime.datetime(tmp_dt.year, tmp_dt.month, tmp_dt.day, tmp_dt.hour, tmp_dt.minute)
        )
print f5_exp_time

tmp = []
tmp.extend(f1_exp_time)
tmp.extend(f2_exp_time)
tmp.extend(f3_exp_time)
tmp.extend(f4_exp_time)
tmp.extend(f5_exp_time)

all_list = list(set(tmp))
common_part = list(set(f1_exp_time) & set(f2_exp_time) & set(f3_exp_time) & set(f4_exp_time) & set(f5_exp_time))
print sorted(all_list)

f1_rest = list(set(f1_exp_time) - set(common_part))
print "Rest f1:", f1_rest


f2_rest = list(set(f2_exp_time) - set(common_part))
print "Rest f2", f2_rest

f3_rest = list(set(f3_exp_time) - set(common_part))
print "Rest f3", f3_rest

f4_rest = list(set(f4_exp_time)- set(common_part))
print "Rest f4", f4_rest

f5_rest = list(set(f5_exp_time) - set(common_part))
print "Rest f5", f5_rest


