

```python
#!/usr/bin/python
#coding=utf-8
```

### OSM-overpass服务接口使用，在线查询[OpenStreetMap](http:www.openstreetmap.org)开放空间数据库。
**_ by [openthings@163.com](http://my.oschina.net/u/2306127/blog), 2016-04-23. _**  
>#### overpy-使用overpass api接口的python library，这里将返回结果集保存为JSON格式。  
* 安装：$ pip install overpy
* 文档：http://python-overpy.readthedocs.org/en/latest/example.html#basic-example  
* 接口：http://wiki.openstreetmap.org/wiki/Overpass_API  
本工具例程基于上述文档例程进行编写。 


```python
import os, sys, gc
import time
import json

import overpy
from pprint import *
```

### 调用overpass接口，获取result数据结果集。
* 由于通过网络返回，容易中断，而且是在内存中处理，不适合创建大的查询集。


```python
#范围：纬度1，经度1，纬度2，经度2
#返回：result
def get_osm():
    query = "[out:json];node(50.745,7.17,50.75,7.18);out;"
    osm_op_api = overpy.Overpass()
    result = osm_op_api.query(query)

    print("Nodes: ",len(result.nodes))
    print("Ways: ",len(result.ways))
    print("Relations: ",len(result.relations))
    return result
```

### 在线获取osm数据.


```python
result = get_osm()
```

    Nodes:  2267
    Ways:  0
    Relations:  0


#### 显示node的属性信息（仅显示前3个node的信息）。


```python
nodeset = result.nodes[0:3]
pprint(nodeset)
```

    [<overpy.Node id=50878400 lat=50.7461788 lon=7.1742257>,
     <overpy.Node id=50878401 lat=50.7476027 lon=7.1744795>,
     <overpy.Node id=100792806 lat=50.7486483 lon=7.1714704>]


#### 遍历node的子集，该子集由上一步产生。


```python
for n in nodeset:
    print(n.id,n.lat,n.lon)
```

    50878400 50.7461788 7.1742257
    50878401 50.7476027 7.1744795
    100792806 50.7486483 7.1714704


### 将查询到的数据集合转换为json格式，写入json格式的文件.
（_ 该格式可由Spark直接载入: SQLContext.read.json()_ ）。


```python
def node2json(node):
    jsonNode="{\"id\":\"%s\", \"lat\":\"%s\", \"lon\":\"%s\"}"%(node.id,node.lat,node.lon)
    return jsonNode

def node2jsonfile(fname,nodeset):
    fnode = open(fname,"w+")
    for n in nodeset:
        jn = node2json(n) + "\n"
        fnode.write(jn)
    fnode.close()
    print("Nodes:",len(nodeset),", Write to: ",fname)
```

#### 执行json文件保存操作。


```python
node2jsonfile("overpass.osm_node.json",result.nodes)    
```

    Nodes: 2267 , Write to:  overpass.osm_node.json


#### 查看一下文件。


```python
!ls -l -h
```

    总用量 2.9M
    -rw-rw-r-- 1 supermap supermap  26K 5月   4 15:20 osm-discovery.ipynb
    -rw-rw-r-- 1 supermap supermap 5.6K 5月   4 15:27 osm-overpass.ipynb
    -rw-rw-r-- 1 supermap supermap  15K 4月  23 08:23 osm-tag2json.ipynb
    -rw-rw-r-- 1 supermap supermap   10 5月   4 15:17 osm_test.cpg
    -rw-rw-r-- 1 supermap supermap 5.8K 5月   4 15:17 osm_test.dbf
    -rw-rw-r-- 1 supermap supermap 2.7M 5月   4 15:00 osm_test.osm
    -rw-rw-r-- 1 supermap supermap  380 5月   4 15:17 osm_test.shp
    -rw-rw-r-- 1 supermap supermap  180 5月   4 15:17 osm_test.shx
    -rw-rw-r-- 1 supermap supermap 131K 5月   4 15:27 overpass.osm_node.json



```python

```
