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
            if lines[LOG_TIME_COLUMN['rloc_set_coherence']] == "False" and "NegativeReply" not in lines[LOG_TIME_COLUMN['round_type_set']]:
                locaters.extend([i.split(",")[0] for i in lines[LOG_TIME_COLUMN['locators_set']].split("#") if i.split(",")[0] not in locaters])
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
            if lines[LOG_TIME_COLUMN['rloc_set_coherence']] == "False" and "NegativeReply" not in lines[LOG_TIME_COLUMN['round_type_set']]:
                count += 1
                print count
                print lines[LOG_TIME_COLUMN['log_file_name']] # print path
                output.write(str(count) + '\n' + lines[LOG_TIME_COLUMN['log_file_name']] + '\n')

                locators = [ j.split('=')[1] for j in [i.split(",")[0] for i in lines[LOG_TIME_COLUMN['locators_set']].split("#")]]
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

def locator_finder_dynamic2(input, output, date):
    output = open(output, 'w+')
    count = 0
    with open(input) as f_handler:
        tmp_locators = []
        ref_eid = ''
        for line in f_handler:
            lines = line.split(";")
            curr_eid = lines[LOG_TIME_COLUMN['eid']]
            curr_locators = lines[LOG_TIME_COLUMN['RLOC_set']:]
            # 最后一个元素会含有换行符，删除之
            curr_locators = [element.strip() for element in curr_locators]
            # print curr_locators
            # print curr_eid, "==", ref_eid, curr_eid == ref_eid
            if curr_eid == ref_eid:
                tmp_locators.extend(curr_locators)

            else:
                "当 当前处理行的eid 与选定的参考eid值不一样的时候，说明已经开始处理新的EID的了" \
                "这个时候 首先需要把以前的EID的对应的locators处理掉"
                tmp_locators = list(set(tmp_locators)) # 去重
                if len(tmp_locators) >= 2:
                    count += 1
                    print count
                    output.write("{0}\nProcessing the associated different RLOC for {1}\n".format(str(count), ref_eid))
                    output.write("Associated Locators ={0}\n".format(";".join(tmp_locators)))
                    for ip in tmp_locators:
                        # os.system("whois -h whois.cymru.com '{0}	{1}' >> {2}".format(ip, date, output_AS_file))
                        # output.write(str(os.system("whois -h whois.cymru.com '{0}	{1}'".format(ip, date))))
                        output_results = os.popen("whois -h whois.cymru.com '{0}	{1}'".format(ip, date)).readlines()
                        for element in output_results:
                            print element.strip()
                            output.write(element.strip())
                # 最后不要忘记了 更新ref_eid 以及清空 tmp_locators
                ref_eid = curr_eid
                tmp_locators = []

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
        # locator_finder_dynamic(rawCSV_file, output_AS_file, date)
        locator_finder_dynamic2(rawCSV_file, output_AS_file, date)