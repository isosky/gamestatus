# -*-coding:utf-8-*-
import math

'''
国际经纬度坐标标准为WGS-84,国内必须至少使用国测局制定的GCJ-02,对地理位置进行首次加密。
百度坐标在此基础上，进行了BD-09二次加密措施,更加保护了个人隐私。
GCJ-02是中国境内的所有GPS设备的数据的坐标系,也是高德等地图的坐标系
所以要从BD-09到GCJ-02再到WGS-84
BDtoWGS:百度坐标系到wgs-84坐标系
WGStoBD:wgs-84坐标系到百度坐标系
GPStoBD
BDtoGPS
GPStoWGS
WGStoGPS
'''

x_pi = 3.14159265358979324*3000.0/180.0
pi = 3.14159265358979324
a = 6378245.0
ee = 0.00669342162296594323


def GPStoBD(gps):
    gps_x = gps[0]
    gps_y = gps[1]
    temp = math.sqrt(gps_x*gps_x + gps_y*gps_y) + 0.00002*math.sin(gps_y*x_pi)
    theta = math.atan2(gps_y, gps_x) + 0.000003*math.cos(gps_x*x_pi)
    bd_x = temp*math.cos(theta) + 0.0065
    bd_y = temp*math.sin(theta) + 0.006
    return [bd_x, bd_y]


def BDtoGPS(bd):
    bd_x = bd[0] - 0.0065
    bd_y = bd[1] - 0.006
    temp = math.sqrt(bd_x*bd_x + bd_y*bd_y) - 0.00002*math.sin(bd_y*x_pi)
    theta = math.atan2(bd_y, bd_x) - 0.000003*math.cos(bd_x*x_pi)
    gps_x = temp*math.cos(theta)
    gps_y = temp*math.sin(theta)
    return [gps_x, gps_y]


def WGStoGPS(wgs):
    wgLon = wgs[0]
    wgLat = wgs[1]
    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat/180.0*pi
    magic = math.sin(radLat)
    magic = 1 - ee*magic*magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat*180.0)/((a*(1 - ee))/(magic*sqrtMagic)*pi)
    dLon = (dLon*180.0)/(a/sqrtMagic*math.cos(radLat)*pi)
    mgLat = wgLat + dLat
    mgLon = wgLon + dLon
    return [mgLon, mgLat]


def GPStoWGS(gps):
    lng = gps[0]
    lat = gps[1]
    dlat = transformLat(lng - 105.0, lat - 35.0);
    dlng = transformLon(lng - 105.0, lat - 35.0);
    radlat = lat/180.0*pi;
    magic = math.sin(radlat);
    magic = 1 - ee*magic*magic;
    sqrtmagic = math.sqrt(magic);
    dlat = (dlat*180.0)/((a*(1 - ee))/(magic*sqrtmagic)*pi);
    dlng = (dlng*180.0)/(a/sqrtmagic*math.cos(radlat)*pi);
    mglat = lat + dlat;
    mglng = lng + dlng;
    return [lng*2 - mglng, lat*2 - mglat]


def transformLat(x, y):
    ret = -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*pi) + 20.0*math.sin(2.0*x*pi))*2.0/3.0
    ret += (20.0*math.sin(y*pi) + 40.0*math.sin(y/3.0*pi))*2.0/3.0
    ret += (160.0*math.sin(y/12.0*pi) + 320*math.sin(y*pi/30.0))*2.0/3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*pi) + 20.0*math.sin(2.0*x*pi))*2.0/3.0
    ret += (20.0*math.sin(x*pi) + 40.0*math.sin(x/3.0*pi))*2.0/3.0
    ret += (150.0*math.sin(x/12.0*pi) + 300.0*math.sin(x/30.0*pi))*2.0/3.0
    return ret


def WGStoBD(wgs):
    res = WGStoGPS(wgs)
    res = GPStoBD(res)
    return res


def BDtoWGS(bd):
    res = BDtoGPS(bd)
    res = GPStoWGS(res)
    return res
