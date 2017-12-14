#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-10-24 17:06
# @Author  : wtr
# @File    : tsservice.py


import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import json
from tornado.options import define, options
from transfergps import GlobalMercator
from config import temp_path_road,dbc

define("port", default=5764, help="run on the given port", type=int)
tornado.options.parse_command_line()


# websocket
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        return True

    def open(self):
        WebSocketHandler.waiters.add(self)
        print 'open'
        print self.waiters

    def on_close(self):
        WebSocketHandler.waiters.remove(self)

    @classmethod
    def pushdata(cls, message, app):
        data = json.dumps({'data': loaddata()})
        for i in cls.waiters:
            if i == app:
                if message == 'oneroad':
                    data = json.dumps({'data': newdata()})
                i.write_message(data)

    def on_message(self, message):
        WebSocketHandler.pushdata(message, self)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ts', WebSocketHandler)
        ]

        settings = {"template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)


gm = GlobalMercator()


def calpolygon(pt1, pt2):
    if pt1 == pt2:
        return False
    x1, y1 = gm.LatLonToMeters(pt1[1], pt1[0])
    x2, y2 = gm.LatLonToMeters(pt2[1], pt2[0])
    if y1 == y2:
        p1 = gm.MetersToLatLon(x1, y1 + 7)
        p2 = gm.MetersToLatLon(x1, y1 - 7)
        p3 = gm.MetersToLatLon(x2, y2 - 7)
        p4 = gm.MetersToLatLon(x2, y2 + 7)
    elif x1 == x2:
        p1 = gm.MetersToLatLon(x1 - 7, y1)
        p2 = gm.MetersToLatLon(x1 + 7, y1)
        p3 = gm.MetersToLatLon(x2 + 7, y2)
        p4 = gm.MetersToLatLon(x2 - 7, y2)
    else:
        k_self = float(y1 - y2)/float(x1 - x2)
        k_vector = -1/k_self
        d = [1, k_vector]
        length_of_dv = pow((1 + pow(k_vector, 2)), 0.5)
        d = [x/length_of_dv*7 for x in d]
        p1 = gm.MetersToLatLon(x1 + d[0], y1 + d[1])
        p2 = gm.MetersToLatLon(x1 - d[0], y1 - d[1])
        p3 = gm.MetersToLatLon(x2 - d[0], y2 - d[1])
        p4 = gm.MetersToLatLon(x2 + d[0], y2 + d[1])
    return [[p1[1], p1[0]], [p2[1], p2[0]], [p3[1], p3[0]], [p4[1], p4[0]]]


def loaddata():
    with open('temp/3d/20171018111500.json', 'r') as f:
        temp = json.loads(f.read())
        res = []
        for i in temp[0:3]:
            # for i in temp:
            color = i['color'].split(',')[:-1]
            color = '#' + ''.join([str.upper(hex(int(x))[2:4]) for x in color])
            pts = i['pts']
            for index in range(len(pts) - 1):
                polygon = calpolygon(pts[index], pts[index + 1])
                if polygon:
                    res.append([polygon, color, pts[index], pts[index + 1]])
    return res


def newdata():
    with open(temp_path_road + '/sboy.json', 'r') as f:
        temp = json.loads(f.read())
    surface = temp['surface']
    print len(surface['indices']),len(surface['vertices'])
    data = {'indices': surface['indices'], 'vertices': surface['vertices']}
    return data


def getsegment():
    db = dbc(True)
    sql = 'select * from segment'
    db.cur.execute(sql)
    temp = db.cur.fetchall()
    for i in temp:
        # if i[0]=='lane-f242d953-78f6-4229-8e37-e3298284fcb9':
        with open('test.json','w') as f:
            f.write(json.dumps(i[1]))
        break

if __name__ == '__main__':
    # application = Application()
    # server = tornado.httpserver.HTTPServer(application)
    # server.listen(options.port)
    # tornado.ioloop.IOLoop.instance().start()
    # loaddata()
    # newdata()
    getsegment()