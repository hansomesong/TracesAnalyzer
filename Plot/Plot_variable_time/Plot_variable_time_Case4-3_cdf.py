__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
import socket
from config.config import *

# Import the targeted raw CSV file
rawCSV_file = os.path.join(PLANET_CSV_DIR, 'liege', 'planetlab1-EID-153.16.18.176-MR-217.8.98.46.log.csv')

time = []
unsortedRlocList = []

i = -1
for line in open(rawCSV_file):
    i = i + 1
    lines = line.split(";")
    if lines[LOG_COLUMN['round_type']] == "Round Type":
        continue
    else:
        #time.append(i)
        if lines[LOG_COLUMN['round_type']] == "RoundNoReply":
            if "0.0.0.0" in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append("0.0.0.0")
        elif int(lines[LOG_COLUMN['locator_count']]) == 1:
            if lines[LOG_COLUMN['locator_id']].split(',')[1] in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append(lines[LOG_COLUMN['locator_id']].split(',')[1])
        else:
            if "-999.999.999.999" in unsortedRlocList:
                continue
            else:
                unsortedRlocList.append("-999.999.999.999")

#print unsortedRlocList
#sortedRlocList = sorted(unsortedRlocList, key=lambda item: socket.inet_aton(item))
#print sortedRlocList

sortedRlocList =[]
sortedRlocList.append("0.0.0.0")
for k in unsortedRlocList:
    if k == "0.0.0.0":
        continue
    else:
        sortedRlocList.append(k)

#print "sortedRlocList:", sortedRlocList
#print "sortedRlocList.__len__():", sortedRlocList.__len__()

j = -1
rlocList = []
for line1 in open(rawCSV_file):
    j = j + 1
    lines1 = line1.split(";")
    if lines1[LOG_COLUMN['round_type']] == "Round Type":
        continue
    else:
        time.append(j)
        if lines1[LOG_COLUMN['round_type']] == "RoundNoReply":
            rlocList.append(sortedRlocList.index("0.0.0.0"))
        elif int(lines1[LOG_COLUMN['locator_count']]) == 1:
            rlocList.append(sortedRlocList.index(lines1[LOG_COLUMN['locator_id']].split(',')[1]))
        else:
            rlocList.append(sortedRlocList.index("-999.999.999.999"))

print "time.__len__():", time.__len__()
print "rlocList:", rlocList
print "rlocList.__len__():", rlocList.__len__()


# Calculate the pdf here
# x-axis of this pdf means that the duration we use the same RLOC
# Take the first check, but the list of pdf_temp contains lots of 0 at the end, because of the initialization de list
value_temp = 1
index = 0
pdf_temp = []
for i in range(0, rlocList.__len__()):
    pdf_temp.append(0)

for value in rlocList:
    if value == value_temp:
        index = index + 1
    else:
        value_temp = value

        pdf_temp[index] = pdf_temp[index] + 1
        index = 1

pdf_temp[index] = pdf_temp[index] + 1

print "pdf_temp:", pdf_temp

# To delete the 0 at the end of list pdf_temp, we use the reversed list of pdf_temp,
# so that the 0 "at the beginning" can be removed
pdf_tempReversed = []
for x in reversed(pdf_temp):
    if (x == 0) and (pdf_tempReversed.__len__() == 0):
        continue
    else:
        pdf_tempReversed.append(x)

print "pdf_tempReversed:", pdf_tempReversed
print "pdf_tempReversed.__len__():", pdf_tempReversed.__len__()

# The pdf list without lots of 0 at the end
total = round(sum(pdf_tempReversed), 5)
print "total =", total
pdf = []
for y in reversed(pdf_tempReversed):
    pdf.append(y/total*100)

print "pdf:", pdf
print "length of pdf:", pdf.__len__()


# Calculate the cumulative percentage of each dedicated packet size, and put them into a list
cdf = []
cdf_per = 0
for k in pdf:
    cdf_per = cdf_per + k
    cdf.append(cdf_per)
print "cdf:", cdf
print "length of cdf:", cdf.__len__()


#Plot begins here

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(16,14)

duration = np.linspace(0, pdf.__len__(), pdf.__len__())
# plt.scatter(duration, cdf, color="blue", label="RLOCset", s=5)
plt.plot(duration, cdf, color="black", linewidth=5)


plt.xlim(0,230)
plt.ylim(50,101)
# To plot the zoom
# plt.xlim(0,60)
# plt.ylim(50,100)

plt.xlabel("number of consecutive round", fontsize=50)
plt.ylabel("cdf (%)", fontsize=50)
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)

# plt.title("Cdf of the duration in which the same RLOC is used")
plt.grid(True)


plt.savefig(os.path.join(PLOT_DIR, 'Plot_variable_time', 'Case4-3_cdf_plot.eps'), dpi=300)
# plt.show()