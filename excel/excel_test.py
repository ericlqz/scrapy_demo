#!/usr/bin python2
# -*- coding:utf-8 -*-
  
import csv

with open('test.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile,quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['a', '1', '1', '2', u'1这是什么'.encode('gb2312')])
    spamwriter.writerow(['b', '3', '3', '6', u'4这是什么'.encode('gb2312')])
    spamwriter.writerow(['c', '7', '7', '1', u'4这是什么'.encode('gb2312')])
    spamwriter.writerow(['d', '11','11','1', u'1这是什么'.encode('gb2312')])
    spamwriter.writerow(['e', '12','12','1', u'3这是什么'.encode('gb2312')])

