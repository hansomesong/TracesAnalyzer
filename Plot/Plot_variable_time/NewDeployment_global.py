__author__ = 'yueli'

import subprocess

# Find out all the NewDeployment logs for MR-149.20.48.61 in liege, and put them into "NewDeployment_global_149.20.48.61_liege.csv"
subprocess.call('cat /Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time/comparison_time_liege.csv | cut -d ";" -f3 -f4 -f8 | grep "149.20.48.61" | grep "RoundNormal,NegativeReply" >> /Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time/NewDeployment_global_149.20.48.61_liege.csv', shell=True)

liege_MR1 = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/comparison_time/NewDeployment_global_149.20.48.61_liege.csv"


for line in open(liege_MR1):
    lines = line.split(";")
    print "----------------------"
    print lines
    for row in open("/Users/yueli/Documents/Codes/TracesAnalyzer/log/PlanetLab_CSV/liege/planetlab1-EID-"+lines[0]+"-MR-"+lines[1]+".log.csv"):
        rows = row.split(";")
        if rows[0] == "RoundNormal":
            print rows[1]
            break


    # 根据 lines[0]，lines[1]等在 /Users/yueli/Documents/Codes/TracesAnalyzer/log/PlanetLab_CSV/liege中打开相对应的.csv文件，
    # 格式为planetlab1-EID-lines[0]-MR-lines[1].log.csv
    # 记录由 Negative -> Normal 的时间Date或是experiment number，用长度为753的list来记录
    # 求出在某个experiment number上出现New Deployment的概率 即上式／NewDeployment_global_149.20.48.61_liege.csv的行数59