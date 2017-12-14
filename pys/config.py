# coding=utf-8

import psycopg2


class dbc(object):
    def __init__(self, s=True):
        """

        :rtype: object
        """
        if s:
            self.conn = psycopg2.connect(database="fuyang0913", user="postgres",
                                         password="password", host="10.1.51.93", port="5432")
        else:
            self.conn = psycopg2.connect(database="fuyang", user="postgres",
                                         password="123", host="localhost", port="5432")
        self.cur = self.conn.cursor()

    def disconnectdb(self):
        self.cur.close()
        self.conn.close()
        print "DB Disconnected"

    def Commit(self):
        self.conn.commit()


# dis_path = './wuxi'
# old_path = './wuxi_bak'
ts_path = './ts'
temp_path_2d = './temp/2d'
temp_path_3d = './temp/3d'
temp_path_road = './temp/roadjson'

# http://api1.map.bdimg.com/customimage/tile?&x=1635&y=430&z=13&udt=20150601
# 需要从url中抓到下面的信息
# style = "&styles=t%3Awater%7Ce%3Aall%7Cc%3A%230e5581%2Ct%3Aland%7Ce%3Aall%7Cc%3A%23071733%2Ct%3Aboundary%7Ce%3Ag%7Cc%3A%23064f85%2Ct%3Arailway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Ag%7Cv%3Aoff%7Cc%3A%230363a2%7Cw%3A0.2%2Ct%3Ahighway%7Ce%3Ag.f%7Cv%3Aoff%7Cc%3A%230363a2%7Cl%3A1%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aoff%2Ct%3Aarterial%7Ce%3Ag%7Cv%3Aoff%7Cc%3A%23ffffff%7Cl%3A-39%2Ct%3Aarterial%7Ce%3Ag.f%7Cv%3Aoff%7Cc%3A%2300508b%2Ct%3Apoi%7Ce%3Aall%7Cv%3Aoff%2Ct%3Agreen%7Ce%3Aall%7Cv%3Aoff%7Cc%3A%23056197%2Ct%3Asubway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Amanmade%7Ce%3Aall%7Cv%3Aoff%2Ct%3Alocal%7Ce%3Aall%7Cv%3Aoff%2Ct%3Aarterial%7Ce%3Al%7Cv%3Aoff%2Ct%3Aboundary%7Ce%3Ag.f%7Cc%3A%23029fd4%2Ct%3Abuilding%7Ce%3Aall%7Cc%3A%231a5787%2Ct%3Alabel%7Ce%3Aall%7Cv%3Aoff%2Ct%3Apoi%7Ce%3Al.t.f%7Cc%3A%23ffffff%2Ct%3Apoi%7Ce%3Al.t.s%7Cc%3A%231e1c1c%2Ct%3Aadministrative%7Ce%3Al%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aoff"

# 有路
# style = "&styles=t%3Awater%7Ce%3Aall%7Cc%3A%230e5581%2Ct%3Aland%7Ce%3Aall%7Cc%3A%23071733%2Ct%3Aboundary%7Ce%3Ag%7Cc%3A%23064f85%2Ct%3Arailway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Ag%7Cv%3Aoff%7Cc%3A%230363a2%7Cw%3A0.2%2Ct%3Ahighway%7Ce%3Ag.f%7Cv%3Aon%7Cc%3A%230363a2%7Cl%3A1%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aon%2Ct%3Aarterial%7Ce%3Ag%7Cv%3Aon%7Cc%3A%23ffffff%7Cl%3A-39%2Ct%3Aarterial%7Ce%3Ag.f%7Cv%3Aon%7Cc%3A%2300508b%2Ct%3Apoi%7Ce%3Aall%7Cv%3Aoff%2Ct%3Agreen%7Ce%3Aall%7Cv%3Aoff%7Cc%3A%23056197%2Ct%3Asubway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Amanmade%7Ce%3Aall%7Cv%3Aoff%2Ct%3Alocal%7Ce%3Aall%7Cv%3Aoff%2Ct%3Aarterial%7Ce%3Al%7Cv%3Aoff%2Ct%3Aboundary%7Ce%3Ag.f%7Cc%3A%23029fd4%2Ct%3Abuilding%7Ce%3Aall%7Cc%3A%231a5787%2Ct%3Alabel%7Ce%3Aall%7Cv%3Aoff%2Ct%3Apoi%7Ce%3Al.t.f%7Cc%3A%23ffffff%2Ct%3Apoi%7Ce%3Al.t.s%7Cc%3A%231e1c1c%2Ct%3Aadministrative%7Ce%3Al%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aoff"

# new
# style ="&styles=t%3Awater%7Ce%3Aall%7Cc%3A%230e5581%2Ct%3Aland%7Ce%3Aall%7Cc%3A%23071733%2Ct%3Aboundary%7Ce%3Ag%7Cc%3A%23064f85%2Ct%3Arailway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Ag%7Cv%3Aon%7Cc%3A%230363a2%7Cw%3A0.2%2Ct%3Ahighway%7Ce%3Ag.f%7Cv%3Aon%7Cc%3A%230363a2%7Cl%3A1%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aon%2Ct%3Aarterial%7Ce%3Ag%7Cv%3Aon%7Cc%3A%23ffffff%7Cl%3A-39%2Ct%3Aarterial%7Ce%3Ag.f%7Cv%3Aon%7Cc%3A%2300508b%2Ct%3Apoi%7Ce%3Aall%7Cv%3Aoff%2Ct%3Agreen%7Ce%3Aall%7Cv%3Aoff%7Cc%3A%23056197%2Ct%3Asubway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Amanmade%7Ce%3Aall%7Cv%3Aoff%2Ct%3Alocal%7Ce%3Aall%7Cv%3Aoff%2Ct%3Aarterial%7Ce%3Al%7Cv%3Aoff%2Ct%3Aboundary%7Ce%3Ag.f%7Cc%3A%23029fd4%2Ct%3Abuilding%7Ce%3Aall%7Cc%3A%231a5787%2Ct%3Alabel%7Ce%3Aall%7Cv%3Aoff%2Ct%3Apoi%7Ce%3Al.t.f%7Cc%3A%23ffffff%2Ct%3Apoi%7Ce%3Al.t.s%7Cc%3A%231e1c1c%2Ct%3Aadministrative%7Ce%3Al%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aon"

