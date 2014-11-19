__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
import socket


# Import the targeted raw CSV file
rawCSV_file = "/Users/yueli/Documents/Codes/TracesAnalyzer/log/planetlab1-EID-153.16.18.176-MR-217.8.98.46.log.csv"

time = []
unsortedRlocList = []

i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[0] == "Round Type":
        continue
    else:
        #time.append(i)
        if lines[0] == "RoundNoReply":
            if "0.0.0.0" in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append("0.0.0.0")
        elif int(lines[9]) == 1:
            if lines[15] in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append(lines[15])
        else:
            if "-999.999.999.999" in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append("-999.999.999.999")

print unsortedRlocList
sortedRlocList = sorted(unsortedRlocList, key=lambda item: socket.inet_aton(item))
print sortedRlocList

j = -1
rlocList = []
for line1 in open(rawCSV_file):
    j = j + 1
    lines1 = line1.split(";")
    if lines1[0] == "Round Type":
        continue
    else:
        time.append(j)
        if lines1[0] == "RoundNoReply":
            rlocList.append(sortedRlocList.index("0.0.0.0"))
        elif int(lines1[9]) == 1:
            rlocList.append(sortedRlocList.index(lines1[15]))
        else:
            rlocList.append(sortedRlocList.index("-999.999.999.999"))

print time.__len__()
print rlocList.__len__()


#Plot begins here
plt.scatter(time, rlocList, color="blue", label="RLOCset", s=1)

plt.xlabel("Time (2013/07/02 07:30 - 2013/07/18 23:30)")
plt.ylabel("RLOC set")
plt.title("RLOC sets by time")

plt.savefig("/Users/yueli/Documents/Codes/TracesAnalyzer/Plot/Plot_variable_time/Case3.png")
plt.show()