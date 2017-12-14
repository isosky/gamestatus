#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-10-16 10:05
# @Author  : wtr
# @File    : tts_bd.py


from transfergps import *
import urllib2
import os
from PIL import Image, ImageDraw
from coordinatetransform import BDtoWGS
import time
import json
from config import ts_path, bounds, arrTrafficStyles, temp_path_2d, temp_path_3d, dbc
from gisfuncs import CalAngle

# download
# http://its.map.baidu.com:8002/traffic/TrafficTileService?level=12&x=791&y=295&time=1508118996039&v=081&smallflow=1&scaler=1


gm = GlobalMercator()


# 保存图片
def saveimage_2d(x, y, z, t, ts):
    filename = temp_path_2d + '/' + ts + '/' + str(z) + '/' + str(y) + '_' + str(x) + '.png'
    # 地址需要修改
    site = "http://its.map.baidu.com:8002/traffic/TrafficTileService?level=%s&x=%s&y=%s&time=%s&scaler=1"%(
        z, x, y, t)
    print site
    response = urllib2.urlopen(site)
    html = response.read()
    # 如果没有路的判定
    if len(html) == 0:
        temp_image = Image.new('P', (256, 256))
        temp_image.save(filename)
    else:
        with open(filename, 'wb') as f:
            f.write(html)
    time.sleep(1)  # todo 根据线程数量 优化等待时间


# 用3d的方式请求
def savedata_3d(x, y, z, ts):
    site = 'http://its.map.baidu.com:8002/traffic/?qt=vtraffic&z=%s&x=%s&y=%s'%(z, x, y)
    response = urllib2.urlopen(site)
    html = response.read()
    html = eval(html)
    data = []
    if not html['error'] == -1:
        print site
        temp = html['content']['tf']
        c = 1
        for i in temp:
            pts = i[1]
            dx = dy = 0.0
            res = {'color': arrTrafficStyles[i[3]][1]}
            res['index'] = c
            res['x'] = x
            res['y'] = y
            res['z'] = z
            temp_pts = []
            for pt_index in range(len(pts)/2):
                dx += float(pts[pt_index*2])/10
                dy += float(pts[pt_index*2 + 1])/10
                # todo 到底是不是256-dy
                lon, lat = gm.imagepixeltolonlat(int(dx), int(dy), x, y, z)
                lon, lat = BDtoWGS([lon, lat])
                temp_pts.append([lon, lat])
                # temp_pts.append([int(dx), int(dy)])
            res['pts'] = temp_pts
            data.append(res)
            c += 1
    # temp_image = Image.new('P', (256, 256))
    return data


# 将文件保存到数据库中
def savedb(ts):
    db = dbc(False)
    with open(temp_path_3d + '/' + str(ts) + '.json', 'r') as f:
        data = json.loads(f.read())
    i = 1
    res = []
    for row in data:
        pts = row['pts']
        color = row['color']
        c = 1
        for t in range(len(pts) - 1):
            if pts[t] == pts[t + 1]:
                continue
            angel = CalAngle(pts[t], pts[t + 1])
            h= hash(str(row['x'])+str(row['y'])+str(row['z'])+str(row['index'])+str(c))
            res.append(
                [i, pts[t][0], pts[t][1], pts[t + 1][0], pts[t + 1][1], angel/math.pi*180, color, row['x'], row['y'],
                 row['z'], row['index'], c,h])
            i += 1
            c += 1
    for row in res:
        db.cur.execute("INSERT INTO bdts VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (row))
    db.Commit()


# 负责输入xy的边界和z的级别,生成array_x和array_y
def getxyz(bounds, z_level):
    left, bottom = gm.MetersToTiles_bd(bounds[0][0], bounds[0][1], z_level)
    print left, bottom
    right, top = gm.MetersToTiles_bd(bounds[1][0], bounds[1][1], z_level)
    print right, top
    array_x = range(left, right + 1)
    array_y = range(bottom, top + 1)
    if left == right:
        array_x = [left]
    if bottom == top:
        array_y = [top]
    print len(array_x)*len(array_y)
    return array_x, array_y


def networkproxy():
    proxy_handler = urllib2.ProxyHandler({'http': 'http://proxy.asiainfo.com:8080'})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)


