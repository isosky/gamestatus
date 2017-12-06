#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:54
# @Author  : wtr
# @File    : cookerparser.py


class cookerparser:
    def __init__(self, row):
        _cooker = {'chao': row[3], 'kao': row[4], 'zhu': row[5], 'zheng': row[6],
                   'qie': row[7], 'zha': row[8]}
        self.id = row[0]
        self.name = row[1]
        self.attr = _cooker
        self.dishid = []
        self.dishsp = []
        self.dishearns = []
        self.dishtime = []

    def adddish(self, dish, sp):
        if len(self.dishid) == 3:
            pass
        self.dishid = dish.id
        self.dishsp = sp
        self.dishearns = dish.earn
        self.dishtime = dish.total_time
