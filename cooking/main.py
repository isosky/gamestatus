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
        self.check(x, y)

    def check(self, x, y):
        if self.task_ground[x][y] == 1:
            return True
        else:
            return False


food = {'rice': [[0, 1, 0], [1, 1, 1]]}


def fix_rice(task):
    print('try to fix rice')
    ground = np.zeros((5, 4))
    x = 0
    y = 0
    ground[x][y] = 2
    x += 1
    y += 1
    while not task.moveto(x, y) and x < len(ground) - 1:
        ground[x][y] = 2
        x += 1
    if task.check(x, y):
        ground[x][y] = 1
        task.step -= 1
        x -= 1
        y += 1
        if task.check(x, y):
            ground[x][y] = 1
            task.step -= 1
            x += 1
            ground[x][y] = 1
            task.step -= 1
            y += 1
            ground[x][y] = 1
            task.step -= 1

        else:
            ground[x][y] = 2
            task.step -= 2
            x += 2
            ground[x][y] = 1
            ground[x][y - 1] = 1
            ground[x][y - 2] = 1
            task.step -= 3
    print(ground, 13 - task.step)


if __name__ == "__main__":
    t = task1()
    t.load(food['rice'])
    # print(t.check(0,2))
    fix_rice(t)
