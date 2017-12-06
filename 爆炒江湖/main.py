#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:35
# @Author  : wtr
# @File    : main.py

import csvreader
import time

# total_time = raw_input('pls input time: ')
total_time = 2.0
total_time = float(total_time) * 3600

# print total_time

# load cookers
cookers = csvreader.initcooker([3, 177])
dishes = csvreader.initdish()

arr = ['chao', 'kao', 'zhu', 'zheng', 'qie', 'zha']

sp = {1: 1.0, 2: 1.1, 3: 1.3, 4: 1.5}


def calcookdish(cooker, dish):
    s = []
    if not dish.cookerid:
        for i in arr:
            if cooker.attr[i] == '' and dish.attr[i] != '':
                # print(i,' not match')
                return
            if cooker.attr[i] != '' and dish.attr[i] != '':
                s.append(int(cooker.attr[i] / dish.attr[i]))
        if s:
            if min(s) > 0:
                if s > 4:
                    s = 4
                    dish.setcooker(cooker, sp[s])
                    cooker.adddish(dish)
                # print dish.earn * sp[s] * dish.total_time
        # else:
        #     print "can't cook this dish"


# print cookers
for c in cookers:
    for i in dishes:
        calcookdish(c, dishes[i])
# calcookdish(cookers[0], dishes['89'])
for c in cookers:
    temp = c.dish
    print c.name, c.attr
    for i in temp:
        print i.id, i.name, i.sp, i.per, i.total_time, i.total_money
