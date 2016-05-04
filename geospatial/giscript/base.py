#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
from PyUGC import *
from PyUGC.Stream import UGC
from PyUGC.Base import OGDC

'''
转换字符串，赋值？有点奇怪，没有必要的操作。
'''
def Convert(strFile):
    strUnicode = OGDC.OgdcUnicodeString()
    strTemp   = OGDC.OgdcMBString(strFile)
    OGDC.MBString2Unicode(strTemp, strUnicode)
    return strUnicode

'''
! \brief   Geometry类型转换
! \param   nType[I] 字段类型
! \return  
! \remarks
'''
def GeometryType2Str(nType):
    strType = ""
    
    if nType == 1:
        strType = "Point"
    elif nType == 2:
        strType = "MultiPoint"
    elif nType == 3:
        strType = "Line"
    elif nType == 5:
        strType = "Region"
    elif nType == 7:
        strType = "Text"
    else:
        strType = "Null"

    return strType
 
'''
! \brief   字段类型转换
! \param   nType[I] 字段类型
! \return  
! \remarks
'''
def FieldType2Str(nType):
    strType = ""
    
    if nType == 1:
        strType = "Boolean"
    elif nType == 2:
        strType = "Byte"
    elif nType == 3:
        strType = "INT16"
    elif nType == 4:
        strType = "INT32"
    elif nType == 6:
        strType = "Float"
    elif nType == 7:
        strType = "Double"
    elif nType == 8:
        strType = "Date"
    elif nType == 9:
        strType = "Binary"
    elif nType == 10:
        strType = "Text"
    elif nType == 11:
        strType = "LongBinary"
    elif nType == 16:
        strType = "INT64"
    elif nType == 18:
        strType = "Char"
    elif nType == 22:
        strType = "Time"
    elif nType == 23:
        strType = "TimeStamp"
    elif nType == 127:
        strType = "NText"
    elif nType == 128:
        strType = "Geometry"
    else:
        strType = "UnKnown"
    return strType


