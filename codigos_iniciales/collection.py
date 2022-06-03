import ee

def initialize():
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()

def collection_mean(ini,fin):
    collection=ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2').select('tropospheric_NO2_column_number_density').filterDate(ini,fin)
    collection_img_mean=collection.mean().setDefaultProjection(collection.first().projection())
    return collection_img_mean
