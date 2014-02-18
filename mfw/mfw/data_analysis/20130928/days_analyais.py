#!/usr/bin/python2
# -*- coding:utf-8 -*-

import csv
import sqlite3
import string
import re

class DaysAnalysis:
    filename = 'data.sqlite'

    first_line = [u'游记ID',u'标题',u'链接',u'规则1',u'规则2']
    def analysis(self):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        data = cursor.execute('select * from post')

        with open('post_day.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile,dialect='excel')
            spamwriter.writerow(self.encode_sequence(self.first_line))
            for line in data:
                spamwriter.writerow(self.days_analysis(line))

    def days_analysis(self, line):
        rule1 = ur'(?<!第)[一二三四五六七八九十\d]+\s*[天|日|days|day]+'
        rule2 = ur'(第[一二三四五六七八九十\d]+\s*[天|日]|day\s*\d+)'

        nline =[]
        nline.append(self.encode(line[0]))
        nline.append(self.encode(line[2]))
        url = self.encode('http://www.mafengwo.cn/i/' + line[0] + '.html')
        nline.append(url)

        rule1_days = self.apply_rule(rule1, line)
        if rule1_days:
            nline.append(self.encode('|'.join(rule1_days)))
        else:
            nline.append(self.encode(u'无'))
        
        rule2_days = self.apply_rule(rule2, line)
        if rule2_days:
            nline.append(self.encode('|'.join(rule2_days)))
        else:
            nline.append(self.encode(u'无'))

        if not (rule1_days or rule2_days):
           print url

        return nline
        # print ','.join(nline)

    def apply_rule(self, rule, line):
        interval = 20

        content = line[-1].replace(' ','')
        days = []
        for match in re.finditer(rule, content.lower()):
            start = match.start()-interval if match.start()>interval else 0
            end = match.end()+interval if match.end()+interval<len(content) else len(content)
            days.append(match.group()+'('+content[start:end]+')')
        return days

    def encode_sequence(self, line):
        nline = []
        for p in line:
            nline.append(p.encode('utf-8'))
        return nline

    def encode(self, s):
        return s.encode('utf-8')
    
analyser = DaysAnalysis()
analyser.analysis()
