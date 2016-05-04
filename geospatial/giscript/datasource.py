#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
#from PyUGC import *
#from PyUGC.Stream import UGC
#from PyUGC.Base import OGDC

from PyUGC.Stream import UGC
from PyUGC.Base import OGDC
from PyUGC import Engine,FileParser,DataExchange

from base import *
#from base import *

#================================================================
'''
! \brief   创建数据源，目前支持oracle和UDB
! \param   nEngineType[I] 数据源类型（UGC.UDB/UGC.OraclePlus）
! \return  如果成功则返回数据源指针,否则返回空指针
! \remarks 
'''
def CreateDatasource(nEngineType,datapath_out):
    if nEngineType == UGC.UDB:
        ds  = UGC.UGDataSourceManager.CreateDataSource(nEngineType)
        con = ds.GetConnectionInfo()
        con.m_strServer = Convert(datapath_out)
        
        bOpen = ds.Open()
        if bOpen[0] == 1:
            print("需要创建的数据源已经存在！！")
        else:
            bCreate = ds.Create()
            if bCreate[0] == 1:
                print("创建数据源成功！！")
            else:
                print("创建数据源失败，请查看文件型数据源是否已经打开！！")      
        return ds
    elif nEngineType == UGC.OraclePlus:
        ds  = UGC.UGDataSourceManager.CreateDataSource(nEngineType)
        con = ds.GetConnectionInfo()
        con.m_strServer   = Convert("weizq")
        con.m_strUser     = Convert("test")
        con.m_strPassword = Convert("test")

        bOpen = ds.Open()
        if bOpen[0] == 1:
            print("需要创建的数据源已经存在！！")
        else:
            bCreate = ds.Create()
            if bCreate[0] == 1:
                print("创建数据源成功！！")
            else:
                print("创建数据源失败！！")

        return ds
    else:
        printf("目前不支持此类型数据源创建，创建数据源失败！！")
        return None

#================================================================
'''
! \brief   创建Vector数据集
! \param   ds           [I] 数据源（如：UGC.UDB/UGC.OraclePlus）
! \param   strDtName    [I] 数据集名称
! \param   nType        [I] 数据集类型
! \param   nCodeType    [I] 编码方式
! \return  返回数据集指针或者None
! \remarks
'''
def CreateDatasetVector(ds, strDtName, nType, nCodeType):
    vectorInfo = UGC.UGDatasetVectorInfo()
    vectorInfo.m_strName    = Convert(strDtName)
    vectorInfo.m_nType      = nType
    vectorInfo.m_nCodecType = nCodeType

    dt = ds.CreateDatasetVector(vectorInfo)
    if dt != None:
        print("创建数据集成功！！")
    else:
        print("创建数据集失败,请检查数据集名称是否合法！！")

    return dt

#================================================================
def CreateDatasetPoint(ds, strDtName):
    #strDtName = Convert(strDtName)
    nType     = UGC.UGDataset.Point
    nCodeType = UGC.UGDataCodec.enrNONE
    dt = CreateDatasetVector(ds, strDtName, nType, nCodeType)
    if dt != None:
        print("Create dataset success:"+strDtName)
    else:
        print("Create dataset failed:"+strDtName)
    return dt

#================================================================
'''
! \brief   创建栅格数据集
! \param   ds           [I] 数据源（如：UGC.UDB/UGC.OraclePlus）
! \param   strDtName    [I] 数据集名称
! \param   nType        [I] 数据集类型
! \param   nWidth       [I] 数据集宽度
! \param   nHeight      [I] 数据集高度
! \param   nBlkSize     [I] 块大小
! \param   ePixelFormat [I] 像素格式
! \param   nCodeType    [I] 编码方式
! \param   bounds       [I] 数据集bound范围
! \return  返回数据集指针或者None
! \remarks
'''
def CreateDatasetRaster(ds, strDtName, nType, nWidth, nHeight, nBlkSize, \
                        ePixelFormat, nCodeType, bounds, bMb=False):
    strTableName = Convert("")
    raterInfo = UGC.UGDatasetRasterInfo(\
                            Convert(strDtName), strTableName, nType, \
                            nWidth, nHeight, nBlkSize, \
                            ePixelFormat, nCodeType, bounds)
    dt = ds.CreateDatasetRaster(raterInfo, bMb)
    if dt != None:
        print("创建数据集成功！！")
    else:
        print("创建数据集失败,请检查数据集名称是否合法！！")

    return dt
   
