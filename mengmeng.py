__author__ = 'yueli'
# -*- coding: utf-8 -*-
import math
from netaddr import *

def initData():
   fs = open("log_mengmeng","r")
   # get data list
   datalist = []
   for line in fs.readlines():
       eles = line.split(',')
       for ele in eles:
           datalist.append(ele.strip()[1:-1].strip())
   fs.close()
   return datalist

def findContinous(datalist):
   result = []
   prefix = 0
   temp = [datalist[0]]

   for data in datalist:
       eles = data.split('/')
       ip = eles[0]
       mask = eles[1]
       num = iptoBinary(ip)
       newprefix = num >> (32-int(mask))
       #print data,num,newprefix
       if newprefix == prefix+1:
           temp.append(data)
       else:
           if len(temp) > 1:
               result.append(temp)
           temp = [data]
       prefix = newprefix

   if len(temp) > 1:
       result.append(temp)

   return result


def iptoBinary(address):
   result = 0
   eles = address.split('.')
   result += int(eles[0]) << 24
   result += int(eles[1]) << 16
   result += int(eles[2]) << 8
   result += int(eles[3])

   return result

def findInclude(datalist):
   result = []
   last = 1
   lastmask = 32
   temp = [datalist[0]]

   for data in datalist:
       eles = data.split('/')
       ip = eles[0]
       mask = eles[1]
       num = iptoBinary(ip)
       if num ^ last < pow(2,32-int(lastmask)):
           temp.append(data)
       else:
           if len(temp) > 1:
               result.append(temp)
           temp = [data]
           lastmask = mask
       last = num

   if len(temp) > 1:
       result.append(temp)

   return result


if __name__ == "__main__":
   datalist = initData()
   res1 = findContinous(datalist)
   print "results for continous subnets:"
   for g in res1:
       print g
   res2 = findInclude(datalist)
   print "results for included subnets:"
   for g in res2:
       print g