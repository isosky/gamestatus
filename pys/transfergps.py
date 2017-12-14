# -*- coding: utf-8 -*-


# !/usr/bin/env python
###############################################################################
# $Id$
#
# Project:  GDAL2Tiles, Google Summer of Code 2007 & 2008
#           Global Map Tiles Classes
# Purpose:  Convert a raster into TMS tiles, create KML SuperOverlay EPSG:4326,
#           generate a simple HTML viewers based on Google Maps and OpenLayers
# Author:   Klokan Petr Pridal, klokan at klokan dot cz
# Web:      http://www.klokan.cz/projects/gdal2tiles/
#
###############################################################################
# Copyright (c) 2008 Klokan Petr Pridal. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

""" 
globalmaptiles.py 
 
Global Map Tiles as defined in Tile Map Service (TMS) Profiles 
============================================================== 
 
Functions necessary for generation of global tiles used on the web. 
It contains classes implementing coordinate conversions for: 
 
  - GlobalMercator (based on EPSG:900913 = EPSG:3785) 
       for Google Maps, Yahoo Maps, Microsoft Maps compatible tiles 
  - GlobalGeodetic (based on EPSG:4326) 
       for OpenLayers Base Map and Google Earth compatible tiles 
 
More info at: 
 
http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification 
http://wiki.osgeo.org/wiki/WMS_Tiling_Client_Recommendation 
http://msdn.microsoft.com/en-us/library/bb259689.aspx 
http://code.google.com/apis/maps/documentation/overlays.html#Google_Maps_Coordinates 
 
Created by Klokan Petr Pridal on 2008-07-03. 
Google Summer of Code 2008, project GDAL2Tiles for OSGEO. 
 
In case you use this class in your product, translate it to another language 
or find it usefull for your project please let me know. 
My email: klokan at klokan dot cz. 
I would like to know where it was used. 
 
Class is available under the open-source GDAL license (www.gdal.org). 
"""

import math