#================================================================
'''
! \brief   复制数据集
! \param   ds         [I] 数据源
! \param   srcDt      [I] 源数据集
! \param   strDesName [I] 目标数据集名称
! \param   nCodeType  [I] 编码方式
! \return  成功返回True，否则返回False
! \remarks
'''
def CopyDataset(ds, srcDt, strDesName, nCodeType):
    if srcDt == None:
        print("源数据集为空，复制数据集失败！")
        return None

    desDt = ds.CopyDataset(srcDt, strDesName, nCodeType)

    if desDt == None:
        print("复制数据集失败，请检查数据源中是否已经存在相同名称的数据集！")
        return None

    print("复制数据集成功！")

    return desDt

#================================================================
#Todo: need process params.
def AddField(srcDt,fieldname):
    bOpen = srcDt.Open()
    if bOpen[0] == 1:
        # 创建字段
        filedInfo = OGDC.OgdcFieldInfo()
        filedInfos = OGDC.OgdcFieldInfos()
        
        filedInfo.m_strName = Convert("MyTest1")
        filedInfo.m_nType = OGDC.OgdcFieldInfo.Double
        filedInfo.m_nSize = 8
        filedInfos.Add(filedInfo)
        
        filedInfo.m_strName = Convert("MyTest2")
        filedInfo.m_nType = OGDC.OgdcFieldInfo.NText
        filedInfo.m_nSize = 255
        filedInfos.Add(filedInfo)
        
        filedInfo.m_strName = Convert("MyTest3")
        filedInfo.m_nType = OGDC.OgdcFieldInfo.INT32
        filedInfo.m_nSize = 4
        filedInfos.Add(filedInfo)
        b = srcDt.CreateFields(filedInfos)
        if b[0] == 1:
            print("创建字段成功！！")
        else:
            print("创建字段失败！！")

#================================================================
'''
! \brief   删除数据集
! \param   ds        [I] 数据源
! \param   strDtName [I] 数据集名称
! \return  成功返回True，否则返回False
! \remarks
'''
def DeleteDataset(ds, strDtName):
    return ds.DeleteDataset(strDtName)
    
#================================================================
'''
! \brief   创建空间索引
! \param   dt   [I] 数据集
! \param   nType[I] 空间索引类型
! \return  创建成功返回true，否则返回false
! \remarks 
'''
def BuildSpatialIndex(dt, nType):
    vectorInfo = dt.GetInfo()
    nIndexType = vectorInfo.GetIndexType()
    if (nIndexType != 1 and nType == nIndexType):
        print("已经存在同种类型的空间索引，不需要创建！！")
        return True;

    IndexInfo = UGC.UGSpatialIndexInfo(nType)
    bBuild = dt.BuildSpatialIndex(IndexInfo)

    if bBuild[0] == 1:
        print("创建空间索引成功！！")

        return True
    else:
        print("创建空间索引失败！！")

        return False

#================================================================
'''
! \brief   删除空间索引空间索引
! \param   dt   [I] 数据集
! \return  删除成功返回true，否则返回false
! \remarks 
'''
def DeleteSpatialIndex(dt):
    b = dt.DropSpatialIndex()

    return b[0]

#================================================================
'''
! \brief   重新创建空间索引空间索引空间索引
! \param   dt   [I] 数据集
! \return  删除成功返回true，否则返回false
! \remarks 
'''
def ReBuildSpatialIndex(dt):
    b = dt.ReBuildSpatialIndex()
    return b[0]
    
#================================================================
'''
! \brief   导入数据，支持矢量和栅格
! \param   nFileType  [I] 文件类型（如：UGC.UGFileType.Shape）
! \param   importMode [I] 导入类型（如：UGC.UGImportParams.ModeGIS）
! \param   strFileName[I] 文件路径
! \param   ds         [I] 数据源
! \return  成功则返回true,否则返回false
! \remarks
'''
def Import(nFileType, importMode, strFileName, ds):
    importParams = UGC.UGExchangeParamsManager.MakeImportParams(nFileType)
    importParams.SetImportMode(importMode)
    importParams.SetFilePathName(strFileName)
    
    dataExchange = UGC.UGDataExchange()
    dataExchange.AttachDataSource(ds)
    bSuccess = dataExchange.Import(importParams)
    return bSuccess

#================================================================
def onResult(bSuccess,info):
    if bSuccess == 1:
        print("数据导入成功:"+info)
    else:
        print("数据导入失败:"+info)
    
