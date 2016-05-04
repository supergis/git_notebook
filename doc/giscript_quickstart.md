
# GIScript－开放地理空间信息处理与分析Python库
**GIScript**是一个开放的地理空间心处理与分析Python框架，GIS内核采用SuperMap UGC封装，集成多种开源软件，也可以使用其它的商业软件引擎。  
_ by wangerqi@supermap.com, 2016-05-03。_

#### 本文档介绍GIScript的安装和配置，并进行简单的运行测试，以确认安装的软件正常运行。
* 本教程基于Anaconda3+python3.5.1科学计算环境，请参考：http://www.anaconda.org 。
* 本Notebook在Ubuntu 14.04/15.10/16.04运行通过，在本地服务器和阿里云服务器都可以运行。
* 可以在[NBViewer上直接访问和下载本文档](http://nbviewer.jupyter.org/github/supergis/git_notebook/blob/master/geospatial/giscript/giscript_quickstart.ipynb
)。

## （一）安装与配置
GIScript的安装包括<font color="blue">**系统库的设置**、**UGC Runtime设置**和**Python库**</font>的设置，通过编写一个启动脚本，可以在给定环境下载入相应的运行库的路径。
#### 1、下载GIScript支持库：
```
cd /home/supermap/GISpark
git clone https://github.com/supergis/GIScriptLib.git
```

#### 2、UGC系统库的版本适配。
由于GIScript的几个编译库版本较新，在默认使用系统老版本库时部分函数找不到会引起调用失败，因此需要将这几个的系统调用指向到GIScript编译使用的的新版本。在Ubuntu上，具体操作包括：
```
cd ~/anaconda3/envs/GISpark/lib
mv libstdc++.so libstdc++.so.x
mv libstdc++.so.6 libstdc++.so.6.x
mv libsqlite3.so.0 libsqlite3.so.0.x
mv libsqlite3.so libsqlite3.so.x
mv libgomp.so.1.0.0 libgomp.so.1.0.0.x
mv libgomp.so.1 libgomp.so.1.x
mv libgomp.so libgomp.so.x
```
* _可以运行GIScriptLib/lib-giscript-x86-linux64/下的setup-giscript.sh来自动处理(请根据自己的目录布局修改路径)。_
* _由于不同系统安装的软件和版本不同，如果还有其它的动态库冲突，可以使用ldd \*.so来查看库的依赖关系，按照上述办法解决。_

#### 3、安装Python的支持库。
GIScript的Python封装库，默认存放在系统目录：/usr/lib/python3/dist-packages/PyUGC  
使用Anaconda时，存在相应的env的目录下，如：[/home/supermap/Anaconda3]/envs/GISpark/lib/python3.5/site-packages    
* **安装方法一：链接。**在[...]/python3.5/site-packages下建立PyUGC的软连接。注意，原文件不可删除，否则就找不到了。
```
ln -s -f /home/supermap/GISpark/GIScriptLib/lib-giscript-x86-linux64/lib ~/anaconda3/envs/GISpark/lib/python3.5/site-packages/PyUGC
```
* **安装方法二：复制。**将lib-giscript-x86-linux64/lib（Python的UGC封装库）复制为Python下的site-packages/PyUGC目录，如下： 
```
cd /home/supermap/GISpark/GIScriptLib
cp -r lib-giscript-x86-linux64/lib ~/anaconda3/envs/GISpark/lib/python3.5/site-packages/PyUGC
```

#### 4、Jupyter启动之前，设置GIScript运行时 library 载入的路径:
*  **编写脚本，启动前设置GIScript的运行时动态库路径，内容如下：**  

```
echo "Config GIScript2016..."

# 使用GIScript2015的开发工程目录，配置示例：
# export SUPERMAP_HOME=/home/supermap/GIScript/GIScript2015/Linux64-gcc4.9

# 使用GIScriptLib运行时动态库，配置如下：
export SUPERMAP_HOME=/home/supermap/GISpark/GIScriptLib/lib-giscript-x86-linux64
export LD_LIBRARY_PATH=$SUPERMAP_HOME/Bin:$LD_LIBRARY_PATH
echo "Config: LD_LIBRARY_PATH＝"$LD_LIBRARY_PATH
```

* **将上面的内容与Jupyter启动命令放到start.sh脚本中，如下:**

