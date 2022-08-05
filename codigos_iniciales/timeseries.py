import ee
import pandas as pd
import geopandas as gpd
import isoweek
import json
from dateutil.relativedelta import relativedelta
import collection as col
import datetime

# parametrizar el estadistico del reductor (espacial) que ahora es mean - linea 62
# listo (o la idea sería que le pases un string y te genere el reductor?)

# parametrizar el estadistico que tomo de la serie de tiempo, que ahora es mean - linea 75 p.ej
# listo - acá hice lo del string. está mejor? habría que agregar más estadísticos.

# pasarle a time_series_df una geometria en vez de coordenadas. y otra funcion hace la geometria
# listo - podemos hacer más geometrias, tipo un circulo, etc.
#       - de la forma en que está hecho, se puede crear la geo que quiera con ee y usar esa

#en timeseres_df pasar un array de reducers y que esten como columnas del df

#armar otro como geometry rectangel que tome uhn archivo y haga esto
# shape = gpd.read_file("delta-shp/Mapas/Delta/Delta.shp")
# js = json.loads(shape.to_json())
# roi = ee.Geometry(ee.FeatureCollection(js).geometry())

#agregasr un warning cuando usa mean, que tenga en cuenta que sirve si los datos siguen una dist normal


col.initialize()

def create_reduce_region_function(geometry,
                                  reducer=ee.Reducer.mean(),
                                  scale=1000,
                                  crs='EPSG:4326',
                                  bestEffort=True,
                                  maxPixels=1e13,
                                  tileScale=4):

    def reduce_region_function(img):

        stat = img.reduceRegion(
            reducer=reducer,
            geometry=geometry,
            scale=scale,
            crs=crs,
            bestEffort=bestEffort,
            maxPixels=maxPixels,
            tileScale=tileScale)

        return ee.Feature(geometry, stat).set({'millis': img.date().millis()})
    return reduce_region_function

def fc_to_dict(fc):
    prop_names = fc.first().propertyNames()
    prop_lists = fc.reduceColumns(
        reducer=ee.Reducer.toList().repeat(prop_names.size()),
      selectors=prop_names).get('list')

    return ee.Dictionary.fromLists(prop_names, prop_lists)

# Function to add date variables to DataFrame.
def add_date_info(df):
    df['Timestamp'] = pd.to_datetime(df['millis'], unit='ms')
    df['Year'] = pd.DatetimeIndex(df['Timestamp']).year
    df['Month'] = pd.DatetimeIndex(df['Timestamp']).month
    df['Day'] = pd.DatetimeIndex(df['Timestamp']).day
    df['Weekday']=pd.DatetimeIndex(df['Timestamp']).weekday
    return df

def geometry_rectangle(lon_w,lat_s,lon_e,lat_n):
    return ee.Geometry.Rectangle([lon_w,lat_s,lon_e,lat_n],geodesic= False,proj='EPSG:4326')

def geometry_polygon(shapefile):
    shape = gpd.read_file(shapefile)
    shape = shape.convex_hull
    js = json.loads(shape.to_json())
    roi = ee.Geometry(ee.FeatureCollection(js).geometry())
    return roi

def time_series_df(roi, start, end, file_name = 'NO2trop_series.csv', reducers = [ee.Reducer.mean()], red_names = ['NO2_trop_mean'], collection = None):
    
    assert(len(reducers) == len(red_names))
    #satelite COPERNICUS, modo offline, elijo el no2 // para tiempor real elegir NRTI en vez de OFFL
    collection_name = 'COPERNICUS/S5P/OFFL/L3_NO2'
    #dentro de eso elijo la densidad de columna troposferica:
    variable  = 'tropospheric_NO2_column_number_density'
    var_name  = 'NO2_trop_mean'

    df = pd.DataFrame({"millis": []})

    if collection == None:
        collection_filter = col.get_collection(start,end)
    else:
        collection_filter = collection.filterDate(start,end)

    i=0
    for reducer in reducers:
        reduce_function = create_reduce_region_function(geometry=roi, reducer=reducer, scale=1113.2, crs='EPSG:4326')
        collection_fc = ee.FeatureCollection(collection_filter.map(reduce_function)).filter(ee.Filter.notNull(collection_filter.first().bandNames()))
        collection_dict=fc_to_dict(collection_fc).getInfo()

        new_df = pd.DataFrame(collection_dict)
        new_df = new_df.rename(columns={variable: red_names[i]}).drop(columns=['system:index'])
        df = pd.merge(df, new_df, on='millis', how='outer')
        i += 1 
    df = add_date_info(df)
    df = df.drop(columns=['millis'])
    df.to_csv(file_name,index=False)
    return df

