#!/usr/bin/python2
# -*- coding:utf-8 -*-

import csv
import sqlite3
import string

class Convert:
    filename = 'data.sqlite'
    first_line = [u'游记ID',u'用户ID',u'标题',u'作者',u'链接',
        u'锦里', u'熊猫基地', u'武候祠', u'文殊院', u'青城山', u'金沙遗址', u'杜甫草堂',
        u'青羊宫', u'都江堰', u'春熙路', u'四川大学', u'天府广场', u'望江楼', u'洛带',
        u'宽窄巷子', u'井巷子', u'四川博物馆', u'市博物馆', u'川剧艺术陈列馆', u'科技馆', u'黄龙溪',
        u'西岭雪山', u'石象湖', u'九眼桥', u'文殊坊', u'人民公园', u'百花潭', u'三圣花乡',
        u'永陵', u'浣花溪', u'琴台路', u'东区音乐公园', u'张家巷天主堂', u'动物园', u'文化公园',
        u'合江亭', u'宝光寺', u'海洋世界', u'天台山', u'刘氏庄园', u'街子古镇',
        u'朝阳湖', u'平乐古镇', u'塔子山', u'石象湖', u'龙泉驿', u'回龙沟', u'白鹿',
        u'龙门山', u'安仁古镇', u'太平镇', u'九峰山', u'卧龙', u'九寨沟', u'黄龙',
        u'峨眉', u'乐山', u'重庆', u'西藏', u'汶川', u'雅安', u'泸沽湖',u'丽江',
        u'内容'
    ]

    favorites = [
        u'锦里', u'熊猫基地', u'武候祠', u'文殊院', u'青城山', u'金沙遗址', u'杜甫草堂',
        u'青羊宫', u'都江堰', u'春熙路', u'四川大学', u'天府广场', u'望江楼', u'洛带',
        u'宽窄巷子', u'井巷子', u'四川博物馆', u'市博物馆', u'川剧艺术陈列馆', u'科技馆', u'黄龙溪',
        u'西岭雪山', u'石象湖', u'九眼桥', u'文殊坊', u'人民公园', u'百花潭', u'三圣花乡',
        u'永陵', u'浣花溪', u'琴台路', u'东区音乐公园', u'张家巷天主堂', u'动物园', u'文化公园',
        u'合江亭', u'宝光寺', u'海洋世界', u'天台山', u'刘氏庄园', u'街子古镇',
        u'朝阳湖', u'平乐古镇', u'塔子山', u'石象湖', u'龙泉驿', u'回龙沟', u'白鹿',
        u'龙门山', u'安仁古镇', u'太平镇', u'九峰山', u'卧龙', u'九寨沟', u'黄龙',
        u'峨眉', u'乐山', u'重庆', u'西藏', u'汶川', u'雅安', u'泸沽湖', u'丽江'
    ]

    #favorites = [
        #u'锦里', u'熊猫基地', u'武侯祠', u'文殊院', u'青城山', u'金沙遗址', u'杜甫草堂',
        #u'青羊宫', u'都江堰', u'春熙路', u'四川大学', u'天府广场', u'望江楼', u'洛带',
        #u'宽窄巷子', u'井巷子', u'四川博物院', u'市博物馆', u'川剧艺术陈列馆', u'科技馆',
        #u'黄龙溪', u'西岭雪山', u'石象湖', u'九眼桥', u'文殊坊', u'人民公园', u'百花潭',
        #u'三圣花乡', u'永陵', u'浣花溪', u'琴台路', u'东区音乐公园', u'张家巷天主堂',
        #u'动物园', u'文化公园', u'合江亭', u'宝光寺', u'海洋世界', u'天台山', u'刘氏庄园',
        #u'街子古镇', u'朝阳湖', u'平乐古镇', u'塔子山', u'石象湖', u'龙泉驿'u'回龙沟',
        #u'白鹿', u'龙门山', u'安仁古镇', u'太平镇', u'九峰山', u'卧龙', u'九寨沟', u'黄龙',
        #u'峨眉', u'乐山', u'重庆', u'西藏', u'汶川', u'雅安', u'泸沽湖', u'丽江',
    #]

    def convert(self):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        data = cursor.execute('select * from post')
        with open('post.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile,dialect='excel')
            spamwriter.writerow(self.encode_sequence(self.first_line))
            for line in data:
                spamwriter.writerow(self.data_process(line))

    def encode_sequence(self, line):
        nline = []
        for p in line:
            nline.append(p.encode('utf-8'))
        return nline

    def encode(self, s):
        return s.encode('utf-8')

    def data_process(self, line):
        nline = []

        for i in range(0,4):
            nline.append(self.encode(line[i]))

        nline.append(self.encode('http://www.mafengwo.cn/i/' + line[0] + '.html'))

        content = line[-1].replace(' ','')
        title = line[2].replace(' ','')
        for f in self.favorites:
            # if f in content or f in title:
            if f in content:
                nline.append(self.encode('1'))
            else:
                nline.append(self.encode('0'))

        for i in range(5, 68):
            if 1 == string.atoi(nline[i]):
                break;
        else:
            print nline[4]

        size = 500
        nline.extend(self.group(content, size))

        return nline

    def group(self, seq, size):
        while seq:
            frag = '\"' + seq[:size] + '\"'
            yield frag.encode('utf-8')
            seq = seq[size:]

    #def days_analysis(self, line):
        #rule1 = ur'[一二三四五六七八九十\d]+\s*[天|日|days|day]+'
        #rule2 = ur'(第[一二三四五六七八九十\d]+\s*[天|日]|day\s*\d+)'
        #interval = 5
        #test_rule1(rule1, line)

    #def test_rule(self, rule, line):
        #print '\ntest_rule'
        #print 'source:', line
        #for match in re.finditer(self.rule, line.lower()):
            #print 'start:', match.start()
            #print 'end:', match.end()
            #start = match.start()-self.interval if match.start()>self.interval else 0
            #end = match.end()+self.interval if match.end()+self.interval<len(line) else len(line)
            #print 'group:', match.group()
    #        print 'statement:', match.group()+'('+line[start:end]+')'



converter = Convert()
converter.convert()
