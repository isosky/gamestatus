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
            # if temp[0] in ids:
            if temp[2] == '三阶':
                cookers.append(cookerparser.cookerparser(temp))
    return cookers


def initm():
    km = ['面', '肉', '肉', '肉', '蔬', '蔬', '蔬', '鱼']
    m = {'面': [], '肉': [], '蔬': [], '鱼': []}
    data = xlrd.open_workbook('s.xlsx')
    sheet = data.sheet_by_index(4)
    cols = sheet.ncols
    rows = sheet.nrows
    # print(cols, rows)
    for i in range(1, rows):
        for j in range(1, cols, 2):
            m[km[i - 1]].append(sheet.cell(i, j).value)
    for i in m:
        while '' in m[i]:
            m[i].remove('')
    return m


def initdish():
    dishes = {}
    m = initm()
    data = xlrd.open_workbook('s.xlsx')
    sheet = data.sheet_by_index(1)
    cols = sheet.ncols
    rows = sheet.nrows
    for i in range(2, rows):
        temp = sheet.row(i)
        temp = [x.value for x in temp]
        if temp[1] != '' and temp[7] != '':
            dishes[str(int(temp[0]))] = (dishparser.dishparser(temp, m))
    return dishes


if __name__ == '__main__':
    m = initm()
    for i in m:
        for j in m[i]:
            print(j)
