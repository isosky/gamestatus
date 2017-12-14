# coding=utf-8
from transfergps import *
import urllib2
import os
from PIL import Image
import random
import threading
import time
import shutil
from config import dis_path, old_path, style, bounds


# 保存图片
def saveimage(x, y, z):
    s = random.randint(0, 2)
    filename = str(z) + '/' + str(x) + '/' + str(y) + '.jpg'
    # 地址需要修改
    site = 'http://api' + str(s) + '.map.bdimg.com/customimage/tile?&x=' + str(x) + '&y=' + str(y) + '&z=' + str(
        z) + '&udt=20150601' + style

    response = urllib2.urlopen(site)
    html = response.read()
    with open(dis_path + '/' + filename, 'wb') as f:
        f.write(html)
    time.sleep(1) #todo 根据线程数量 优化等待时间


# 截断文件名,开始下载
def saveimage_a(ll):
    counts = 0
    s = len(ll)
    for i in ll:
        k = i.split(',')
        print threading.currentThread().getName() + ':' + str(k[0]) + ',' + str(k[1]) + ',' + str(k[2])
        print threading.currentThread().getName() + ': the rest of list is ' + str(s - counts)
        counts += 1
        saveimage(k[0], k[1], k[2])


# 本函数负责检查哪些已经下载了,同时生成待下载列表
l = []


def check_old(x, y, z):
    global l
    l = []
    for i in x:
        for j in y:
            filename = str(z) + '/' + str(i) + '/' + str(j) + '.jpg'
            if not os.path.exists(old_path + '/' + filename):
                l.append(str(i) + ',' + str(j) + ',' + str(z))
                # else:
                #     print filename + ' is already exists,skip'
    print "need download :", len(l)


# 负责输入xy的边界和z的级别,生成array_x和array_y,同时生成目录
def getxyz(bounds, z_level):
    gm = GlobalMercator()
    left, bottom = gm.MetersToTiles_bd(bounds[0][0], bounds[0][1], z_level)
    print   left, bottom
    right, top = gm.MetersToTiles_bd(bounds[1][0], bounds[1][1], z_level)
    print   right, top

    array_x = range(left, right + 1)
    array_y = range(bottom, top + 1)
    if left == right:
        array_x = [left]
    if bottom == top:
        array_y = [top]
    print len(array_x) * len(array_y)
    for i in array_x:
        if not os.path.exists(dis_path + '/' + str(z_level) + '/' + str(i)):
            os.makedirs(dis_path + '/' + str(z_level) + '/' + str(i))
    return array_x, array_y


# 负责备份图片
def bakphotos():
    if not os.path.exists(dis_path):
        os.makedirs(dis_path)
    if not os.path.exists(old_path):
        os.makedirs(old_path)
    for dirpaths, dirnames, filenames in os.walk(dis_path):
        for filename in filenames:
            temp_old = dirpaths + '/' + filename
            # print temp_old
            temp_new = old_path + temp_old[len(dis_path):]
            temp_dis_dir = old_path + dirpaths[len(dis_path):]
            # print temp_dis_dir
            if not os.path.exists(temp_new):
                if not os.path.exists(temp_dis_dir):
                    os.makedirs(temp_dis_dir)
                shutil.move(temp_old, temp_new)


def startThread():
    threads = []
    if len(l) > 100:
        pro_count = 50
        pro_numbs = int(len(l) / pro_count)
        for i in range(0, pro_numbs + 1):
            print 'start from :', pro_count * i, ',end by :', pro_count * (i + 1)
            t = l[pro_count * i:pro_count * (i + 1)]
            print "the number of this thread's image is :", len(t)
            thread = threading.Thread(target=saveimage_a, args=(t,))
            threads.append(thread)
    else:
        thread = threading.Thread(target=saveimage_a, args=(l,))
        threads.append(thread)
    # print threads
    for t in threads:
        # t.setDaemon(True)
        t.start()

def networkproxy():
    proxy_handler = urllib2.ProxyHandler({'http': 'http://proxy.asiainfo.com:8080'})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

if __name__ == '__main__':
    networkproxy()
    bakphotos()
    for z_level in range(12, 13):
        print 'starting download :', z_level
        # z_level=7CC
        array_x, array_y = getxyz(bounds, z_level)
        check_old(array_x, array_y, z_level)
    startThread()
    bakphotos()
