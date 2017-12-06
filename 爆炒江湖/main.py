#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:35
# @Author  : wtr
# @File    : main.py

import csvreader
import operator
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# total_time = raw_input('pls input time: ')
total_time = 2.0
total_time = float(total_time) * 3600

# print total_time

# load cookers
cookers = csvreader.initcooker([3, 177])
dishes = csvreader.initdish()

arr = ['炒', '烤', '煮', '蒸', '切', '炸']

sp = {1: 1.0, 2: 1.1, 3: 1.3, 4: 1.5}

m = csvreader.initm()


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


# temp = dishes['1']

# print(temp)


for c in cookers:
    if c.id == 177:
        c.addcookware('鱼', 20.0)
    for i in dishes:
        calcookdish(c, dishes[i])
# calcookdish(cookers[0], dishes['89'])
for c in cookers:
    c.dish = sorted(c.dish, key=lambda a: a.per, reverse=True)
    temp = c.dish
    print c.name, c.attr, c.ss, c.es
    for i in temp:
        print i.id, i.name, i.sp, round(i.per, 2), i.gv, i.total_time, i.total_money,(',').join(i.g)
