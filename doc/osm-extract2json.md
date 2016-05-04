

```python
#!/usr/bin/python
#coding=utf-8
```

# [OpenStreetMap](http://www.openstreetmap.org)的OSM文件对象数据分类捡取器

by [openthings@163.com](http://my.oschina.net/u/2306127/blog?catalog=3420733), 2016-03-21.   

### 功能：
* **输出三个单行存储的json文件，可在[Spark](http://spark.apache.org)中使用，通过spark的sc.read.json()直接读入处理。** 
* **本工具将osm文件按照tag快速分类，直接转为node/way/relation三个json文件，并按行存储。**

### 说明：
* Spark默认按行处理，因此处理xml尤其是多行XML比较麻烦，如OpenStreetMap的OSM格式。  
* 对于xml文件较大、无法全部载入内存的情况，需要预处理成行方式，然后在Spark中分布式载入。  


#### 后续工作：
    1、映射way的nd节点坐标，构建出几何对象的坐标串。  
    2、每一几何对象数据转为wkt格式，保存到JSON的geometry域。  
    3、数据表按区域分割后，转为GeoPandas，然后进一步转为shape file。

### XML快速转为JSON格式，使用lxml进行流式处理。
* 流方式递归读取xml结构数据（占用资源少）: http://www.ibm.com/developerworks/xml/library/x-hiperfparse/  
* XML字符串转为json对象支持库 : https://github.com/martinblech/xmltodict  
>* xmltodict.parse()会将字段名输出添加@和#，在Spark查询中会引起问题，需要去掉。如下设置即可： 
```
xmltodict.parse(elem_data,attr_prefix="",cdata_key="")
```
>* 编码和错误xml文件恢复，如下：
```
magical_parser = lxml.etree.XMLParser(encoding='utf-8', recover=True)  
tree = etree.parse(StringIO(your_xml_string), magical_parser) #or pass in an open file object
```
>* 先将element转为string，然后生成dict，再用json.dump()产生json字符串。
```
elem_data = etree.tostring(elem)
elem_dict = xmltodict.parse(elem_data)
elem_jsonStr = json.dumps(elem_dict)
``` 
>* 可以使用json.loads(elem_jsonStr)创建出可编程的json对象。


```python
import os
import time
import json
from pprint import *

import lxml
from lxml import etree
import xmltodict, sys, gc
from pymongo import MongoClient

gc.enable() #Enable Garbadge Collection

# 将指定tag的对象提取，写入json文件。 
def process_element(elem):
    elem_data = etree.tostring(elem)
    elem_dict = xmltodict.parse(elem_data,attr_prefix="",cdata_key="")
    #print(elem_dict)
    
    if (elem.tag == "node"): 
        elem_jsonStr = json.dumps(elem_dict["node"])
        fnode.write(elem_jsonStr + "\n")
    elif (elem.tag == "way"): 
        elem_jsonStr = json.dumps(elem_dict["way"])
        fway.write(elem_jsonStr + "\n")
    elif (elem.tag == "relation"): 
        elem_jsonStr = json.dumps(elem_dict["relation"])
        frelation.write(elem_jsonStr + "\n")

# 遍历所有对象，然后调用process_element处理。
# 迭代处理，func为迭代的element处理函数。
def fast_iter(context, func_element, maxline):
    placement = 0
    try:
        for event, elem in context:
            placement += 1
            if (maxline > 0):  # 最多的转换对象限制，大数据调试时使用于抽样检查。 
                print(etree.tostring(elem))
                if (placement >= maxline): break

            func_element(elem)  #处理每一个元素,调用process_element.      
            elem.clear()
            while elem.getprevious() is not None:
               del elem.getparent()[0]
    except Exception as ex:
        print(time.strftime(ISOTIMEFORMAT),", Error:",ex)
        
    del context
```

### 执行osm的xml到json转换，一次扫描提取为三个文件。  
* context = etree.iterparse(osmfile,tag=["node","way"])的**tag**参数必须要给值，否则取出来的sub element全部是none。  
* 使用了3个打开的全局文件：fnode、fway、frelation


```python
#maxline = 0  #抽样调试使用，最多转换的对象，设为0则转换文件的全部。
def transform(osmfile,maxline = 0):
    ISOTIMEFORMAT="%Y-%m-%d %X"
    print(time.strftime( ISOTIMEFORMAT),", Process osm XML...",osmfile," =>MaxLine:",maxline)

    global fnode
    global fway
    global frelation
    
    fnode = open(osmfile + "_node.json","w+")
    fway = open(osmfile + "_way.json","w+")
    frelation = open(osmfile + "_relation.json","w+")

    context = etree.iterparse(osmfile,tag=["node","way","relation"])
    fast_iter(context, process_element, maxline)

    fnode.close()
    fway.close()
    frelation.close()

    print(time.strftime( ISOTIMEFORMAT),", OSM to JSON, Finished.")
```

## 执行转换。


```python
# 需要处理的osm文件名，自行修改。
osmfile = '../data/osm/muenchen.osm'
transform(osmfile,0)
```

    2016-05-04 16:18:37 , Process osm XML... ../data/osm/muenchen.osm  =>MaxLine: 0
    2016-05-04 16:18:38 , Error: attributes construct error, line 51046, column 44
    2016-05-04 16:18:38 , OSM to JSON, Finished.


### 保存到MongoDB等其它存储系统(待续)。
client = MongoClient()
db = client.re
streetsDB = db.streets
hwTypes = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'pedestrian', 'unclassified', 'service']
