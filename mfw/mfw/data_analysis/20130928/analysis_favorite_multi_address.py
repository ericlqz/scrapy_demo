#!/usr/bin/python2
# -*- coding:utf-8 -*-

import xlrd
import csv
import sqlite3
import string


class FavoriteAnalysis:

    #favFileName = 'data/pre_data/chengdu_multi_address_favorites_remove_useless.xlsx'
    favFileName = 'data/pre_data/chengdu_favorites.xlsx'
    postFileName = 'data/pre_data/data.sqlite'

    resultFavFlagFile = 'data/result/post.csv'
    resultFavNoneFile = 'data/result/only_content_zero.txt'

    favorites = []

    def readFavorites(self):

        data = xlrd.open_workbook(self.favFileName)

        result = []
        sheet = data.sheet_by_index(0)
        rowCount = sheet.nrows
        colCount = sheet.ncols
        #print 'row: ' + str(rowCount) + ' col: ' + str(colCount)

        for i in range(1, rowCount):
            rowValues = sheet.row_values(i)
            end = 2
            for index in range(2, colCount):
                if len(rowValues[index]) == 0:
                    break
                else:
                    end = end + 1
            #rowValues = rowValues[1:index]
            rowValues = rowValues[1:end]
            result.append(rowValues)

        self.favorites.extend(result)

    def favoritesToFirstLine(self):

        self.readFavorites()

        firstLineFavs = []
        for fav in self.favorites:
            #print 'fav', fav
            if len(fav) == 1:
                firstLineFavs.append(fav[0])
            elif len(fav) == 2:
                firstLineFavs.append(fav[0]+'('+fav[1]+')')
            elif len(fav) == 3:
                firstLineFavs.append(fav[0]+'('+fav[1]+',' + fav[2] +')')
        return firstLineFavs


    def getFirstLine(self):

        firstLine = [u'游记ID', u'用户ID', u'标题', u'作者', u'链接']
        favTitle = self.favoritesToFirstLine()
        firstLine.extend(favTitle)
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
        for fav in self.favorites:
            # if f in content or f in title:
            exists = False
            for f in fav:
                if f == u'黄龙':
                    temp = content[0:-1]
                    temp = temp.replace(u'黄龙溪', u'huanglongxi')
                    if f in temp:
                        nline.append(self.encode('1'))
                        exists = True
                        print self.encode(temp)
                        break
                else:
                    if f in content:
                        nline.append(self.encode('1'))
                        exists = True
                        break
            if not exists:
                nline.append(self.encode('0'))

            #if f in content:
            #    nline.append(self.encode('1'))
            #else:
            #    nline.append(self.encode('0'))

        print ','.join(nline[5 : 5 + len(self.favorites)])

        for i in range(5, 5 + len(self.favorites)):
            if 1 == string.atoi(nline[i]):
                break
        else:
            zerofile.write(nline[4] + '\n')
            #print nline[4]
            #print ','.join(nline[5:68])

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
