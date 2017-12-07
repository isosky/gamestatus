#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-6 16:35
# @Author  : wtr
# @File    : main.py
from copy import deepcopy

import csvreader
import operator
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# total_time = raw_input('pls input time: ')
total_time = 2.0
total_time = float(total_time)*3600

# print total_time

# load cookers
cookers = csvreader.initcooker([])
dishes = csvreader.initdish()

# load save
o_cookers = deepcopy(cookers)
o_dishes = deepcopy(dishes)

arr = ['炒', '烤', '煮', '蒸', '切', '炸']

sp = {1: 1.0, 2: 1.1, 3: 1.3, 4: 1.5}
dp = {1.5: '神', 1.3: '特', 1.1: '优', 1: '可'}

m = csvreader.initm()


def calcookdish(cooker, dish):
    s = []
    # if not dish.cookerid:
    if True:
        for i in arr:
            if cooker.attr[i] == '' and dish.attr[i] != '':
                # print(i,' not match')
                return
            if cooker.attr[i] != '' and dish.attr[i] != '':
                s.append(int(cooker.attr[i]/dish.attr[i]))
        t = min(s)
        if t > 0:
            if t > 4:
                t = 4
            dish.setcooker(cooker, sp[t])
            cooker.adddish(dish)
            # print dish.id,dish.per
            # tempd(cooker)


def tempd(c):
    temp = c.dish
    dic = {}
    for i in temp:
        dic[i.id] = i.per
    print dic


def presult():
    for c in cookers:
        c.dish = sorted(c.dish, key=lambda a: a.per, reverse=True)
        c.dish = [x for x in c.dish if x.per > 1.74]
        temp = c.dish
        if len(temp) > 0:
            print c.id, c.name, c.attr, c.ss, c.es
            print 'id', '名称', '倍率', '价格/h', '加成', '时长', '总价', '加成类别'
            for i in temp:
                print i.id, i.name, i.sp, dp[i.sp], round(i.per, 2), i.gv, i.total_time, i.total_money, (',').join(i.g)
            print '\n'*2



if __name__ == '__main__':
    while True:
        mode = raw_input('1:查询某个菜哪些厨师可以做\n2:查询某厨师推荐的菜\nplease input value: ')
        # mode = '2'
        if mode == '1':
            k = 1
            while k:
                dish_name = raw_input('请输入菜名:')
                for d in dishes:
                    if dishes[d].name == dish_name:
                        for c in cookers:
                            calcookdish(c, dishes[d])
                        k += 1
                        break
                if k == 1:
                    print '名称不存在,请重新输入'
                else:
                    break
            presult()

        if mode == '2':
            k = 1
            while k:
                cooker_name = raw_input('请输入厨师名称:')
                # cooker_name = '大天狗'
                for c in cookers:
                    if c.name == cooker_name:
                        if cooker_name == '大天狗':
                            c.addcookware('鱼', 20.0)
                        for d in dishes:
                            calcookdish(c, dishes[d])
                        k += 1
                        break
                if k == 1:
                    print '名称不存在,请重新输入'
                else:
                    break
            presult()

        if mode == '3':
            for c in cookers:
                for d in dishes:
                    calcookdish(c, dishes[d])
                presult()
                del dishes
                dishes = deepcopy(o_dishes)