def ts_dailydf(df, file_name='dailymean_df.csv', statistic = 'mean'):
    assert(statistic == 'mean' or statistic == 'median')
    if statistic == 'mean' :
        df_daily=df.groupby(['Year','Month','Day']).mean().reset_index()
    elif statistic == 'median':
        df_daily=df.groupby(['Year','Month','Day']).median().reset_index()
    df_daily_c=df.groupby(['Year','Month','Day']).count().reset_index()
    df_daily['N_obs']=df_daily_c[df.columns[0]]
    df_daily['Fecha_datetime']=pd.to_datetime(df_daily['Year'].astype(str)+'-'+df_daily['Month'].astype(str)+'-'+df_daily['Day'].astype(str),format='%Y-%m-%d')
    t=df_daily.Fecha_datetime.values
    dias_completos=pd.date_range(start=t[0], end=t[-1]).to_frame(name='Fecha_datetime')
    df_daily=dias_completos.merge(df_daily, how='left',on='Fecha_datetime')
    df_daily['Year']=df_daily['Fecha_datetime'].dt.year
    df_daily['Month']=df_daily['Fecha_datetime'].dt.month
    df_daily['Day']=df_daily['Fecha_datetime'].dt.day
    df_daily['Weekday']=df_daily['Fecha_datetime'].dt.weekday
    df_daily['N_obs']=df_daily['N_obs'].fillna(0).astype(int)
    df_daily.to_csv(file_name,index=False)
    return df_daily

def ts_monthlydf(df, file_name='monthlymean_df.csv', statistic = 'mean'):
    assert(statistic == 'mean' or statistic == 'median')
    df_daily=ts_dailydf(df, statistic = statistic)
    if statistic == 'mean' :
        df_monthly=df_daily.groupby(['Year','Month']).mean().reset_index()
    elif statistic == 'median':
        df_monthly=df_daily.groupby(['Year','Month']).median().reset_index()
    df_monthly_c=df_daily.groupby(['Year','Month']).count().reset_index()
    df_monthly['Fecha_datetime']=pd.to_datetime(df_monthly['Year'].astype(str)+'-'+df_monthly['Month'].astype(str),format='%Y-%m')
    df_monthly.drop(columns=['Day','Weekday','N_obs'],inplace=True)
    df_monthly['N_days']=df_monthly_c[df.columns[0]]
    df_monthly.to_csv(file_name,index=False)
    return df_monthly

def ts_weeklydf(df, file_name='weeklymean_df.csv', statistic = 'mean'):
    assert(statistic == 'mean' or statistic == 'median')
    df_daily=ts_dailydf(df, statistic = statistic)
    #retrocedo tantos días según el día de la semana que sea
    df_daily['Fecha_datetime']= df_daily['Fecha_datetime'] - df_daily['Weekday'].apply(lambda x : datetime.timedelta(days=x))
    #df_daily['WeekOfYear']=[isoweek.Week.withdate(d) for d in day]
    #df_daily['WeekOfYear']=pd.DatetimeIndex(df_daily['Fecha_datetime']).week
    df_daily['WeekOfYear']=pd.Int64Index(pd.DatetimeIndex(df_daily['Fecha_datetime']).isocalendar().week)
    if statistic == 'mean' :
        df_weekly=df_daily.groupby(['WeekOfYear','Fecha_datetime']).mean().reset_index()
    if statistic == 'median':
        df_weekly=df_daily.groupby(['WeekOfYear','Fecha_datetime']).median().reset_index()
    df_weekly_c=df_daily.groupby(['WeekOfYear']).count().reset_index()
    df_weekly['N_days']=df_weekly_c[df.columns[0]].astype(int)
    #df_weekly['Fecha_datetime']=[isoweek.Week.monday(s) for s in df_weekly.WeekOfYear.values]
    #df_weekly['Fecha_datetime']=df_weekly['WeekOfYear'].apply(lambda x : x+1)
    df_weekly.drop(columns=['Year','Month','Day','Weekday','N_obs'],inplace=True)
    df_weekly.to_csv(file_name,index=False)
    return df_weekly



#def ts_graph(df, timeinterval=daily):
#    if timeinterval ==
