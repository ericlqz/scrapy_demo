#!/usr/bin/python2
# -*- coding:utf-8 -*-

import xlrd


class ExcelReader:

    filename = 'data/pre_data/chengdu_multi_address_favorites_remove_useless.xlsx'

    def readColumn(self, index):

        result = []
        data = xlrd.open_workbook(self.filename)
        sheet = data.sheet_by_index(0)
        rowCount = sheet.nrows
        colCount = sheet.ncols
        print 'row: ' + str(rowCount) + ' col: ' + str(colCount)

        for i in range(1, rowCount):
            rowValues = sheet.row_values(i)
            for index in range(2, colCount):
                if len(rowValues[index]) == 0:
                    break
            rowValues = rowValues[1:index]
            result.append(rowValues)

        print result
        #column = sheet.col_values(index)
        #column = column[1:]
        #print 'Column ' + str(index) + ' len ' + str(len(column)) + ' ' + ','.join(column)

reader = ExcelReader()
reader.readColumn(1)

