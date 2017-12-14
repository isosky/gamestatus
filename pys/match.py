#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-13 12:00
# @Author  : wtr
# @File    : match.py

from config import ts_path, bounds, arrTrafficStyles, temp_path_2d, temp_path_3d, dbc
import json
from gisfuncs import CalAngle
from gisfuncs import linerecins as lri
from gisfuncs import getdistance_pl_l as gpl
import math


def loadjson():
    ts = 20171212101811
    with open(temp_path_3d + '/' + str(ts) + '.json', 'r') as f:
        data = json.loads(f.read())


def loaddata(tbname):
    db = dbc(True)
    db.cur.execute("SELECT uid ,info FROM " + tbname)
    temp = db.cur.fetchall()
    segs = []
    for i in temp:
        # segs[i[0]] = i[1]['path']
        for j in range(len(i[1]['path']) - 1):
            # print(i[1]['path'])
            segs.append([i[0], i[1]['path'][j][0], i[1]['path'][j][1], i[1]['path'][j + 1][0], i[1]['path'][j + 1][1],
                         CalAngle(i[1]['path'][j], i[1]['path'][j + 1])/math.pi*180])
    return segs


def savedata(segs, tbname):
    db = dbc(False)
    for i in segs:
        sql = "INSERT into %s VALUES ('%s','%s','%s','%s','%s','%s')"%(tbname, i[0], i[1], i[2], i[3], i[4], i[5],)
        # print(sql)
        db.cur.execute(sql)
    db.conn.commit()


def matchuuid():
    db = dbc(False)
    # load links
    links = {}
    sql = "SELECT * FROM links"
    db.cur.execute(sql)
    temp = db.cur.fetchall()
    for i in temp:
        links[i[0]] = {'pt1_lon': float(i[1]), 'pt1_lat': float(i[2]), 'pt2_lon': float(i[3]), 'pt2_lat': float(i[4]),
                       'angle': float(i[5])}

    # load segmets
    segmets = {}
    sql = "SELECT * FROM segments"
    db.cur.execute(sql)
    temp = db.cur.fetchall()
    for i in temp:
        segmets[i[0]] = {'pt1_lon': float(i[1]), 'pt1_lat': float(i[2]), 'pt2_lon': float(i[3]), 'pt2_lat': float(i[4]),
                         'angle': float(i[5])}

    # load segmets
    bdts = {}
    sql = "SELECT hash,pt1_lon,pt1_lat,pt2_lon,pt2_lat,angle FROM bdts;"
    db.cur.execute(sql)
    temp = db.cur.fetchall()
    for i in temp:
        bdts[i[0]] = {'pt1_lon': float(i[1]), 'pt1_lat': float(i[2]), 'pt2_lon': float(i[3]), 'pt2_lat': float(i[4]),
                      'angle': float(i[5])}

    # try first
    for i in segmets.keys():
        print(i)
        temp = segmets[i]
        for bdr in bdts:
            # if bdr ==  -2078938823:
            #     print('aa')
            if abs(bdts[bdr]['angle'] - temp['angle']) < 10:
                lpt1 = [temp['pt1_lon'], temp['pt1_lat']]
                lpt2 = [temp['pt2_lon'], temp['pt2_lat']]
                rpt1 = [bdts[bdr]['pt1_lon'], bdts[bdr]['pt1_lat']]
                rpt2 = [bdts[bdr]['pt2_lon'], bdts[bdr]['pt2_lat']]
                if lri(rpt1, rpt2, lpt1, lpt2):
                    print(bdr)
                if gpl([rpt1, rpt2], lpt1) < 5 and gpl([rpt1, rpt2], lpt2) < 5 and gpl([lpt1, lpt2],
                                                                                       rpt1) < 5 and gpl(
                    [lpt1, lpt2], rpt2) < 5:
                    print(bdr)


if __name__ == '__main__':
    # transfer data
    # s = loaddata('segment')
    # savedata(s, 'segments')
    # s = loaddata('link')
    # savedata(s, 'links')
    # try to match :>
    matchuuid()
