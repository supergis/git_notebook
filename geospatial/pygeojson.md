
# GeoJSON的python支持库。
[openthings@163.com](http://my.oschina.net/u/2306127/blog?catalog=3420733), 2016-04.   
* IETF标准项目：https://github.com/geojson  
* PyPi支持库: https://pypi.python.org/pypi/geojson  
* 其它的支持库包括：GeoPandas, Shaply, GDAL, GIScript


```python
from pprint import * 
```

## Installation

python-geojson is compatible with Python 2.6, 2.7, 3.2, 3.3, and 3.4. 
It is listed on PyPi as ‘geojson’. The recommended way to install is via pip:

>pip install geojson

## GeoJSON Objects

This library implements all the GeoJSON Objects described in The GeoJSON Format Specification.

## Point


```python
from geojson import Point

Point((-115.81, 37.24))  # doctest: +ELLIPSIS
```




    {"coordinates": [-115.81, 37.24], "type": "Point"}



Visualize the result of the example above here. General information about Point can be found in Section 2.1.2 and Appendix A: Point within The GeoJSON Format Specification.
## MultiPoint


```python
from geojson import MultiPoint

MultiPoint([(-155.52, 19.61), (-156.22, 20.74), (-157.97, 21.46)])  # doctest: +ELLIPSIS
#{"coordinates": [[-155.5..., 19.6...], [-156.2..., 20.7...], [-157.9..., 21.4...]], "type": "MultiPoint"}
```




    {"coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]], "type": "MultiPoint"}



Visualize the result of the example above here. General information about MultiPoint can be found in Section 2.1.3 and Appendix A: MultiPoint within The GeoJSON Format Specification.
## LineString


```python
from geojson import LineString

lstring = LineString([(8.919, 44.4074), (8.923, 44.4075)])  # doctest: +ELLIPSIS
#{"coordinates": [[8.91..., 44.407...], [8.92..., 44.407...]], "type": "LineString"}

pprint(lstring)
```

    {"coordinates": [[8.919, 44.4074], [8.923, 44.4075]], "type": "LineString"}


Visualize the result of the example above here. General information about LineString can be found in Section 2.1.4 and Appendix A: LineString within The GeoJSON Format Specification.
## MultiLineString


```python
from geojson import MultiLineString

mlstring = MultiLineString([
[(3.75, 9.25), (-130.95, 1.52)],
[(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
])  # doctest: +ELLIPSIS
#{"coordinates": [[[3.7..., 9.2...], [-130.9..., 1.52...]], [[23.1..., -34.2...],
#[-1.3..., -4.6...], [3.4..., 77.9...]]], "type": "MultiLineString"}

pprint(mlstring)
```

    {'coordinates': [[(3.75, 9.25), (-130.95, 1.52)],
                     [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]],
     'type': 'MultiLineString'}


Visualize the result of the example above here. General information about MultiLineString can be found in Section 2.1.5 and Appendix A: MultiLineString within The GeoJSON Format Specification.
## Polygon


```python
from geojson import Polygon

# no hole within polygon
polya = Polygon([[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)]])  # doctest: +ELLIPSIS
#{"coordinates": [[[2.3..., 57.32...], [23.19..., -20.2...], [-120.4..., 19.1...]]], "type": "Polygon"}

pprint(polya)

# hole within polygon
polyb = Polygon([
[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15), (2.38, 57.322)],
[(-5.21, 23.51), (15.21, -10.81), (-20.51, 1.51), (-5.21, 23.51)]
])  # doctest: +ELLIPSIS
#{"coordinates": [[[2.3..., 57.32...], [23.19..., -20.2...], [-120.4..., 19.1...]], 
#[[-5.2..., 23.5...], [15.2..., -10.8...], [-20.5..., 1.5...], [-5.2..., 23.5...]]], "type": "Polygon"}

pprint(polyb)
```

    {'coordinates': [[(2.38, 57.322),
                      (23.194, -20.28),
                      (-120.43, 19.15),
                      (2.38, 57.322)]],
     'type': 'Polygon'}
    {'coordinates': [[(2.38, 57.322),
                      (23.194, -20.28),
                      (-120.43, 19.15),
                      (2.38, 57.322)],
                     [(-5.21, 23.51),
                      (15.21, -10.81),
                      (-20.51, 1.51),
                      (-5.21, 23.51)]],
     'type': 'Polygon'}


Visualize the results of the example above here. General information about Polygon can be found in Section 2.1.6 and Appendix A: Polygon within The GeoJSON Format Specification.
## MultiPolygon


```python
from geojson import MultiPolygon

mp = MultiPolygon([
([(3.78, 9.28), (-130.91, 1.52), (35.12, 72.234), (3.78, 9.28)],),
([(23.18, -34.29), (-1.31, -4.61), (3.41, 77.91), (23.18, -34.29)],)
])  # doctest: +ELLIPSIS

#{"coordinates": [[[[3.7..., 9.2...], [-130.9..., 1.5...], [35.1..., 72.23...]]], 
#[[[23.1..., -34.2...], [-1.3..., #-4.6...], [3.4..., 77.9...]]]], "type": "MultiPolygon"}

pprint(mp)
```

    {'coordinates': [([(3.78, 9.28),
                       (-130.91, 1.52),
                       (35.12, 72.234),
                       (3.78, 9.28)],),
                     ([(23.18, -34.29),
                       (-1.31, -4.61),
                       (3.41, 77.91),
                       (23.18, -34.29)],)],
     'type': 'MultiPolygon'}


Visualize the result of the example above here. General information about MultiPolygon can be found in Section 2.1.7 and Appendix A: MultiPolygon within The GeoJSON Format Specification.
## GeometryCollection


```python
from geojson import GeometryCollection, Point, LineString

my_point = Point((23.532, -63.12))

my_line = LineString([(-152.62, 51.21), (5.21, 10.69)])

gc = GeometryCollection([my_point, my_line])  # doctest: +ELLIPSIS
#{"geometries": [{"coordinates": [23.53..., -63.1...], "type": "Point"}, 
#{"coordinates": [[-152.6..., 51.2...], [5.2..., 10.6...]], "type": "LineString"}], "type": "GeometryCollection"}

pprint(gc)
```

    {'geometries': [{"coordinates": [23.532, -63.12], "type": "Point"},
                    {'coordinates': [(-152.62, 51.21), (5.21, 10.69)],
                     'type': 'LineString'}],
     'type': 'GeometryCollection'}


Visualize the result of the example above here. General information about GeometryCollection can be found in Section 2.1.8 and Appendix A: GeometryCollection within The GeoJSON Format Specification.
## Feature


```python
from geojson import Feature, Point

my_point = Point((-3.68, 40.41))

f1 = Feature(geometry=my_point)  # doctest: +ELLIPSIS
#{"geometry": {"coordinates": [-3.68..., 40.4...], "type": "Point"}, "properties": {}, "type": "Feature"}
pprint(f1)

f2 = Feature(geometry=my_point, properties={"country": "Spain"})  # doctest: +ELLIPSIS
#{"geometry": {"coordinates": [-3.68..., 40.4...], "type": "Point"}, "properties": {"country": "Spain"}, 
#"type": "Feature"}
pprint(f2)

f3 = Feature(geometry=my_point, id=27)  # doctest: +ELLIPSIS
#{"geometry": {"coordinates": [-3.68..., 40.4...], "type": "Point"}, "id": 27, "properties": {}, "type": "Feature"}
pprint(f3)
```

    {'geometry': {"coordinates": [-3.68, 40.41], "type": "Point"},
     'properties': {},
     'type': 'Feature'}
    {'geometry': {"coordinates": [-3.68, 40.41], "type": "Point"},
     'properties': {'country': 'Spain'},
     'type': 'Feature'}
    {'geometry': {"coordinates": [-3.68, 40.41], "type": "Point"},
     'id': 27,
     'properties': {},
     'type': 'Feature'}


Visualize the results of the examples above here. General information about Feature can be found in Section 2.2 within The GeoJSON Format Specification.
## FeatureCollection


```python
from geojson import Feature, Point, FeatureCollection

my_feature = Feature(geometry=Point((1.6432, -19.123)))

my_other_feature = Feature(geometry=Point((-80.234, -22.532)))

fc = FeatureCollection([my_feature, my_other_feature])  # doctest: +ELLIPSIS
#{"features": [{"geometry": {"coordinates": [1.643..., -19.12...], "type": "Point"}, "properties": {}, "type": #"Feature"}, {"geometry": {"coordinates": [-80.23..., -22.53...], "type": "Point"}, "properties": {}, "type": #"Feature"}], "type": "FeatureCollection"}

pprint(fc)
```

    {'features': [{'geometry': {"coordinates": [1.6432, -19.123], "type": "Point"},
                   'properties': {},
                   'type': 'Feature'},
                  {'geometry': {"coordinates": [-80.234, -22.532], "type": "Point"},
                   'properties': {},
                   'type': 'Feature'}],
     'type': 'FeatureCollection'}


Visualize the result of the example above here. General information about FeatureCollection can be found in Section 2.3 within The GeoJSON Format Specification.
## GeoJSON encoding/decoding

All of the GeoJSON Objects implemented in this library can be encoded and decoded into raw GeoJSON with the geojson.dump, geojson.dumps, geojson.load, and geojson.loads functions.


```python
import geojson

my_point = geojson.Point((43.24, -1.532))

pprint(my_point)  # doctest: +ELLIPSIS
#{"coordinates": [43.2..., -1.53...], "type": "Point"}

dump = geojson.dumps(my_point, sort_keys=True)

pprint(dump)  # doctest: +ELLIPSIS
#'{"coordinates": [43.2..., -1.53...], "type": "Point"}'

gj = geojson.loads(dump)  # doctest: +ELLIPSIS
#{"coordinates": [43.2..., -1.53...], "type": "Point"}
pprint(gj)
```

    {"coordinates": [43.24, -1.532], "type": "Point"}
    '{"coordinates": [43.24, -1.532], "type": "Point"}'
    {"coordinates": [43.24, -1.532], "type": "Point"}


## Custom classes

This encoding/decoding functionality shown in the previous can be extended to custom classes using the interface described by the __geo_interface__ Specification.


```python
import geojson

class MyPoint():
     def __init__(self, x, y):
         self.x = x
         self.y = y

     @property
     def __geo_interface__(self):
         return {'type': 'Point', 'coordinates': (self.x, self.y)}

point_instance = MyPoint(52.235, -19.234)

geojson.dumps(point_instance, sort_keys=True)  # doctest: +ELLIPSIS
#'{"coordinates": [52.23..., -19.23...], "type": "Point"}'
```




    '{"coordinates": [52.235, -19.234], "type": "Point"}'



## Helpful utilities
### coords

geojson.utils.coords yields all coordinate tuples from a geometry or feature object.


```python
import geojson

my_line = LineString([(-152.62, 51.21), (5.21, 10.69)])

my_feature = geojson.Feature(geometry=my_line)

list(geojson.utils.coords(my_feature))  # doctest: +ELLIPSIS
#[(-152.62..., 51.21...), (5.21..., 10.69...)]
```




    [(-152.62, 51.21), (5.21, 10.69)]



### map_coords

geojson.utils.map_coords maps a function over all coordinate tuples and returns a geometry of the same type. Useful for translating a geometry in space or flipping coordinate order.


```python
import geojson

new_point = geojson.utils.map_coords(lambda x: x/2, geojson.Point((-115.81, 37.24)))

geojson.dumps(new_point, sort_keys=True)  # doctest: +ELLIPSIS
#'{"coordinates": [-57.905..., 18.62...], "type": "Point"}'
```




    '{"coordinates": [-57.905, 18.62], "type": "Point"}'



### validation

geojson.is_valid provides validation of GeoJSON objects.


```python
import geojson

validation = geojson.is_valid(geojson.Point((-3.68,40.41,25.14)))
print(validation['valid'])
#'no'

print(validation['message'])
#'the "coordinates" member must be a single position'
```

    no
    the "coordinates" member must be a single position


### generate_random

geojson.utils.generate_random yields a geometry type with random data


```python
import geojson

geojson.utils.generate_random("LineString")  # doctest: +ELLIPSIS
#{"coordinates": [...], "type": "LineString"}
```




    {"coordinates": [[-4.454240116119678, -85.11096594745686], [-102.67726268531537, -21.1641373701423], [-175.4525855417237, 53.518811905348855]], "type": "LineString"}



### Development

To build this project, run python setup.py build. To run the unit tests, run python setup.py test.


```python

```
