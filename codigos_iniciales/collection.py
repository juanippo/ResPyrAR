import ee

def initialize():
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()

def get_collection(ini,fin, sat = 'COPERNICUS/S5P/OFFL/L3_NO2', column ='tropospheric_NO2_column_number_density'):
    collection=ee.ImageCollection(sat).select(column).filterDate(ini,fin)
    return collection
