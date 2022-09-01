import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import geemap
#import os

import miapp_NO2.roi as roir
import miapp_NO2.date_selection as ds
import miapp_NO2.collection as collection
import ee

def tif_gen():
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()
     
    print('This programme generates mean monthly maps of NO2 concentration over a region of interest')

    lat_s,lat_n,lon_w,lon_e = roir.roi_rectangle()
    roi = ee.Geometry.Rectangle([lon_w,lat_s,lon_e,lat_n],geodesic= False,proj='EPSG:4326')
    date_generated=ds.selec_month_dataseries()

    for ii, date in enumerate(date_generated):
          inicio=date.strftime("%Y-%m-%d")
          ini=date.strftime("%Y_%m")
          fin=date + relativedelta(months=1)
          final=fin.strftime("%Y-%m-%d")

          #collection=ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2').select('tropospheric_NO2_column_number_density').filterDate(inicio,final)
          #collection_img_mean=collection.mean().setDefaultProjection(collection.first().projection())  
          collection_img_mean=collection.collection_mean(inicio,final)
          geemap.ee_export_image(collection_img_mean, filename=ini+'.tif', region=roi, scale=1113.2)
          
    return

def tif_gen2(lon_w,lat_s,lon_e,lat_n,date_ini,date_end):

    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()
    
    roi = ee.Geometry.Rectangle([lon_w,lat_s,lon_e,lat_n],geodesic= False,proj='EPSG:4326')
    date_generated=ds.selec_month_dataseries2(date_ini,date_end)

    for ii, date in enumerate(date_generated):
          inicio=date.strftime("%Y-%m-%d")
          ini=date.strftime("%Y_%m")
          fin=date + relativedelta(months=1)
          final=fin.strftime("%Y-%m-%d")

          collection_img_mean=collection.collection_mean(inicio,final)
          geemap.ee_export_image(collection_img_mean, filename=ini+'.tif', region=roi, scale=1113.2)
          
    return