#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:59
# @Author  : wtr
# @File    : dishparser.py


class dishparser:
    def __init__(self, row, m):
        self.total_money = 0
        self.sp = 0
        self.per = 0
        self.gv = 0
        _attr = {'炒': row[9], '烤': row[10], '煮': row[11], '蒸': row[12], '切': row[13], '炸': row[14]}
        self.id = row[0]
        self.name = row[1]
        self.total_time = row[6]
        self.earn = row[7]
        self.attr = _attr
        self.g = []
        self.m1 = row[15]
        self.m2 = row[17]
        self.m3 = row[19]
        for i in m.keys():
            if self.m1 != '' and self.m1 in m[i]:
                self.g.append(i)
            if self.m2 != '' and self.m2 in m[i]:
                self.g.append(i)
            if self.m3 != '' and self.m3 in m[i]:
                self.g.append(i)
        for i in _attr.keys():
            if _attr[i] != '':
                self.g.append(i)
        self.g = list(set(self.g))

        self.cookerid = False

    def __repr__(self):
        return repr((self.id, self.total_time, self.per))

    def setcooker(self, cooker, sp):
        self.cookerid = cooker.id
        self.sp = sp
        if cooker.ss in self.g:
            sp += cooker.sv/100
        if cooker.es in self.g:
            sp += cooker.ev/100
        self.gv = sp
        self.per = self.gv*self.earn
        self.total_money = self.gv*self.earn*self.total_time

    def clearcooker(self):
        self.cookerid = False
        self.sp = 0
        self.gv = 0
        self.per = 0
        self.total_money = 0
