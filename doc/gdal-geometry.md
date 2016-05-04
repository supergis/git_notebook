

```python
#!/usr/bin/python
#coding=GB2312
```

# OGR-Geometry and Projection
### 几何对象与地图投影的使用。
by [openthings@163.com](http://my.oschina.net/u/2306127/blog?catalog=3420733), 2016-04-25.  
#### OGR矢量库：简单的矢量数据读写，是GDAL的一部分。
#### 相关模块:
    Numeric：高速的数组处理，对栅格数据尤其重要
    NumPy：下一代的Numeric
    更强大的gis库 http://www.gispython.org/

### 导入库


```python
from osgeo import gdal, gdalconst
from osgeo.gdalconst import *
import gdal, gdalconst

from osgeo import ogr
```

## 建立新的几何对象

建立空的geometry对象：ogr.Geometry，定义各种不同的geometry使用的方法是不一样的(point, line, polygon, etc)。

### 新建点对象－point
使用方法AddPoint( <x>, <y>, [<z>])。其中的z坐标一般是省略的，默认值是0.


```python
point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(10,20)
```




    <osgeo.ogr.Geometry; proxy of <Swig Object of type 'OGRGeometryShadow *' at 0x7f2d0812d240> >




```python
#help(point)
str(point)
```




    'POINT (10 20 0)'



### 新建线对象－line

* 使用AddPoint(<x>, <y>, [<z>])添加点。
* 使用SetPoint(<index>, <x>, <y>, [<z>])更改点的坐标。

例如下面这段代码，更改了0号点的坐标：


```python
line = ogr.Geometry(ogr.wkbLineString)
line.AddPoint(10,10)
line.AddPoint(20,20)
line.SetPoint(0,30,30)   #(10,10) -> (30,30)
```


```python
str(line)
```




    'LINESTRING (30 30 0,20 20 0)'



统计所有点的数目


```python
print(line.GetPointCount())
```

    2


读取0号点的x坐标和y坐标


```python
print(line.GetX(0))
print(line.GetY(0))
```

    30.0
    30.0


### 新建多边形-polygon
首先要新建环(ring)，然后把环添加到多边形对象中。  
如何创建一个ring？先新建一个ring对象，然后向里面逐个添加点。


```python
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(0,0)
ring.AddPoint(100,0)
ring.AddPoint(100,100)
ring.AddPoint(0,100)
```

结束的时候，用CloseRings关闭ring，或者将最后一个点的坐标设定为与第一个点相同。


```python
ring.CloseRings()

#ring.AddPoint(0,0)
```


```python
str(ring)
```




    'LINEARRING (0 0 0,100 0 0,100 100 0,0 100 0,0 0 0)'



### 下面举一个例子，创建一个方框。
这是个polygon对象，又例外两层ring构成。


```python
outring = ogr.Geometry(ogr.wkbLinearRing)
outring.AddPoint(0,0)
outring.AddPoint(100,0)
outring.AddPoint(100,100)
outring.AddPoint(0,100)
outring.AddPoint(0,0)

inring = ogr.Geometry(ogr.wkbLinearRing)
inring = ogr.Geometry(ogr.wkbLinearRing)
inring.AddPoint(25,25)
inring.AddPoint(75,25)
inring.AddPoint(75,75)
inring.AddPoint(25,75)
inring.CloseRings()

polygon = ogr.Geometry(ogr.wkbPolygon)
polygon.AddGeometry(outring)
polygon.AddGeometry(inring)
```




    0




```python
str(polygon)
```




    'POLYGON ((0 0 0,100 0 0,100 100 0,0 100 0,0 0 0),(25 25 0,75 25 0,75 75 0,25 75 0,25 25 0))'



** _最后三句话比较重要，就是先建立一个polygon对象，然后添加外层ring和内层ring。_ **

下面这句话可以帮你数数，polygon能有几个ring。


```python
print(polygon.GetGeometryCount())
```

    2


从polygon中读取ring，index的顺序和创建polygon时添加ring的顺序相同。


```python
outring = polygon.GetGeometryRef(0)
inring = polygon.GetGeometryRef(1)
```


```python
print("OutRing: ",str(outring))
print("InRing: ",str(inring))
```

    OutRing:  LINEARRING (0 0 0,100 0 0,100 100 0,0 100 0,0 0 0)
    InRing:  LINEARRING (25 25 0,75 25 0,75 75 0,25 75 0,25 25 0)


### 创建复合几何形状－multi geometry

例如：MultiPoint, MultiLineString, MultiPolygon。用AddGeometry把普通的几何形状加到复合几何形状中。


```python
multipoint = ogr.Geometry(ogr.wkbMultiPoint)
point = ogr.Geometry(ogr.wkbPoint)

point.AddPoint(10,10)
multipoint.AddGeometry(point)

point.AddPoint(20,20)
multipoint.AddGeometry(point)
```




    0




```python
str(multipoint)
```




    'MULTIPOINT (10 10 0,20 20 0)'



### 读取MultiGeometry中的Geometry
方法和从Polygon中读取ring是一样的，可以说Polygon是一种内置的MultiGeometry。

* 不要删除一个已存在的Feature的Geometry，会把python搞崩溃的。
* 只能删除脚本运行期间创建的Geometry，比方说手工创建出来的，或者调用其他函数自动创建的。就算这个Geometry已经用来创建别的Feature，你还是可以删除它。

例如：Polygon.Destroy()

# 关于投影－Projection
使用SpatialReference对象。
* 多种多样的Projections，GDAL支持WKT, PROJ.4, ESPG, USGS, ESRI.prj  
* 可以从layer和Geometry中读取Projections。

例如：


```python
spatialRef = layer.GetSpatialRef()
spatialRef = geom.GetSpatialReference()
```

投影信息一般存储在.prj文件中，如果没有这个文件，上述函数返回None。
### 建立一个新的Projection
首先导入osr库，之后使用osr.SpatialReference()创建SpatialReference对象。
用下列语句向SpatialReference对象导入投影信息。

    ImportFromWkt(<wkt>)  
    ImportFromEPSG(<epsg>)  
    ImportFromProj4(<proj4>)  
    ImportFromESRI(<proj_lines>)  
    ImportFromPCI(<proj>, <units>, <parms>)  
    ImportFromUSGS(<proj_code>, <zone>)  
    ImportFromXML(<xml>)  

### 导出Projection
使用下面的语句可以导出为字符串

    ExportToWkt()
    ExportToPrettyWkt()
    ExportToProj4()
    ExportToPCI()
    ExportToUSGS()
    ExportToXML()

对一个几何形状Geometry进行投影变换，要先初始化两个Projection，然后创建一个CoordinateTransformation对象，用它来做变换。


```python
from osgeo import osr

sourceSR = osr.SpatialReference()
sourceSR.ImportFromEPSG(32612) #UTM 12N WGS84

targetSR = osr.SpatialReference()
targetSR.ImportFromEPSG(4326) #Geo WGS84

coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)
```

### 对几何对象进行投影变换


```python
print("Projection transform:")
print("Before:", multipoint)

#geom.Transform(coordTrans)
multipoint.Transform(coordTrans)

print("After :", multipoint)
```

    Projection transform:
    Before: MULTIPOINT (-115.489778556511723 0.0 0,-115.489778556511723 0.0 0)
    After : MULTIPOINT (-115.489778556511723 0.0 0,-115.489778556511723 0.0 0)


据说，在windows里面跑不通(http://n2.nabble.com/PROJ-4-EPSG-28992-td2033665.html)  
我在linux（Ubuntu15.04）里面没问题。
#### 另外还有几个要注意的地方：

* 要在适当的时候编辑Geometry，投影变换之后最好就不要再动了吧。  
* 对一个数据源DataSource里面的所有Geometry做投影变换，得一个一个来，用个循环吧。  

### 将投影参数写入.prj文件。
首先MorphToESRI()，转成字符串，然后开个文本文件往里面写就行了。


```python
targetSR.MorphToESRI()
sr_wkt = targetSR.ExportToWkt()
print(sr)

file = open('test.prj', 'w')
file.write(sr_wkt)
file.close()
```

    GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]



```python

```
