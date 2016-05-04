

```python
#!/usr/bin/python
#coding=utf-8
```

# 探索OSM的文件格式(Node对象)。
#### 在线获取[OpenStreetMap](http://www.openstreetmap.org)区域地图数据，转为GeoPandas，并最终转为shp格式文件。
**_ by [openthings@163.com](http://my.oschina.net/u/2306127/blog) _**

** OSM为xml格式，解析文件结构使用强大的requests数据下载包，网页和xml分析神器BeautifulSoup。**
<font color="red">**注意：**由于BeautifulSoup将数据读到内存处理，因此不适合大数据量的处理。</font>


```python
from bs4 import BeautifulSoup as bs
import requests as req
from pprint import *
```

#### 直接下载到内存。不推荐使用，因为如果网络中断，需要重新下载。


```python
url = "http://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145"
try:
    r = req.get(url)
    print(r)
except Exception as ex:
    print("Error:",ex)  
```

#### 使用wget -c下载OSM数据，保存到本地文件，然后载入。


```python
!wget -c -O osm_test.osm "http://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145"
```

    --2016-05-04 14:59:47--  http://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145
    正在解析主机 api.openstreetmap.org (api.openstreetmap.org)... 193.63.75.99, 193.63.75.100, 193.63.75.103, ...
    正在连接 api.openstreetmap.org (api.openstreetmap.org)|193.63.75.99|:80... 已连接。
    已发出 HTTP 请求，正在等待回应... 200 OK
    长度： 未指定 [text/xml]
    正在保存至: “osm_test.osm”
    
    osm_test.osm            [        <=>         ]   2.67M  87.2KB/s    in 39s     
    
    2016-05-04 15:00:27 (71.0 KB/s) - “osm_test.osm” 已保存 [2799533]
    


#### 查看文件列表。可到当前目录去查看内容，由于文件较大，不要在本页面直接打开。


```python
!ls -l -h
```

    总用量 2.8M
    -rw-rw-r-- 1 supermap supermap  24K 5月   4 15:02 osm-discovery.ipynb
    -rw-rw-r-- 1 supermap supermap 5.0K 4月  24 17:45 osm-overpass.ipynb
    -rw-rw-r-- 1 supermap supermap  15K 4月  23 08:23 osm-tag2json.ipynb
    -rw-rw-r-- 1 supermap supermap 2.7M 5月   4 15:00 osm_test.osm


## 直接读取本地文件，获得范围信息。


```python
#bsr = bs(atext,"lxml")
bsr = bs(open("osm_test.osm"),"lxml")

mbr = bsr.find_all('bounds')
print(mbr)
```

    [<bounds maxlat="48.1450000" maxlon="11.5430000" minlat="48.1400000" minlon="11.5400000"></bounds>]


### 获得osm文件中所有的node对象。


```python
nodelist = bsr.find_all('node')

print("All Nodes:",len(nodelist),", list 0-5:")
pprint(nodelist[0:5])
```

    All Nodes: 1864 , list 0-5:
    [<node changeset="34651972" id="398692" lat="48.1452196" lon="11.5414971" timestamp="2015-10-15T10:53:28Z" uid="2290263" user="soemisch" version="20" visible="true">
    <tag k="tmc" v="DE:35375"></tag>
    </node>,
     <node changeset="34904180" id="1956100" lat="48.1434822" lon="11.5487963" timestamp="2015-10-27T14:01:37Z" uid="2385132" user="MENTZ_TU" version="43" visible="true">
    <tag k="tmc" v="DE:61453"></tag>
    <tag k="TMC:cid_58:tabcd_1:Class" v="Point"></tag>
    <tag k="TMC:cid_58:tabcd_1:Direction" v="positive"></tag>
    <tag k="TMC:cid_58:tabcd_1:LCLversion" v="9.00"></tag>
    <tag k="TMC:cid_58:tabcd_1:LocationCode" v="35356"></tag>
    <tag k="TMC:cid_58:tabcd_1:NextLocationCode" v="35357"></tag>
    <tag k="TMC:cid_58:tabcd_1:PrevLocationCode" v="35355"></tag>
    </node>,
     <node changeset="10842011" id="21565151" lat="48.1414994" lon="11.5522715" timestamp="2012-03-01T20:37:08Z" uid="342705" user="KonB" version="4" visible="true"></node>,
     <node changeset="9695595" id="21585828" lat="48.1445431" lon="11.5384205" timestamp="2011-10-30T16:47:12Z" uid="534662" user="Q12" version="17" visible="true"></node>,
     <node changeset="9883923" id="60300474" lat="48.1406915" lon="11.5502820" timestamp="2011-11-20T13:24:04Z" uid="64536" user="Michael Forster" version="4" visible="true"></node>]


### 查看node的数据结构。


```python
node = nodelist[0]
print(node)
```

    <node changeset="34651972" id="398692" lat="48.1452196" lon="11.5414971" timestamp="2015-10-15T10:53:28Z" uid="2290263" user="soemisch" version="20" visible="true">
    <tag k="tmc" v="DE:35375"></tag>
    </node>



```python
node.attrs
```




    {'changeset': '34651972',
     'id': '398692',
     'lat': '48.1452196',
     'lon': '11.5414971',
     'timestamp': '2015-10-15T10:53:28Z',
     'uid': '2290263',
     'user': 'soemisch',
     'version': '20',
     'visible': 'true'}



### 解析Node的属性，以K:V存储的值。


```python
for (k,v) in node.attrs.items():
    print(k,":",v)
```

    lon : 11.5414971
    user : soemisch
    timestamp : 2015-10-15T10:53:28Z
    id : 398692
    uid : 2290263
    version : 20
    visible : true
    changeset : 34651972
    lat : 48.1452196


### 将nodelist转换为Pandas.DataFrame，为了便于显示，只处理了5个node。


```python
import pandas as pd
nodelist2 = []
for node in nodelist[0:10]:
    nodelist2.append(node.attrs)
#print(nodelist2)

df = pd.DataFrame(nodelist2)
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>changeset</th>
      <th>id</th>
      <th>lat</th>
      <th>lon</th>
      <th>timestamp</th>
      <th>uid</th>
      <th>user</th>
      <th>version</th>
      <th>visible</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>34651972</td>
      <td>398692</td>
      <td>48.1452196</td>
      <td>11.5414971</td>
      <td>2015-10-15T10:53:28Z</td>
      <td>2290263</td>
      <td>soemisch</td>
      <td>20</td>
      <td>true</td>
    </tr>
    <tr>
      <th>1</th>
      <td>34904180</td>
      <td>1956100</td>
      <td>48.1434822</td>
      <td>11.5487963</td>
      <td>2015-10-27T14:01:37Z</td>
      <td>2385132</td>
      <td>MENTZ_TU</td>
      <td>43</td>
      <td>true</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10842011</td>
      <td>21565151</td>
      <td>48.1414994</td>
      <td>11.5522715</td>
      <td>2012-03-01T20:37:08Z</td>
      <td>342705</td>
      <td>KonB</td>
      <td>4</td>
      <td>true</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9695595</td>
      <td>21585828</td>
      <td>48.1445431</td>
      <td>11.5384205</td>
      <td>2011-10-30T16:47:12Z</td>
      <td>534662</td>
      <td>Q12</td>
      <td>17</td>
      <td>true</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9883923</td>
      <td>60300474</td>
      <td>48.1406915</td>
      <td>11.5502820</td>
      <td>2011-11-20T13:24:04Z</td>
      <td>64536</td>
      <td>Michael Forster</td>
      <td>4</td>
      <td>true</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2434259</td>
      <td>256554156</td>
      <td>48.1431978</td>
      <td>11.5197388</td>
      <td>2009-09-10T10:34:54Z</td>
      <td>127922</td>
      <td>w3box</td>
      <td>4</td>
      <td>true</td>
    </tr>
    <tr>
      <th>6</th>
      <td>11085110</td>
      <td>256554158</td>
      <td>48.1432360</td>
      <td>11.5170168</td>
      <td>2012-03-24T14:42:27Z</td>
      <td>342705</td>
      <td>KonB</td>
      <td>5</td>
      <td>true</td>
    </tr>
    <tr>
      <th>7</th>
      <td>9505942</td>
      <td>256554152</td>
      <td>48.1420008</td>
      <td>11.5383182</td>
      <td>2011-10-08T19:22:24Z</td>
      <td>334153</td>
      <td>Alexander Roalter</td>
      <td>4</td>
      <td>true</td>
    </tr>
    <tr>
      <th>8</th>
      <td>30794039</td>
      <td>1423405650</td>
      <td>48.1398728</td>
      <td>11.5447444</td>
      <td>2015-05-04T23:26:30Z</td>
      <td>354141</td>
      <td>Anoniman</td>
      <td>2</td>
      <td>true</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9212407</td>
      <td>1423405651</td>
      <td>48.1399051</td>
      <td>11.5444005</td>
      <td>2011-09-04T20:47:20Z</td>
      <td>17085</td>
      <td>cfaerber</td>
      <td>1</td>
      <td>true</td>
    </tr>
  </tbody>
</table>
</div>



### 将Pandas.DataFrame转为GeoPandas.DataFrame，点生成为GeoSeries。  
**注意:** 需要安装shapely和geopandas包。在anaconda先运行source activate GISpark，然后安装：  
```
conda install -y -c https://conda.anaconda.org/conda-forge fiona  
conda install -y -c https://conda.anaconda.org/conda-forge gdal  
conda install -y -c https://conda.anaconda.org/conda-forge geopandas  
conda install -y -c https://conda.anaconda.org/conda-forge geojson 
```


```python
from shapely.geometry import (Point, LinearRing, LineString, Polygon, MultiPoint)
from geopandas import GeoSeries, GeoDataFrame
from geopandas.base import GeoPandasBase

def node2pandas(nodelist):
    nodelist2 = []
    for node in nodelist[0:10]:
        nodelist2.append(node.attrs)
    df = pd.DataFrame(nodelist2)
    return df

def pandas2geopandas(nodelist):
    pass

def node2geopandas(nodelist):
    df = node2pandas(nodelist)

    ps = []
    ps0 = [1]
    for index, row in df.iterrows():
        #print(index,':',row['lat'],'-',row['lon'])
        ps0[0] = Point(float(row['lon']),float(row['lat']))
        ps.append(ps0[0])

    gs = GeoSeries(ps,crs={'init': 'epsg:4326', 'no_defs': True})        
    geodf = GeoDataFrame({'id' : df["id"],'user' : df["id"], 
                        'lon' : df["lon"],'lat' : df["lat"],
                        'timestamp' : df["timestamp"],'uid' : df["uid"],'version' : df["version"],
                        'geometry' : gs
                        })
    return geodf
```


```python
gdf = node2geopandas(nodelist)
gdf
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>geometry</th>
      <th>id</th>
      <th>lat</th>
      <th>lon</th>
      <th>timestamp</th>
      <th>uid</th>
      <th>user</th>
      <th>version</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>POINT (11.5414971 48.1452196)</td>
      <td>398692</td>
      <td>48.1452196</td>
      <td>11.5414971</td>
      <td>2015-10-15T10:53:28Z</td>
      <td>2290263</td>
      <td>398692</td>
      <td>20</td>
    </tr>
    <tr>
      <th>1</th>
      <td>POINT (11.5487963 48.1434822)</td>
      <td>1956100</td>
      <td>48.1434822</td>
      <td>11.5487963</td>
      <td>2015-10-27T14:01:37Z</td>
      <td>2385132</td>
      <td>1956100</td>
      <td>43</td>
    </tr>
    <tr>
      <th>2</th>
      <td>POINT (11.5522715 48.1414994)</td>
      <td>21565151</td>
      <td>48.1414994</td>
      <td>11.5522715</td>
      <td>2012-03-01T20:37:08Z</td>
      <td>342705</td>
      <td>21565151</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>POINT (11.5384205 48.1445431)</td>
      <td>21585828</td>
      <td>48.1445431</td>
      <td>11.5384205</td>
      <td>2011-10-30T16:47:12Z</td>
      <td>534662</td>
      <td>21585828</td>
      <td>17</td>
    </tr>
    <tr>
      <th>4</th>
      <td>POINT (11.550282 48.1406915)</td>
      <td>60300474</td>
      <td>48.1406915</td>
      <td>11.5502820</td>
      <td>2011-11-20T13:24:04Z</td>
      <td>64536</td>
      <td>60300474</td>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>POINT (11.5197388 48.1431978)</td>
      <td>256554156</td>
      <td>48.1431978</td>
      <td>11.5197388</td>
      <td>2009-09-10T10:34:54Z</td>
      <td>127922</td>
      <td>256554156</td>
      <td>4</td>
    </tr>
    <tr>
      <th>6</th>
      <td>POINT (11.5170168 48.143236)</td>
      <td>256554158</td>
      <td>48.1432360</td>
      <td>11.5170168</td>
      <td>2012-03-24T14:42:27Z</td>
      <td>342705</td>
      <td>256554158</td>
      <td>5</td>
    </tr>
    <tr>
      <th>7</th>
      <td>POINT (11.5383182 48.1420008)</td>
      <td>256554152</td>
      <td>48.1420008</td>
      <td>11.5383182</td>
      <td>2011-10-08T19:22:24Z</td>
      <td>334153</td>
      <td>256554152</td>
      <td>4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>POINT (11.5447444 48.1398728)</td>
      <td>1423405650</td>
      <td>48.1398728</td>
      <td>11.5447444</td>
      <td>2015-05-04T23:26:30Z</td>
      <td>354141</td>
      <td>1423405650</td>
      <td>2</td>
    </tr>
    <tr>
      <th>9</th>
      <td>POINT (11.5444005 48.1399051)</td>
      <td>1423405651</td>
      <td>48.1399051</td>
      <td>11.5444005</td>
      <td>2011-09-04T20:47:20Z</td>
      <td>17085</td>
      <td>1423405651</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### 保存为shape格式文件。


```python
filename = "osm_test.shp"
gdf.to_file(filename)
```

### 查看一下文件列表。


```python
!ls -l -h
```

    总用量 2.8M
    -rw-rw-r-- 1 supermap supermap  25K 5月   4 15:17 osm-discovery.ipynb
    -rw-rw-r-- 1 supermap supermap 5.0K 4月  24 17:45 osm-overpass.ipynb
    -rw-rw-r-- 1 supermap supermap  15K 4月  23 08:23 osm-tag2json.ipynb
    -rw-rw-r-- 1 supermap supermap   10 5月   4 15:17 osm_test.cpg
    -rw-rw-r-- 1 supermap supermap 5.8K 5月   4 15:17 osm_test.dbf
    -rw-rw-r-- 1 supermap supermap 2.7M 5月   4 15:00 osm_test.osm
    -rw-rw-r-- 1 supermap supermap  380 5月   4 15:17 osm_test.shp
    -rw-rw-r-- 1 supermap supermap  180 5月   4 15:17 osm_test.shx



```python

```