def mergeimage(array_x, array_y, z, t, style_time):
    # cal image size
    print array_x, array_y
    image_size = (len(array_x)*256, len(array_y)*256)
    m_image = Image.new("RGBA", image_size)
    for x in array_x:
        for y in array_y:
            temp_img = Image.open(temp_path_2d + '/' + style_time + '/' + str(z) + '/' + str(y) + '_' + str(x) + '.png')
            p_x = array_x.index(x)*256
            p_y = len(array_y)*256 - array_y.index(y)*256
            # print x, y, p_x, p_y
            temp_img.convert("RGBA")
            m_image.paste(temp_img, (p_x, p_y))
    m_image.convert("P")
    m_image.save(ts_path + '/' + str(style_time) + '/' + str(z) + '/' + 'm.png')


# 生成目录并且下载
def startdownload_2d(array_x, array_y, z, t, style_time):
    if not os.path.exists(temp_path_2d + '/' + style_time + '/' + str(z)):
        os.makedirs(temp_path_2d + '/' + style_time + '/' + str(z))
    if not os.path.exists(ts_path + '/' + style_time + '/' + str(z)):
        os.makedirs(ts_path + '/' + style_time + '/' + str(z))
    index = 1
    for x in array_x:
        for y in array_y:
            print index
            index += 1
            saveimage_2d(x, y, z, t, ts=style_time)
    mergeimage(array_x, array_y, z, t, style_time)


def startdownload_3d(array_x, array_y, z, style_time):
    res = []
    for x in array_x:
        for y in array_y:
            data = savedata_3d(x, y, z, style_time)
            res.extend(data)
    with open(temp_path_3d + '/' + style_time + '.json', 'w') as f:
        f.write(json.dumps(res))


def drawimage(data):
    im = Image.new('RGB', (256, 256))
    draw = ImageDraw.Draw(im)
    for i in data:
        color = i['color'].split(',')
        color = [int(x) for x in color]
        pts = i['pts']
        for i in range(len(pts) - 1):
            draw.line([tuple(pts[i]), tuple(pts[i + 1])], (color[0], color[1], color[2]))
        im.show()
    im.show()
    # im.save('ts.jpg')


def old_main():
    z = 16
    # array_x, array_y = getxyz(bounds, z)
    # print array_x, array_y
    # todo 定时下载
    # t = 1509100273
    # t = time.localtime()
    # http://its.map.baidu.com:8002/traffic/?qt=vtraffic&z=14&x=3145&y=937
    # style_time = time.strftime("%Y%m%d%H%M%S", t)
    # print(style_time)
    style_time = 20171212101811
    # startdownload_3d(array_x, array_y, z, style_time)
    # startdownload_2d(array_x, array_y, z, t, style_time)
    # data = savedata_3d(3147, 943, 14, style_time)
    # drawimage(data)
    savedb(style_time)

# todo 怎么根据这个经纬度从我们库中获取车道数量
def speedtovolumn(speed, t, lanenumber, zygl, jfgl):
    if t < 7*60 or t > 23*60:
        if lanenumber == 2:
            return (80 - speed)/0.2
        if lanenumber == 4:
            if not zygl:
                return (80 - speed)/0.04
            else:
                return (70 - speed)/0.04
        if lanenumber == 6:
            return (80 - speed)/0.06
        if lanenumber == 8:
            return (80 - speed)/0.0567
    elif 9*60 > t > 7*60 or 19*60 > t > 17*60:
        if lanenumber == 2:
            return (pow(13.75 - speed, 1/4.1) - 2.7)/(-0.004)
        if lanenumber == 4:
            if not zygl:
                return (pow(28.6 - speed, 1/8) - 1.57)/(-0.0006)
            else:
                return (pow(31.4 - speed, 1/9) - 1.57)/(-0.0006)
        if lanenumber == 6:
            return (pow(27.98 - speed, 1/1.38) - 9.87)/(-0.0035)
        if lanenumber == 8:
            return (pow(66.058 - speed, 1/0.2) - 164789978)/(-677557)
    else:
        if lanenumber == 2:
            return (pow(73 - speed, 1/0.38) - 14)/51
        if lanenumber == 4:
            if not zygl:
                return (pow(110 - speed, 1/0.241) - 14305)/23908.8
            else:
                return (pow(51 - speed, 1/1.25) - 3.58)/0.005
        if lanenumber == 6:
            return (pow(86 - speed, 1/0.218) - 1430042.11727)/23908.8
        if lanenumber == 8:
            return (pow(36.778 - speed, 1/1.78) + 3.505)/0.0044


if __name__ == '__main__':
    if not os.path.exists(ts_path):
        os.makedirs(ts_path)
    if not os.path.exists(temp_path_2d):
        os.makedirs(temp_path_2d)
    if not os.path.exists(temp_path_3d):
        os.makedirs(temp_path_3d)
    # networkproxy()
    old_main()
    # savedb()
