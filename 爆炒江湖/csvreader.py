#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:49
# @Author  : wtr
# @File    : csvreader.py

import xlrd
from CSVparser import cookerparser, dishparser


def initcooker(ids):
    cookers = []
    data = xlrd.open_workbook('s.xlsx')
    sheet = data.sheet_by_index(3)
    cols = sheet.ncols
    rows = sheet.nrows
    for i in range(1, rows):
        temp = sheet.row(i)
        temp = [x.value for x in temp]
        if temp[1] != '':
            if temp[0] in ids:
                cookers.append(cookerparser.cookerparser(temp))
    return cookers


def initdish():
    dishes = {}
    data = xlrd.open_workbook('s.xlsx')
    sheet = data.sheet_by_index(1)
    cols = sheet.ncols
    rows = sheet.nrows
    for i in range(2, rows):
        temp = sheet.row(i)
        temp = [x.value for x in temp]
        if temp[1] != '' and temp[7] != '':
            dishes[str(int(temp[0]))] = (dishparser.dishparser(temp))
    return dishes
