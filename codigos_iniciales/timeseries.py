import ee
import pandas as pd
import isoweek

try:
        ee.Initialize()
except Exception as e:
        ee.Authenticate()
        ee.Initialize()
        
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
  #df['DOY'] = pd.DatetimeIndex(df['Timestamp']).dayofyear
  df['Weekday']=pd.DatetimeIndex(df['Timestamp']).weekday
  return df
  
  
def time_series_df(lon_w,lat_s,lon_e,lat_n,date_ini,date_end):
    collection_name = 'COPERNICUS/S5P/OFFL/L3_NO2'
    variable  = 'tropospheric_NO2_column_number_density'
    var_name  = 'NO2_trop_mean'
    file_name = 'NO2trop_series.csv'
    roi = ee.Geometry.Rectangle([lon_w,lat_s,lon_e,lat_n],geodesic= False,proj='EPSG:4326')
    
    reduce_mean = create_reduce_region_function(geometry=roi, reducer=ee.Reducer.mean(), scale=1113.2, crs='EPSG:4326')
 
    collection_filter=ee.ImageCollection(collection_name).select(variable).filterDate(date_ini,date_end)
    collection_fc = ee.FeatureCollection(collection_filter.map(reduce_mean)).filter(ee.Filter.notNull(collection_filter.first().bandNames()))
    collection_dict=fc_to_dict(collection_fc).getInfo()

    df=pd.DataFrame(collection_dict)
    df =  add_date_info(df)
    df  = df.rename(columns={variable: var_name}).drop(columns=['millis', 'system:index'])
    df.to_csv(file_name,index=False)
    return df
    
def ts_dailydf(df):
    df_daily=df.groupby(['Year','Month','Day']).mean().reset_index()
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
    df_daily.to_csv('dailymean_df.csv',index=False)
    return df_daily

def ts_montlydf(df):
    df_daily=ts_dailydf(df)
    df_monthly=df_daily.groupby(['Year','Month']).mean().reset_index()
    df_monthly_c=df_daily.groupby(['Year','Month']).count().reset_index()
    df_monthly['Fecha_datetime']=pd.to_datetime(df_monthly['Year'].astype(str)+'-'+df_monthly['Month'].astype(str),format='%Y-%m')
    df_monthly.drop(columns=['Day','Weekday','N_obs'],inplace=True)
    df_monthly['N_days']=df_monthly_c[df.columns[0]]
    df_monthly.to_csv('monthlymean_df.csv',index=False)
    return df_monthly

def ts_weeklydf(df):
    df_daily=ts_dailydf(df)
    day=df_daily.Fecha_datetime.dt.date.values
    df_daily['WeekOfYear']=[isoweek.Week.withdate(d) for d in day]
    df_weekly=df_daily.groupby(['WeekOfYear']).mean().reset_index()
    df_weekly_c=df_daily.groupby(['WeekOfYear']).count().reset_index()
    df_weekly['N_days']=df_weekly_c[df.columns[0]].astype(int)
    df_weekly['Fecha_datetime']=[isoweek.Week.monday(s) for s in df_weekly.WeekOfYear.values]
    df_weekly.drop(columns=['Year','Month','Day','Weekday','N_obs'],inplace=True) 
    df_weekly.to_csv('weeklymean_df.csv',index=False)
    return df_weekly
    
#def ts_graph(df, timeinterval=daily):
#    if timeinterval == 
    