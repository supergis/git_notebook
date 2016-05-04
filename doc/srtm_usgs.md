
# SRTM高程数据处理
#### 下载文件、解压，转换为GeoTif, 添加投影信息，渲染三维立体效果图像，生成高程等值线矢量图。
**_ by [openthings@163.com](http://my.oschina.net/u/2306127/blog) _**

## （一）获取数据。

#### 从[USGS](http://dds.cr.usgs.gov/srtm/version2_1/SRTM3)下载数据。


```python
!wget -c http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/Africa/N00E018.hgt.zip
```

    --2016-05-04 14:12:03--  http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/Africa/N00E018.hgt.zip
    正在解析主机 dds.cr.usgs.gov (dds.cr.usgs.gov)... 152.61.133.66, 2001:49c8:4000:124c::66
    正在连接 dds.cr.usgs.gov (dds.cr.usgs.gov)|152.61.133.66|:80... 已连接。
    已发出 HTTP 请求，正在等待回应... 200 OK
    长度： 896459 (875K) [application/zip]
    正在保存至: “N00E018.hgt.zip”
    
    N00E018.hgt.zip     100%[===================>] 875.45K  16.2KB/s    in 98s     
    
    2016-05-04 14:13:48 (8.89 KB/s) - 已保存 “N00E018.hgt.zip” [896459/896459])
    


#### 解压缩得到 *.hgt 文件。


```python
!unzip N00E018.hgt.zip
```

    Archive:  N00E018.hgt.zip
      inflating: N00E018.hgt             


## （二）数据格式和投影转换。

#### 将 *.hgt 转为 GeoTiff。
使用GDAL(http://www.gdal.org) 进行转换。


```python
!gdal_translate -of GTiff -co "TILED=YES" -a_srs "+proj=latlong" N00E018.hgt N00E018_adapted.tif
```

    Input file size is 1201, 1201
    0...10...20...30...40...50...60...70...80...90...100 - done.


#### 地理投影转换。


```python
!gdalwarp -of GTiff -co "TILED=YES" -srcnodata 32767 -t_srs "+proj=merc +ellps=sphere +R=6378137 \
+a=6378137 +units=m" -rcs -order 3 -tr 30 30 -multi N00E018_adapted.tif N00E018_warped.tif
```

    Creating output file that is 3714P x 3714L.
    Processing input file N00E018_adapted.tif.
    Copying nodata values from source N00E018_adapted.tif to destination N00E018_warped.tif.
    0...10...20...30...40...50...60...70...80...90...100 - done.


## （三）立体效果渲染。
#### 从DEM生成Hillshade。


```python
!gdaldem hillshade N00E018_warped.tif N00E018_hillshade.tif
```

    0...10...20...30...40...50...60...70...80...90...100 - done.


## （四）生成等高线。
#### 使用GDAL生成25米等高距的等高线，输出shp格式。


```python
!gdal_contour -a elev N00E018_adapted.tif N00E018_contour25.shp -i 25.0
```

    0...10...20...30...40...50...60...70...80...90...100 - done.


## 查看生成的文件目录。


```python
!ls -l -h 
```

    总用量 53M
    -rw-rw-r-- 1 supermap supermap 3.2M 5月   4 14:18 N00E018_adapted.tif
    -rw-rw-r-- 1 supermap supermap 321K 5月   4 14:32 N00E018_contour25.dbf
    -rw-rw-r-- 1 supermap supermap  144 5月   4 14:32 N00E018_contour25.prj
    -rw-rw-r-- 1 supermap supermap 4.5M 5月   4 14:32 N00E018_contour25.shp
    -rw-rw-r-- 1 supermap supermap 123K 5月   4 14:32 N00E018_contour25.shx
    -rw-r--r-- 1 supermap supermap 2.8M 1月  15  2009 N00E018.hgt
    -rw-rw-r-- 1 supermap supermap 876K 7月  22  2009 N00E018.hgt.zip
    -rw-rw-r-- 1 supermap supermap  14M 5月   4 14:19 N00E018_hillshade.tif
    -rw-rw-r-- 1 supermap supermap  29M 5月   4 14:19 N00E018_warped.tif
    -rw-rw-r-- 1 supermap supermap 5.8K 5月   4 14:32 srtm_usgs.ipynb



```python

```
