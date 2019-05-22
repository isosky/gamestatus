#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-3-21 9:40
# @Author  : wtr
# @File    : main.py

import random
import numpy as np


class task1():

    def __init__(self):
        self.task_ground = np.zeros((5, 4))
        self.fix_ground = np.zeros((5, 4))
        self.step = 13

    def load(self, shape):
        x = random.randint(0, 4 - len(shape[0]))
        y = random.randint(0, 5 - len(shape))
        if x == 0 and y == 0:
            self.load(shape)
            return
        # x = 0
        # y = 2
        print(x, y)
        for new in shape:
            # print(new, x, y)
            self.task_ground[y][x:x + len(new)] = new
            y += 1
        print(self.task_ground)

    def moveto(self, x, y):
        self.step -= 1
        return x, y

    def check(self, x, y):
        if self.task_ground[x][y] == 1:
            return True
        else:
            return False


food = {'rice': [[0, 1, 0], [1, 1, 1]],
        'flour': [[1, 1, 1]],
        'egg': [[1, 1], [1, 1]]}


def fix(fn, t):
    if fn == 'rise':
        fix_rice(fn, t)
    if fn == 'flour':
        fix_flour(fn, t)
    if fn == 'egg':
        fix_egg(fn, t)


def init_task1(name, task):
    print('try to fix %s'%name)
    ground = np.zeros((5, 4))
    x = 0
    y = 0
    ground[x][y] = 2
    ground[x][y] = 2
    x, y = task.moveto(x + 1, y + 1)
    return ground, x, y


def fix_rice(fn, task):
    ground, x, y = init_task1(fn, task)
    while not task.check(x, y) and x < len(ground) - 1:
        ground[x][y] = 2
        x, y = task.moveto(x + 1, y)
    ground[x][y] = 1
    x, y = task.moveto(x - 1, y + 1)
    if task.check(x, y):
        ground[x][y] = 1
        x, y = task.moveto(x + 1, y)
        ground[x][y] = 1
        x, y = task.moveto(x, y + 1)
        ground[x][y] = 1

    else:
        ground[x][y] = 2
        x, y = task.moveto(x + 1, y)
        ground[x][y] = 2
        x, y = task.moveto(x + 1, y)
        ground[x][y] = 1
        x, y = task.moveto(x, y - 1)
        ground[x][y] = 1
        x, y = task.moveto(x, y - 1)
        ground[x][y] = 1
    print(ground, 'use step:' + str(13 - task.step))


def fix_flour(fn, task):
    ground, x, y = init_task1(fn, task)
    while not task.check(x, y) and x < len(ground) - 1:
        ground[x][y] = 2
        x, y = task.moveto(x + 1, y)
    ground[x][y] = 1
    if x == 0:
        x, y = task.moveto(x, y + 1)
        ground[x, y] = 1
        x, y = task.moveto(x, y + 1)
        ground[x, y] = 1
        print(ground, 'use step:' + str(13 - task.step))
        return
    x, y = task.moveto(x, y - 1)
    if task.check(x, y):
        ground[x, y] = 1
        x, y = task.moveto(x, y + 1)
        x, y = task.moveto(x, y + 1)
        ground[x, y] = 1
    else:
        ground[x, y] = 2
        x, y = task.moveto(x, y + 1)
        x, y = task.moveto(x, y + 1)
        ground[x, y] = 1
        x, y = task.moveto(x, y + 1)
        ground[x, y] = 1
    print(ground, 'use step:' + str(13 - task.step))


def fix_egg(fn, task):
    ground, x, y = init_task1(fn, task)


if __name__ == "__main__":
    t = task1()
    t.load(food['egg'])
    fix('egg', t)
    # print(t.check(0,2))
    # fix_rice(t)
