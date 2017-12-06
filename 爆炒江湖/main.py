#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:35
# @Author  : wtr
# @File    : main.py

import csvreader

# total_time = raw_input('pls input time: ')
total_time = 2.0
total_time = float(total_time)*3600

# print total_time

# load cookers
cookers = csvreader.initcooker([6])
dishes = csvreader.initdish()

arr = ['chao', 'kao', 'zhu', 'zheng', 'qie', 'zha']

sp = {1: 1.0, 2: 1.1, 3: 1.3, 4: 1.5}


def calcookdish(cooker, dish):
    s = []
    if not dish.cooker:
        for i in arr:
            if cooker.attr[i] != '' and dish.attr[i] != '':
                s.append(int(cooker.attr[i]/dish.attr[i]))
        if s:
            if s > 4:
                s = 4
                cooker.adddish(dish,sp[s])
                print dish.earn*sp[s]*dish.total_time
        else:
            print "can't cook this dish"


# print cookers

calcookdish(cookers[0], dishes['1'])
print cookers[0].dishid
