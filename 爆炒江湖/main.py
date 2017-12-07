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
o_cookers = csvreader.initcooker([])
o_dishes = csvreader.initdish()

arr = ['炒', '烤', '煮', '蒸', '切', '炸']

sp = {1: 1.0, 2: 1.1, 3: 1.3, 4: 1.5}

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



# for c in cookers:
#     # if c.id == 177:
#     #     c.addcookware('鱼', 20.0)
#     # for i in dishes:
#     #     calcookdish(c, dishes[i])
#     calcookdish(c, dishes['20'])


def presult():
    for c in cookers:
        c.dish = sorted(c.dish, key=lambda a: a.per, reverse=True)
        temp = c.dish
        if len(temp) > 0:
            print c.name, c.attr, c.ss, c.es
            print 'id', '名称', '倍率', '价格/h', '加成', '时长', '总价', '加成类别'
            for i in temp:
                print i.id, i.name, i.sp, round(i.per, 2)*3600, i.gv, i.total_time, i.total_money, (',').join(i.g)


if __name__ == '__main__':
    while True:
        mode = raw_input('1:查询某个菜哪些厨师可以做\n2:查询某厨师推荐的菜\nplease input value: ')
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
        if mode == '2':
            k = 1
            while k:
                cooker_name = raw_input('请输入厨师名称:')
                for c in cookers:
                    if c.name == cooker_name:
                        for d in dishes:
                            calcookdish(c, dishes[d])
                        k += 1
                        break
                if k == 1:
                    print '名称不存在,请重新输入'
                else:
                    break

        presult()
        print '\n'*3
        del cookers
        del dishes
        cookers = deepcopy(o_cookers)
        dishes = deepcopy(o_dishes)