class GlobalMercator(object):
    """ 
    TMS Global Mercator Profile 
    --------------------------- 

    Functions necessary for generation of tiles in Spherical Mercator projection, 
    EPSG:900913 (EPSG:gOOglE, Google Maps Global Mercator), EPSG:3785, OSGEO:41001. 

    Such tiles are compatible with Google Maps, Microsoft Virtual Earth, Yahoo Maps, 
    UK Ordnance Survey Ope nSpace API, ...
    and you can overlay them on top of base maps of those web mapping applications. 

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left). 

    What coordinate conversions do we need for TMS Global Mercator tiles:: 

         LatLon      <->       Meters      <->     Pixels    <->       Tile      

     WGS84 coordinates   Spherical Mercator  Pixels in pyramid  Tiles in pyramid 
         lat/lon            XY in metres     XY pixels Z zoom      XYZ from TMS  
        EPSG:4326           EPSG:900913                                          
         .----.              ---------               --                TMS       
        /      \     <->     |       |     <->     /----/    <->      Google     
        \      /             |       |           /--------/          QuadTree    
         -----               ---------         /------------/                    
       KML, public         WebMapService         Web Clients      TileMapService 

    What is the coordinate extent of Earth in EPSG:900913? 

      [-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244] 
      Constant 20037508.342789244 comes from the circumference of the Earth in meters, 
      which is 40 thousand kilometers, the coordinate origin is in the middle of extent. 
      In fact you can calculate the constant as: 2 * math.pi * 6378137 / 2.0 
      $ echo 180 85 | gdaltransform -s_srs EPSG:4326 -t_srs EPSG:900913 
      Polar areas with abs(latitude) bigger then 85.05112878 are clipped off. 

    What are zoom level constants (pixels/meter) for pyramid with EPSG:900913? 

      whole region is on top of pyramid (zoom=0) covered by 256x256 pixels tile, 
      every lower zoom level resolution is always divided by two 
      initialResolution = 20037508.342789244 * 2 / 256 = 156543.03392804062 

    What is the difference between TMS and Google Maps/QuadTree tile name convention? 

      The tile raster itself is the same (equal extent, projection, pixel size), 
      there is just different identification of the same raster tile. 
      Tiles in TMS are counted from [0,0] in the bottom-left corner, id is XYZ. 
      Google placed the origin [0,0] to the top-left corner, reference is XYZ. 
      Microsoft is referencing tiles by a QuadTree name, defined on the website: 
      http://msdn2.microsoft.com/en-us/library/bb259689.aspx 

    The lat/lon coordinates are using WGS84 datum, yeh? 

      Yes, all lat/lon we are mentioning should use WGS84 Geodetic Datum. 
      Well, the web clients like Google Maps are projecting those coordinates by 
      Spherical Mercator, so in fact lat/lon coordinates on sphere are treated as if 
      the were on the WGS84 ellipsoid. 

      From MSDN documentation: 
      To simplify the calculations, we use the spherical form of projection, not 
      the ellipsoidal form. Since the projection is used only for map display, 
      and not for displaying numeric coordinates, we don't need the extra precision 
      of an ellipsoidal projection. The spherical projection causes approximately 
      0.33 percent scale distortion in the Y direction, which is not visually noticable. 

    How do I create a raster in EPSG:900913 and convert coordinates with PROJ.4? 

      You can use standard GIS tools like gdalwarp, cs2cs or gdaltransform. 
      All of the tools supports -t_srs 'epsg:900913'. 

      For other GIS programs check the exact definition of the projection: 
      More info at http://spatialreference.org/ref/user/google-projection/ 
      The same projection is degined as EPSG:3785. WKT definition is in the official 
      EPSG database. 

      Proj4 Text: 
        +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 
        +k=1.0 +units=m +nadgrids=@null +no_defs 

      Human readable WKT format of EPGS:900913: 
         PROJCS["Google Maps Global Mercator", 
             GEOGCS["WGS 84", 
                 DATUM["WGS_1984", 
                     SPHEROID["WGS 84",6378137,298.2572235630016, 
                         AUTHORITY["EPSG","7030"]], 
                     AUTHORITY["EPSG","6326"]], 
                 PRIMEM["Greenwich",0], 
                 UNIT["degree",0.0174532925199433], 
                 AUTHORITY["EPSG","4326"]], 
             PROJECTION["Mercator_1SP"], 
             PARAMETER["central_meridian",0], 
             PARAMETER["scale_factor",1], 
             PARAMETER["false_easting",0], 
             PARAMETER["false_northing",0], 
             UNIT["metre",1, 
                 AUTHORITY["EPSG","9001"]]] 
    """

    def __init__(self, tileSize=256):
        "Initialize the TMS Global Mercator pyramid"
        self.tileSize = tileSize
        self.initialResolution = 2*math.pi*6378137/self.tileSize
        # 156543.03392804062 for tileSize 256 pixels
        self.originShift = 2*math.pi*6378137/2.0
        # 20037508.342789244

    def LatLonToMeters(self, lat, lon):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"

        mx = lon*self.originShift/180.0
        my = math.log(math.tan((90 + lat)*math.pi/360.0))/ \
             (math.pi/180.0)

        my = my*self.originShift/180.0
        return mx, my

    def MetersToLatLon(self, mx, my):
        "Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"

        lon = (mx/self.originShift)*180.0
        lat = (my/self.originShift)*180.0

        lat = 180/math.pi* \
              (2*math.atan(math.exp(lat*math.pi/180.0)) - math.pi/2.0)
        return lat, lon

    def PixelsToMeters(self, px, py, zoom):
        "Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"

        res = self.Resolution(zoom)
        mx = px*res - self.originShift
        my = py*res - self.originShift
        return mx, my

    def MetersToPixels(self, mx, my, zoom):
        "Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"

        res = self.Resolution(zoom)
        px = (mx + self.originShift)/res
        py = (my + self.originShift)/res
        return px, py

    def PixelsToTile(self, px, py):
        "Returns a tile covering region in given pixel coordinates"

        tx = int(math.ceil(px/float(self.tileSize)) - 1)
        ty = int(math.ceil(py/float(self.tileSize)) - 1)
        return tx, ty

    def PixelsToRaster(self, px, py, zoom):
        "Move the origin of pixel coordinates to top-left corner"
        mapSize = self.tileSize << zoom
        return px, mapSize - py

    def MetersToTile(self, mx, my, zoom):
        "Returns tile for given mercator coordinates"
        px, py = self.MetersToPixels(mx, my, zoom)
        return self.PixelsToTile(px, py)

    def TileBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in EPSG:900913 coordinates"
        minx, miny = self.PixelsToMeters(
            tx*self.tileSize, ty*self.tileSize, zoom)
        maxx, maxy = self.PixelsToMeters(
            (tx + 1)*self.tileSize, (ty + 1)*self.tileSize, zoom)
        return (minx, miny, maxx, maxy)

    def TileLatLonBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in latutude/longitude using WGS84 datum"

        bounds = self.TileBounds(tx, ty, zoom)
        minLat, minLon = self.MetersToLatLon(bounds[0], bounds[1])
        maxLat, maxLon = self.MetersToLatLon(bounds[2], bounds[3])

        return (minLat, minLon, maxLat, maxLon)

    def Resolution(self, zoom):
        "Resolution (meters/pixel) for given zoom level (measured at Equator)"

        # return (2 * math.pi * 6378137) / (self.tileSize * 2**zoom)
        return self.initialResolution/(2 ** zoom)

    def ZoomForPixelSize(self, pixelSize):
        "Maximal scaledown zoom of the pyramid closest to the pixelSize."

        for i in range(30):
            if pixelSize > self.Resolution(i):
                return i - 1 if i != 0 else 0  # We don't want to scale up

    def GoogleTile(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Google Tile coordinates"

        # coordinate origin is moved from bottom-left to top-left corner of the
        # extent
        return tx, (2 ** zoom - 1) - ty

    def TmsTile(self, gx, gy, zoom):
        return gx, (2 ** zoom - 1) - gy

    def QuadTree(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Microsoft QuadTree"

        quadKey = ""
        ty = (2 ** zoom - 1) - ty
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if (tx & mask) != 0:
                digit += 1
            if (ty & mask) != 0:
                digit += 2
            quadKey += str(digit)

        return quadKey

    def LatLonToTile(self, lat, lon, zoom):
        m = self.LatLonToMeters(lat, lon)
        tile = self.MetersToTile(m[0], m[1], zoom)
        return tile

    def LatLonToPixels(self, lat, lon, zoom):
        m = self.LatLonToMeters(lat, lon)
        pixel = self.MetersToPixels(m[0], m[1], zoom)
        return pixel

    def MetersToPixels_bd(self, mx, my, zoom):
        px = int(math.floor(mx*(2 ** (zoom - 18))))
        py = int(math.floor(my*(2 ** (zoom - 18))))
        return px, py

    def PixelsToMeters_bd(self, px, py, zoom):
        mx = px/(2 ** (zoom - 18))
        my = py/(2 ** (zoom - 18))
        return mx, my

    def PixelsToTiles_bd(self, px, py, zoom):
        return int(math.floor(px/256)), int(math.floor(py/256))

    def TileBounds_bd(self, tx, ty, zoom):
        minx, miny = self.PixelsToMeters_bd(
            tx*self.tileSize, ty*self.tileSize, zoom)
        maxx, maxy = self.PixelsToMeters_bd(
            (tx + 1)*self.tileSize, (ty + 1)*self.tileSize, zoom)
        return (minx, miny, maxx, maxy)

    def imagepixeltolonlat(self, delta_px, delta_py, tx, ty, zoom):
        px = tx*self.tileSize + delta_px
        py = (ty + 1)*self.tileSize - delta_py
        mx, my = self.PixelsToMeters_bd(px, py, zoom)
        return self.Pointtolnglat(mx, my)

    def MetersToTiles_bd(self, mx, my, zoom):
        px, py = self.MetersToPixels_bd(mx, my, zoom)
        tx, ty = self.PixelsToTiles_bd(px, py, zoom)
        return abs(tx), abs(ty)

    def getPixelsInTiles_bd(self, tx, ty, zoom):
        return int(tx*256), int(ty*256), int((tx + 1)*256), int((ty + 1)*256)

    def getMeterFromPixels_bd(self, px, py, zoom):
        return float(px)/(2 ** (zoom - 18)), float(py)/(2 ** (zoom - 18))

    Bu = [75, 60, 45, 30, 15, 0]
    rG = [1.289059486E7, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
    oG = [[-0.0015702102444, 111320.7020616939, 1704480524535203, -10338987376042340, 26112667856603880,
           -35149669176653700,
           26595700718403920, -10725012454188240, 1800819912950474, 82.5],
          [8.277824516172526E-4, 111320.7020463578, 6.477955746671607E8, -4.082003173641316E9, 1.077490566351142E10,
           -1.517187553151559E10, 1.205306533862167E10, -5.124939663577472E9, 9.133119359512032E8, 67.5],
          [0.00337398766765, 111320.7020202162, 4481351.045890365, -2.339375119931662E7, 7.968221547186455E7,
           -1.159649932797253E8, 9.723671115602145E7, -4.366194633752821E7, 8477230.501135234, 52.5],
          [0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013,
           -1221952.21711287,
           1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5],
          [-3.441963504368392E-4, 111320.7020576856, 278.2353980772752, 2485758.690035394, 6070.750963243378,
           54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5],
          [-3.218135878613132E-4, 111320.7020701615, 0.00369383431289, 823725.6402795718, 0.46104986909093,
           2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45]]
    pP = [[1.410526172116255E-8, 8.98305509648872E-6, -1.9939833816331, 200.9824383106796, -187.2403703815547,
           91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 1.73379812E7],
          [-7.435856389565537E-9, 8.983055097726239E-6, -0.78625201886289, 96.32687599759846, -1.85204757529826,
           -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 1.026014486E7],
          [-3.030883460898826E-8, 8.98305509983578E-6, 0.30071316287616, 59.74293618442277, 7.357984074871,
           -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
          [-1.981981304930552E-8, 8.983055099779535E-6, 0.03278182852591, 40.31678527705744, 0.65659298677277,
           -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
          [3.09191371068437E-9, 8.983055096812155E-6, 6.995724062E-5, 23.10934304144901, -2.3663490511E-4,
           -0.6321817810242,
           -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
          [2.890871144776878E-9, 8.983055095805407E-6, -3.068298E-8, 7.47137025468032, -3.53937994E-6,
           -0.02145144861037,
           -1.234426596E-5, 1.0322952773E-4, -3.23890364E-6, 826088.5]]

    def lnglattoPoint(self, lon, lat):
        for x in self.Bu:
            if lat >= x:
                b = self.oG[self.Bu.index(x)]
                break
        c = b[0] + b[1]*abs(lon)
        d = abs(lat)/b[9]
        d = b[2] + b[3]*d + b[4]*d*d + b[5]*d*d*d + b[6]*d*d*d*d + b[7]*d*d*d*d*d + b[8]*d*d*d*d*d*d
        if 0 > lon:
            c = c*-1
        if 0 > lat:
            d = d*-1
        return [round(c, 2), round(d, 2)]

    def Pointtolnglat(self, mx, my):
        for x in self.rG:
            if my >= x:
                b = self.pP[self.rG.index(x)]
                break
        c = b[0] + b[1]*abs(mx)
        d = abs(my)/b[9]
        d = b[2] + b[3]*d + b[4]*d*d + b[5]*d*d*d + b[6]*d*d*d*d + b[7]*d*d*d*d*d + b[8]*d*d*d*d*d*d
        if 0 > mx:
            c = c*-1
        if 0 > my:
            d = d*-1
        return [round(c, 6), round(d, 6)]


class GlobalGeodetic(object):
    """ 
    TMS Global Geodetic Profile 
    --------------------------- 

    Functions necessary for generation of global tiles in Plate Carre projection, 
    EPSG:4326, "unprojected profile". 

    Such tiles are compatible with Google Earth (as any other EPSG:4326 rasters) 
    and you can overlay the tiles on top of OpenLayers base map. 

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left). 

    What coordinate conversions do we need for TMS Global Geodetic tiles? 

      Global Geodetic tiles are using geodetic coordinates (latitude,longitude) 
      directly as planar coordinates XY (it is also called Unprojected or Plate 
      Carre). We need only scaling to pixel pyramid and cutting to tiles. 
      Pyramid has on top level two tiles, so it is not square but rectangle. 
      Area [-180,-90,180,90] is scaled to 512x256 pixels. 
      TMS has coordinate origin (for pixels and tiles) in bottom-left corner. 
      Rasters are in EPSG:4326 and therefore are compatible with Google Earth. 

         LatLon      <->      Pixels      <->     Tiles      

     WGS84 coordinates   Pixels in pyramid  Tiles in pyramid 
         lat/lon         XY pixels Z zoom      XYZ from TMS  
        EPSG:4326                                            
         .----.                ----                          
        /      \     <->    /--------/    <->      TMS       
        \      /         /--------------/                    
         -----        /--------------------/                 
       WMS, KML    Web Clients, Google Earth  TileMapService 
    """

    def __init__(self, tileSize=256):
        self.tileSize = tileSize

    def LatLonToPixels(self, lat, lon, zoom):
        "Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"

        res = 180/256.0/2 ** zoom
        px = (180 + lat)/res
        py = (90 + lon)/res
        return px, py

    def PixelsToTile(self, px, py):
        "Returns coordinates of the tile covering region in pixel coordinates"

        tx = int(math.ceil(px/float(self.tileSize)) - 1)
        ty = int(math.ceil(py/float(self.tileSize)) - 1)
        return tx, ty

    def Resolution(self, zoom):
        "Resolution (arc/pixel) for given zoom level (measured at Equator)"

        return 180/256.0/2 ** zoom
        # return 180 / float( 1 << (8+zoom) )

    def TileBounds(tx, ty, zoom):
        "Returns bounds of the given tile"
        res = 180/256.0/2 ** zoom
        return (
            tx*256*res - 180,
            ty*256*res - 90,
            (tx + 1)*256*res - 180,
            (ty + 1)*256*res - 90
        )


if __name__ == "__main__":
    import sys
    import os


    def Usage(s=""):
        print "Usage: globalmaptiles.py [-profile 'mercator'|'geodetic'] zoomlevel lat lon [latmax lonmax]"
        print
        if s:
            print s
            print
        print "This utility prints for given WGS84 lat/lon coordinates (or bounding box) the list of tiles"
        print "covering specified area. Tiles are in the given 'profile' (default is Google Maps 'mercator')"
        print "and in the given pyramid 'zoomlevel'."
        print "For each tile several information is printed including bonding box in EPSG:900913 and WGS84."
        sys.exit(1)


    profile = 'mercator'
    zoomlevel = None
    lat, lon, latmax, lonmax = None, None, None, None
    boundingbox = False

    argv = sys.argv
    i = 1
    while i < len(argv):
        arg = argv[i]

        if arg == '-profile':
            i = i + 1
            profile = argv[i]

        if zoomlevel is None:
            zoomlevel = int(argv[i])
        elif lat is None:
            lat = float(argv[i])
        elif lon is None:
            lon = float(argv[i])
        elif latmax is None:
            latmax = float(argv[i])
        elif lonmax is None:
            lonmax = float(argv[i])
        else:
            Usage("ERROR: Too many parameters")

        i = i + 1

    if profile != 'mercator':
        Usage("ERROR: Sorry, given profile is not implemented yet.")

    if zoomlevel == None or lat == None or lon == None:
        Usage("ERROR: Specify at least 'zoomlevel', 'lat' and 'lon'.")
    if latmax is not None and lonmax is None:
        Usage("ERROR: Both 'latmax' and 'lonmax' must be given.")

    if latmax != None and lonmax != None:
        if latmax < lat:
            Usage("ERROR: 'latmax' must be bigger then 'lat'")
        if lonmax < lon:
            Usage("ERROR: 'lonmax' must be bigger then 'lon'")
        boundingbox = (lon, lat, lonmax, latmax)

    tz = zoomlevel
    mercator = GlobalMercator()

    mx, my = mercator.LatLonToMeters(lat, lon)
    print "Spherical Mercator (ESPG:900913) coordinates for lat/lon: "
    print(mx, my)
    tminx, tminy = mercator.MetersToTile(mx, my, tz)

    if boundingbox:
        mx, my = mercator.LatLonToMeters(latmax, lonmax)
        print "Spherical Mercator (ESPG:900913) cooridnate for maxlat/maxlon: "
        print(mx, my)
        tmaxx, tmaxy = mercator.MetersToTile(mx, my, tz)
    else:
        tmaxx, tmaxy = tminx, tminy

    for ty in range(tminy, tmaxy + 1):
        for tx in range(tminx, tmaxx + 1):
            tilefilename = "%s/%s/%s"%(tz, tx, ty)
            print tilefilename, "( TileMapService: z / x / y )"

            gx, gy = mercator.GoogleTile(tx, ty, tz)
            print "\tGoogle:", gx, gy
            quadkey = mercator.QuadTree(tx, ty, tz)
            print "\tQuadkey:", quadkey, '(', int(quadkey, 4), ')'
            bounds = mercator.TileBounds(tx, ty, tz)
            print
            print "\tEPSG:900913 Extent: ", bounds
            wgsbounds = mercator.TileLatLonBounds(tx, ty, tz)
            print "\tWGS84 Extent:", wgsbounds
            print "\tgdalwarp -ts 256 256 -te %s %s %s %s %s %s_%s_%s.tif"%(
                bounds[0], bounds[1], bounds[2], bounds[3], "<your-raster-file-in-epsg900913.ext>", tz, tx, ty)
            print