```
echo "Activate conda enviroment GISpark ..."
source activate GISpark

echo "Config GIScript 2016 for Jupyter ..."
export SUPERMAP_HOME=/home/supermap/GISpark/GIScriptLib/lib-giscript-x86-linux64
export LD_LIBRARY_PATH=$SUPERMAP_HOME/bin:/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH
echo "Config: LD_LIBRARY_PATH="$LD_LIBRARY_PATH

echo "Start Jupyter notebook"
jupyter notebook
```

* **修改start.sh执行权限，运行Jupyter Notebook。**
```
sudo chmod +x start.sh
./start.sh
```

默认配置下，将会自动打开浏览器，就可以开始使用Jupyter Notebook并调用GIScript的库了。   
如果通过服务器使用，需要使用｀jupyter notebook --generate-config｀创建配置文件，然后进去修改参数，这里不再详述。

## （二）运行测试，导入一些数据。
#### 1、导入GIScript的Python库。


```python
from PyUGC import *  
from PyUGC.Stream import UGC  
from PyUGC.Base import OGDC  
from PyUGC import Engine  
from PyUGC import FileParser  
from PyUGC import DataExchange  

import datasource
```

##### 2、使用Python的help(...)查看库的元数据信息获得帮助。


```python
#help(UGC)
#help(OGDC)
#help(datasource)
```

#### 3、设置测试数据目录。


```python
import os

basepath = os.path.join(os.getcwd(),"../data")
print("Data path: ", basepath)

file1 = basepath + u"/Shape/countries.shp"
print("Data file: ", file1)

file2 = basepath + u"/Raster/astronaut(CMYK)_32.tif"
print("Data file: ", file2)

file3 = basepath + u"/Grid/grid_Int32.grd"
print("Data file: ", file3)

datapath_out = basepath + u"/GIScript_Test.udb"
print("Output UDB: ",datapath_out)
```

    Data path:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data
    Data file:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Shape/countries.shp
    Data file:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Raster/astronaut(CMYK)_32.tif
    Data file:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Grid/grid_Int32.grd
    Output UDB:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/GIScript_Test.udb


#### 4、导入数据的测试函数。


```python
def Import_Test():
    print("Export to UDB: ",datapath_out)
    ds = datasource.CreateDatasource(UGC.UDB,datapath_out)
    datasource.ImportVector(file1,ds)
    datasource.ImportRaster(file2,ds)
    datasource.ImportGrid(file3,ds)
    ds.Close()
    del ds
    print("Finished.")
```

#### 5、运行这个测试。


```python
try:
    Import_Test()
except Exception as ex:
    print(ex)
    
```

    Export to UDB:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/GIScript_Test.udb
    创建数据源成功！！
    Import Vector:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Shape/countries.shp
    数据导入成功:Import Vector /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Shape/countries.shp
    Import Raster:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Raster/astronaut(CMYK)_32.tif
    数据导入成功:Import Image /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Raster/astronaut(CMYK)_32.tif
    Import Grid:  /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Grid/grid_Int32.grd
    数据导入成功:Import Grid /home/supermap/GISpark/git_notebook/geospatial/giscript/../data/Grid/grid_Int32.grd
    Finished.


## （三）查看生成的数据源文件UDB。
### 下面使用了<font color="green">IPython的Magic操作符 !</font>，可以直接运行操作系统的Shell命令行。


```python
!ls -l -h ../data/GIScript_Test.*
```

    -rw-rw-r-- 1 supermap supermap 5.6M 5月   4 09:46 ../data/GIScript_Test.udb
    -rw-r--r-- 1 supermap supermap  74K 5月   4 09:46 ../data/GIScript_Test.udd


### <font color="red">删除生成的测试文件。注意，不要误删其它文件！</font>
如果重复运行上面的Import_Test()将会发现GIScript_Test.udb和GIScript_Test.udd文件会不断增大。  
但是打开UDB文件却只有一份数据，为什么呢？
* **因为UDB文件是增量存储的，不用的存储块需要使用SQLlite的存储空间紧缩处理才能回收。**


```python
!rm ../data/GIScript_Test.*
```

#### 再次查看目录，文件是否存在。


```python
!ls -l -h ../data/GIScript_Test.*
```

    -rw-rw-r-- 1 supermap supermap  12M 5月   4 09:44 ../data/GIScript_Test.udb
    -rw-r--r-- 1 supermap supermap 122K 5月   4 09:44 ../data/GIScript_Test.udd



```python

```
