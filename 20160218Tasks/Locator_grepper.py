# -*- coding: utf-8 -*-
__author__ = 'yueli'

from config.config import *
import os

# 将所有要查看的 IP 写入一个 .txt 文档，然后对整个文档求其对应的 AS，并写入 .txt 文档
def locator_finder_all(input, output, date):
    count = 0
    locaters = []
    for line in open(input):
            lines = line.split(";")
            if lines[6] == "False" and "NegativeReply" not in lines[9]:
                locaters.extend([i.split(",")[0] for i in lines[13].split("#") if i.split(",")[0] not in locaters])
                print lines[1]
                count += 1
                print count

    output = open(output, 'w+')
    output.write('begin\n')

    for locater in locaters:
        ip = locater.split("=")[1]
        output.write(ip+'\t'+ date +'\n')
        print ip

    output.write('end')
    output.close()



# 根据每个 mapping 文件，立即生成 IP 所对应的 AS, 并将结果存入文档
def locator_finder_dynamic(input, output, date):
    output = open(output, 'w+')

    count = 0
    for line in open(input):
            lines = line.split(";")
            if lines[6] == "False" and "NegativeReply" not in lines[9]:
                count += 1
                print count
                print lines[1] # print path
                output.write(str(count) + '\n' + lines[1] + '\n')

                locators = [ j.split('=')[1] for j in [i.split(",")[0] for i in lines[13].split("#")]]
                output.write("Locators =" + str(locators) + '\n')

                for ip in locators:
                    # os.system("whois -h whois.cymru.com '{0}	{1}' >> {2}".format(ip, date, output_AS_file))
                    # output.write(str(os.system("whois -h whois.cymru.com '{0}	{1}'".format(ip, date))))
                    output_results = os.popen("whois -h whois.cymru.com '{0}	{1}'".format(ip, date)).readlines()
                    for i in range(len(output_results)):
                        print output_results[i].strip()
                        output.write(output_results[i])

                print '\n'
                output.write('\n')


    output.write('end')
    output.close()


if __name__ == '__main__':
    for vp in VP_LIST:
        # input file
        rawCSV_file = os.path.join(CSV_FILE_DESTDIR, 'comparison_time_{0}.csv'.format(vp))
        print rawCSV_file

        # output file
        locater_vp = os.path.join(CSV_FILE_DESTDIR, 'locators_{0}.txt'.format(vp))
        output_AS_file = os.path.join(CSV_FILE_DESTDIR, 'loc2AS_dynamic_{0}.txt'.format(vp))

        # date wanted to check
        date = '2013-07-10'

        # Call function
        locator_finder_dynamic(rawCSV_file, output_AS_file, date)