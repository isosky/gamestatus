# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 17:42:33 2016

@author: wtr
"""

import math

"""
 第一个参数为一个路的起点和终点组成的list,如下:
 sp=[116.291087273989,40.0484742339865]
 ep=[116.292488728211,40.0487113818083]
 lines=[sp,ep]
 第二个参数为前进了多少的百分比
"""


def line_interpolate_point(lines, percent):
    p1, p2 = lines
    # 如果传进来的数大于1
    if percent > 1:
        return 'false'
    # 如果第2个参数为0或者1
    if percent == 0:
        return p1
    if percent == 1:
        return p2
    # 计算
    return [(p2[0] - p1[0])*percent + p1[0], (p2[1] - p1[1])*percent + p1[1]]


#############################################################
def getDistance(start, end):
    if start == end:
        return 0
    else:
        lat1 = (math.pi/180)*start[1]
        lat2 = (math.pi/180)*end[1]
        lon1 = (math.pi/180)*start[0]
        lon2 = (math.pi/180)*end[0]
        # 地球半径
        R = 6371
        try:
            d = math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2 - lon1))*R
        except:
            print start, end
            return 0
        return d*1000


############################################################
'''已知点A经纬度，根据B点据A点的距离，和方位，求B点的经纬度
   para a 已知点a
   para distance b到a的距离
   para angle b相对于a的方位
   return b的经纬度坐标
'''


############################################################
def getJWD(a, distance, angle):
    Rc = 6378137  # 赤道半径
    Rj = 6356725  # 极半径
    dx = distance*math.sin(angle*math.pi/180)
    dy = distance*math.cos(angle*math.pi/180)
    alon = float(a[0])
    alat = float(a[1])
    a_radlo = alon*math.pi/180
    a_radla = alat*math.pi/180
    Ec = Rj + (Rc - Rj)*(90 - alat)/90
    Ed = Ec*math.cos(a_radla)
    blon = (dx/Ed + a_radlo)*180/math.pi
    blat = (dy/Ec + a_radla)*180/math.pi
    return [blon, blat]


"""
算点到直线的投影
"""


# 经度是x,纬度是y
def getclosedpoint(sp, ep, pt):
    # 如果纬度相同,返回线外点的经度,线上的纬度
    if sp[1] == ep[1]:
        return [pt[0], sp[1]]
    # 如果经度相同,返回线外点的纬度,线上的经度
    if sp[0] == ep[0]:
        return [sp[0], pt[1]]
    # http://blog.csdn.net/luols/article/details/7482626
    k = (sp[1] - ep[1])/(sp[0] - ep[0])
    x = float((k*sp[0] + pt[0]/k + pt[1] - sp[1])/(1/k + k))
    y = float(-1/k*(x - pt[0]) + pt[1])
    return [x, y]


"""
算点到直线距离
"""


def getdistance_pl_l(line, pt):
    return getdistance_pl(line[0], line[1], pt)


# 点到直线距离
def getdistance_pl(sp, ep, pt):
    pro = getclosedpoint(sp, ep, pt)
    return getDistance(pro, pt)


def by_wtr():
    sp = [15, 20]
    ep = [20, 20]
    pt = [25, 25]
    res = getclosedpoint(sp, ep, pt)
    print res


def CalAngle(point1, point2):
    diff_x = float(point2[0]) - float(point1[0])
    diff_y = float(point2[1]) - float(point1[1])
    if diff_x >= 0:
        return 0.5*math.pi - math.atan(diff_y/diff_x)
    else:
        return 1.5*math.pi - math.atan(diff_y/diff_x)


def linerecins(lsp, lep, recpt1, recpt2):
    rect = {'l': min(recpt1[0], recpt2[0]), 'r': max(recpt1[0], recpt2[0]), 'b': min(recpt1[1], recpt2[1]),
            't': max(recpt1[1], recpt2[1])}
    a = lsp[1] - lep[1]
    b = lep[0] - lsp[0]
    c = lsp[0]*lep[1] - lep[0]*lsp[1]
    if ((a*rect['l'] + b*rect['t'] + c >= 0 and a*rect['r'] + b*rect['b'] + c <= 0) or
            (a*rect['l'] + b*rect['t'] + c <= 0 and a*rect['r'] + b*rect['b'] + c >= 0) or
            (a*rect['l'] + b*rect['b'] + c >= 0 and a*rect['r'] + b*rect['t'] + c <= 0) or
            (a*rect['l'] + b*rect['b'] + c >= 0 and a*rect['r'] + b*rect['t'] + c <= 0)):
        if ((lsp[0] < rect['l'] and lep[0] < rect['l']) or
                (lsp[0] > rect['r'] and lep[0] > rect['r']) or
                (lsp[1] > rect['t'] and lep[1] > rect['t']) or
                (lsp[1] < rect['b'] and lep[1] < rect['b'])):
            return False
        else:
            return True
    else:
        return False


if __name__ == '__main__':
    by_wtr()