#================================================================
#Import Image data（tiff）
def ImportRaster(file_in,ds):
    print("Import Raster: ",file_in)
    strFileName = Convert(file_in)
    bSuccess = Import(UGC.UGFileType.GTiff, UGC.UGImportParams.ModeIMG, strFileName, ds)
    onResult(bSuccess,"Import Image "+file_in)
    return bSuccess

#================================================================
#Import Vector data.
def ImportVector(file_in,ds):
    print("Import Vector: ",file_in)
    strFileName = Convert(file_in)
    bSuccess = Import(UGC.UGFileType.Shape, UGC.UGImportParams.ModeGIS, strFileName, ds)
    onResult(bSuccess,"Import Vector "+file_in)
    return bSuccess

#================================================================
'''
! \brief   导出数据，支持矢量和栅格
! \param   nFileType  [I] 文件类型（如：UGC.UGFileType.Shape）
! \param   strDtName  [I] 数据集名称
! \param   strFileName[I] 文件导出路径
! \param   ds         [I] 数据源
! \return  成功则返回true,否则返回false
! \remarks
'''
def Export(nFileType, strFileName, nIndex, ds):
    dt = ds.GetDataset(nIndex)
    if dt == None:
        print("数据集为空")
        return False

    if IsTypeMatch(nFileType, dt.GetType()) == 0:
        print("数据集类型和导出格式不匹配！！")
        return False

    strDtName = dt.GetName()
    strEx = UGC.UGFileType.FileTypeToExtName(nFileType)
    strFilePathName = strFileName+strDtName+strEx
    if IsFileExist(strFilePathName):
        print("已经存在同名文件，请重新设置导出路径！！")
        return False

    # 通过UGC.UGExchangeParamsManager.MakeExportParams创建的方法，需要
    # 用户自己释放内存，尽管python有垃圾回收机制，谁new的谁释放最好不过
    exportParams = UGC.UGExchangeParamsManager.MakeExportParams(nFileType)
    b = UGC.UGExchangeParamsManager.IsValidExportParams(nFileType, exportParams)
    if b[0] != 1:
        return False

    exportParams.SetDtNameToBeExported(strDtName)
    exportParams.SetFilePathName(strFilePathName)

    # tiff按块导出设置参数，对于大影像按导出有很大的优势，
    # 可以加快导出速度，目前默认是不压缩的，后续支持压缩方式设置
    if nFileType == UGC.UGFileType.GTiff:
        exportParams.SetExportAsTile(b"1")
    
    dataExchange = UGC.UGDataExchange()
    dataExchange.AttachDataSource(ds)
    bIsSuccss = dataExchange.Export(exportParams)

    del exportParams
    exportParams = None
    return bIsSuccss

#================================================================    
'''
! \brief 检查类型是否匹配
'''
def IsTypeMatch(nFileType, dtType):
    #矢量
    if UGC.UGFileType.IsVector(nFileType)[0] == 1:
        if (dtType == UGC.UGDataset.Point) or \
        (dtType == UGC.UGDataset.Line)     or \
        (dtType == UGC.UGDataset.Region)   or \
        (dtType == UGC.UGDataset.Text)     or \
        (dtType == UGC.UGDataset.CAD):
            return True
        return False
    #模型
    elif UGC.UGFileType.IsModelFile(nFileType)[0] == 1:
        if (dtType == UGC.UGDataset.CAD) or (dtType == UGC.UGDataset.Model):
            return True
        return False
    #影像/栅格
    else:

        if (dtType == UGC.UGDataset.MBImage) or \
        (dtType == UGC.UGDataset.MBGrid)     or \
        (dtType == UGC.UGDataset.MBDEM)      or \
        (dtType == UGC.UGDataset.Image)      or \
        (dtType == UGC.UGDataset.Grid)       or \
        (dtType == UGC.UGDataset.DEM):
            return True
        return False
    
#================================================================
#Import Grid data.
def ImportGrid(file_in,ds):
    print("Import Grid: ",file_in)
    strFileName = Convert(file_in)
    bSuccess = Import(UGC.UGFileType.AIASCIIGrid, UGC.UGImportParams.ModeGrid, strFileName, ds)
    onResult(bSuccess,"Import Grid "+file_in)
    return bSuccess

def test():
    print("Test Datasource")
        
if __name__ == '__main__':
    print("Datasource functions:")
    print("createdatasource.")