# demo
# style = "&styles=t%3Awater%7Ce%3Aall%7Cc%3A%230e5581%2Ct%3Aland%7Ce%3Aall%7Cc%3A%23071733%2Ct%3Aboundary%7Ce%3Ag%7Cc%3A%23064f85%2Ct%3Arailway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Ag%7Cv%3Aon%7Cc%3A%230363a2%7Cw%3A0.2%2Ct%3Ahighway%7Ce%3Ag.f%7Cv%3Aon%7Cc%3A%230363a2%7Cl%3A1%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aoff%2Ct%3Aarterial%7Ce%3Ag%7Cv%3Aon%7Cc%3A%23ffffff%7Cl%3A-39%2Ct%3Aarterial%7Ce%3Ag.f%7Cv%3Aon%7Cc%3A%2300508b%2Ct%3Apoi%7Ce%3Aall%7Cv%3Aoff%2Ct%3Agreen%7Ce%3Aall%7Cv%3Aoff%7Cc%3A%23056197%2Ct%3Asubway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Amanmade%7Ce%3Aall%7Cv%3Aoff%2Ct%3Alocal%7Ce%3Aall%7Cv%3Aoff%2Ct%3Aarterial%7Ce%3Al%7Cv%3Aoff%2Ct%3Aboundary%7Ce%3Ag.f%7Cc%3A%23029fd4%2Ct%3Abuilding%7Ce%3Aall%7Cc%3A%231a5787%2Ct%3Alabel%7Ce%3Aall%7Cv%3Aoff%2Ct%3Apoi%7Ce%3Al.t.f%7Cc%3A%23ffffff%2Ct%3Apoi%7Ce%3Al.t.s%7Cc%3A%231e1c1c%2Ct%3Aadministrative%7Ce%3Al%7Cv%3Aoff%2Ct%3Ahighway%7Ce%3Al%7Cv%3Aoff&t%20=%201485049133290"

# default
# style = "&styles=t%3Arailway%7Ce%3Al%7Cv%3Aoff"


#############################
# baidu ts config
arrTrafficStyles = [[2, "80,191,57,1", 3, 2, 0, [], 0, 0], [2, "80,191,57,1", 3, 2, 0, [], 0, 0],
                    [2, "80,191,57,1", 4, 2, 0, [], 0, 0], [2, "80,191,57,1", 5, 2, 0, [], 0, 0],
                    [2, "80,191,57,1", 6, 2, 0, [], 0, 0], [2, "255,159,25,1", 3, 2, 0, [], 0, 0],
                    [2, "255,159,25,1", 3, 2, 0, [], 0, 0], [2, "255,159,25,1", 4, 2, 0, [], 0, 0],
                    [2, "255,159,25,1", 5, 2, 0, [], 0, 0], [2, "255,159,25,1", 6, 2, 0, [], 0, 0],
                    [2, "242,48,48,1", 3, 2, 0, [], 0, 0], [2, "242,48,48,1", 3, 2, 0, [], 0, 0],
                    [2, "242,48,48,1", 4, 2, 0, [], 0, 0], [2, "242,48,48,1", 5, 2, 0, [], 0, 0],
                    [2, "242,48,48,1", 6, 2, 0, [], 0, 0], [2, "255,255,255,1", 4, 0, 0, [], 0, 0],
                    [2, "255,255,255,1", 5.5, 0, 0, [], 0, 0], [2, "255,255,255,1", 7, 0, 0, [], 0, 0],
                    [2, "255,255,255,1", 8.5, 0, 0, [], 0, 0], [2, "255,255,255,1", 10, 0, 0, [], 0, 0]]

# 得到bounds  左下和右上
#############################js取得经纬度对应的平面坐标
# var projection =new BMap.MercatorProjection();
# var point = projection.lngLatToPoint(new BMap.Point(72.77109, 12.521009));
#############################
# 无锡
# 120.610797	119.525817	31.991045	31.126222
# 更大区域 119.50,31.1 120.93,32.1
# var point = projection.lngLatToPoint(new BMap.Point(119.50,31.1));
# var point = projection.lngLatToPoint(new BMap.Point(120.93,32.1));
#############################
# bounds = [[13302823.89, 3623469.36], [13462012.5, 3753529.33]]

# 阜阳
# bounds = [[13302823.89, 3623469.36], [13462012.5, 3753529.33]]
# var projection =new BMap.MercatorProjection();
# var point = projection.lngLatToPoint(new BMap.Point(115.751015,32.863678));
# var point = projection.lngLatToPoint(new BMap.Point(115.901355,32.953157));
bounds = [[12885484.25, 3850823.18], [12902220.21, 3862631.13]]




# 3d
# http://its.map.baidu.com:8002/traffic/?qt=vtraffic&z=15&x=6323&y=2365&udt=20171012&fn=BMap.cbkBMAP_CUSTOM_LAYER_0_6323_2365_15