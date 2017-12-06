#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:54
# @Author  : wtr
# @File    : cookerparser.py



class cookerparser:
    def __init__(self, row):
        _cooker = {'炒': row[3], '烤': row[4], '煮': row[5], '蒸': row[6],
                   '切': row[7], '炸': row[8]}
        self.id = row[0]
        self.name = row[1]
        self.attr = _cooker
        self.dish = []
        self.es = 0
        self.ev = 0
        temp = row[10].split('%')
        for i in temp:
            if '0' in i or '5' in i:
                ts = i.split('+')
                self.ss = ts[0]
                self.sv = float(ts[1])

    def adddish(self, d):
        if len(self.dish) == 3:
            temp = self.dish
            c = 0
            for i in temp:
                if i.per < d.per:
                    i.clearcooker()
                    self.dish.remove(i)
                    # print(self.dish)
                    break
                else:
                    c += 1
            if c == 3:
                return
        self.dish.append(d)

    def addcookware(self, s, v):
        self.es = s
        self.ev = v

    def removecookware(self):
        self.es = 0
        self.ev = 0
