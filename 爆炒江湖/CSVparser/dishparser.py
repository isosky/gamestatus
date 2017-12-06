#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:59
# @Author  : wtr
# @File    : dishparser.py



class dishparser:
    def __init__(self, row):
        _attr = {'chao': row[9], 'kao': row[10], 'zhu': row[11], 'zheng': row[12], 'qie': row[13], 'zha': row[14]}
        self.id = row[0]
        self.name = row[1]
        self.total_time = row[6]
        self.earn = row[7]
        self.attr = _attr
        self.m1 = row[15]
        self.m2 = row[17]
        self.m3 = row[19]
        self.cooker = False
