#!/usr/bin/python2
# -*- coding:utf-8 -*-

import xlrd
import csv
import sqlite3
import string


class FavoriteAnalysis:

    favFileName = 'data/pre_data/chengdu_favorites.xlsx'
    postFileName = 'data/pre_data/data.sqlite'

    resultFavFlagFile = 'data/result/post.csv'
    resultFavNoneFile = 'data/result/only_content_zero.txt'

    favorites = []

    def readFavorites(self):

        data = xlrd.open_workbook(self.favFileName)
        favNameIndex = 1
        sheet = data.sheet_by_index(0)
        column = sheet.col_values(favNameIndex)
        column = column[1:]
        #print 'Column ' + str(index) + ' len ' + str(len(column)) + ' ' + ','.join(column)
        return column

    def getFirstLine(self):

        firstLine = [u'游记ID', u'用户ID', u'标题', u'作者', u'链接']
        #firstLine.extend(self.readFavorites())
        self.favorites.extend(self.readFavorites())
        firstLine.extend(self.favorites)
        firstLine.append(u'内容')
        return firstLine

    def analysis(self):
        conn = sqlite3.connect(self.postFileName)
        cursor = conn.cursor()
        data = cursor.execute('select * from post')

        zerofile = open(self.resultFavNoneFile, 'w+')

        with open(self.resultFavFlagFile, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            spamwriter.writerow(self.encode_sequence(self.getFirstLine()))
            for line in data:
                spamwriter.writerow(self.data_process(line, zerofile))

        zerofile.close()

    def encode_sequence(self, line):
        nline = []
        for p in line:
            nline.append(p.encode('utf-8'))
        return nline

    def encode(self, s):
        return s.encode('utf-8')

    def data_process(self, line, zerofile):
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
                break
        else:
            #file = open(self.resultFavNoneFile, 'a')
            zerofile.write(nline[4] + '\n')
            #file.close()
            #print nline[4]
            print ','.join(nline[5:68])

        size = 500
        nline.extend(self.group(content, size))

        return nline

    def group(self, seq, size):
        while seq:
            frag = '\"' + seq[:size] + '\"'
            yield frag.encode('utf-8')
            seq = seq[size:]


analyser = FavoriteAnalysis()
#line = analyser.getFirstLine()
#print ','.join(line)
analyser.analysis()
