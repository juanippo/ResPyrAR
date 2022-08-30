import utils
import timeseries as ts
import matplotlib.pyplot as plt
import pandas as pd 
import mask
import ee

jan19 = '2019-01-01'
march19 = '2019-03-01'
may19 = '2019-05-01'

jan21 = '2021-01-01'

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

reds = [ee.Reducer.mean(), ee.Reducer.min()] #spatial reducers we'll be using
names = ['NO2_trop_mean','NO2_trop_min']


arg_shapefile = "../data/gadm36_ARG_2.shp" 

def test_time_series(start, end, roi):
    
    df = ts.time_series_df(roi,start,end,filename='raw.csv',reducers = reds, red_names = names)
    df_daily = ts.ts_dailydf(df, filename= 'daily.csv')
    df_weekly = ts.ts_weeklydf(df, filename= 'weekly.csv')
    df_monthly = ts.ts_monthlydf(df, filename= 'monthly.csv')

    return df, df_daily, df_weekly, df_monthly

def test_tseries_median(df):
    median_daily = ts.ts_dailydf(df, statistic = 'median')
    median_weekly = ts.ts_weeklydf(df, statistic = 'median')
    median_monthly = ts.ts_monthlydf(df, statistic = 'median')

    return median_daily, median_weekly, median_monthly

print("Create geometry of Buenos Aires")
roi = ts.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)

print("Obtain dataframes with NO2 time series. Aggregate using mean")
df, df_d, df_w, df_m = test_time_series(march19, may19, roi)

print("Show and save plots for these series")
fig, ax = ts.plot_series(df_d,show = True) #save with default name: series.png
ts.plot_series(df_w, filename = 'weekly.png', show = True)
ts.plot_series(df_m, filename = 'monthy.png', show = True)

print("Show plot saved as matplotlib object")
plt.show() #NO ESTA FUNCIONANDO :(

print("Recalculate NO2 time series, now using median to aggregate")
median_d, median_w, median_m = test_tseries_median(df)

print("Show or save plots for these series")
fig, ax = ts.plot_series(median_d,show = True) #show and save with default name: series.png
ts.plot_series(median_w, filename = 'median_weekly.png') #save, don't show
ts.plot_series(median_m, show = True, save = False) #show, don't save

print("Show autocorrelogram for daily series")
ts.plot_autocorr(df_d, lags = 22, show = True, save = False)

print("Get series for 2019 and 2020")
long_df = ts.time_series_df(roi,jan19,jan21,filename='long_raw.csv',reducers = reds, red_names = names)
long_monthly = ts.ts_monthlydf(long_df, filename= 'long_monthly.csv')

print("Load monthly series from csv and plot a bar plot comparing years")
df_monthly = pd.read_csv('long_monthly.csv')
ts.barplot_year_cmp(df_monthly, 2019, 2020, show = True) #SE GUARDÓ MAL

var = ts.interanual_variation(df_monthly, 2019, 2020, month_num = 4)
print("Interannual variation for april 2019-2020: ",var)

##########################################################################################
'''
initial_date = '2019-03-01'
final_date = '2019-05-01'


#initial_date='2019-01-01'
#final_date   ='2021-01-01'


utils.initialize()
utils.get_collection(initial_date, final_date) #esta funcion igual creo que la vamos a sacar

print("Initialize y get_collection corrieron")

shapefile = "../data/gadm36_ARG_2.shp" 

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

roi = ts.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)
print("geometría creada")

reds = [ee.Reducer.mean(), ee.Reducer.min()]
names = ['NO2_trop_mean','NO2_trop_min']

df = ts.time_series_df(roi,initial_date,final_date,filename='../actual_outcomes/raw.csv',reducers = reds, red_names = names)
df_daily = ts.ts_dailydf(df, filename= '../actual_outcomes/daily.csv')
df_monthly = ts.ts_monthlydf(df, filename= '../actual_outcomes/monthly.csv')
df_w = ts.ts_weeklydf(df, filename= '../actual_outcomes/weekly.csv')

print("time_series_df, daily, monthly y weekly corrieron")

#tener los expected_outcomes de antes
assert(compare_csv('../actual_outcomes/raw.csv','../expected_outcomes/NO2trop_series.csv'))
assert(compare_csv('../actual_outcomes/daily.csv','../expected_outcomes/dailymean_df.csv'))
assert(compare_csv('../actual_outcomes/monthly.csv','../expected_outcomes/monthlymean_df.csv'))
assert(compare_csv('../actual_outcomes/weekly.csv','../expected_outcomes/weeklymean_df.csv'))

print("time_series_df, daily, monthly y weekly dieron bien")


ts.ts_dailydf(df, statistic = 'median')
ts.ts_monthlydf(df, statistic = 'median')
ts.ts_weeklydf(df, statistic = 'median')

print("daily, monthly y weekly con median corrieron")

ts.plot_series(df_daily)
ts.plot_series(df_w, filename = "weekly_series.png", show = True)


inicio = initial_date #'2018-08-15'
fin = final_date # '2018-09-06'

ts.plot_series(df_daily, start = inicio, end = fin, show = True)

ts.plot_autocorr(df_daily, lags = 22, show = True)

df_monthly = pd.read_csv('../actual_outcomes/monthly.csv')
#ts.barplot_year_cmp(df_monthly, 2019, 2020, show = True)

#var = ts.interanual_variation(df_monthly, 2019, 2020, month_num = 3)
#print("La variación interanual para abril 2020-2019 es: ",var)


##Este código es para tener una visualización espacial del no2. Vamos a tomar medias mensuales

inicio='2020-04-01'
final ='2020-04-03' 

values, lon, lat = ts.space_data_meshgrid(roi, inicio, final, export = False)
raw, _ = ts.plot_map(values, lon, lat, shapefile, show=True)
raw.savefig("../figures/crudo.png")


# Podes descargar los datos a una coleccion y despues pasarlos a los distintos comandos, en vez de crear la coleccion cada vez.
# Ejemplo:


cole = utils.get_collection(initial_date, final_date)

#df = ts.time_series_df(roi,initial_date,final_date,filename='../actual_outcomes/raw.csv', collection = cole)
#df_daily = ts.ts_dailydf(df, filename= '../actual_outcomes/daily.csv')


inicio = '2018-08-15'
fin = '2018-09-06'

ts.plot_series(df_daily, start = inicio, end = fin, show = True)


inicio='2019-04-01'
final ='2019-05-01' 

values, lon, lat = ts.space_data_meshgrid(roi, inicio, final, collection = cole, export = True)
raw_fig, raw_ax = ts.plot_map(values, lon, lat, shapefile, show=True)


inicio='2019-03-01'
final ='2019-03-09' 
#shape_sjuan = "../../chagas/poligono_sJuan/poligono_sJuan.shp"
shape_sjuan = '../data/sjuan/sanjuan.shp'
shape_cordoba = "../data/cordoba.shp"

lat_n=-31.43207816743497
lat_s=-31.641590578584516
lon_w=-68.67117914175913
lon_e=-68.40888055777475


square_sjuan = ts.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)

print("inicio")

roi_sjuan = ts.geometry_polygon(shape_sjuan)
roi_sjuan_bounds = roi_sjuan.bounds()
#print(roi_sjuan)
#area = roi_sjuan.area().divide(1000 * 1000).getInfo()
#print('sjuan area: ', area)
#perimetro = roi_sjuan.perimeter().getInfo()
#print('perim: ', perimetro)
#area_bounds = roi_sjuan_bounds.area(maxError = 10).divide(1000 * 1000).getInfo()
#print('bounds area: ', area_bounds)
print("creo poligono")
#print(roi_sjuan_bounds)
"""
df = ts.time_series_df(roi_sjuan_bounds,initial_date,final_date,filename='../actual_outcomes/raw_sjuan.csv')
print("creo df")

df_daily = ts.ts_dailydf(df, filename= '../actual_outcomes/daily.csv')
print("creo daily")

ts.plot_series(df_daily)
print("ploteo")

df = ts.time_series_df(square_sjuan,initial_date,final_date,filename='../actual_outcomes/raw_sjuan.csv')
print("creo df")

df_daily = ts.ts_dailydf(df, filename= '../actual_outcomes/daily.csv')
print("creo daily")

ts.plot_series(df_daily, filename='../figures/square_series.png')
print("ploteo")
"""

values, lon, lat = ts.space_data_meshgrid(roi_sjuan, inicio, final, collection = cole, export = True)
ts.plot_map(values, lon, lat, shape_sjuan, show=True)


mask=mask.mask_percentil(values,0.7)  #array de 0 y 1 
mask_list=mask.mask_curve(lons,lats,values,0.7)  ## curva calculada con la matriz original
maskones_list=mask.mask_onescurve(lons,lats,values,0.7) ##curva calculada con la matriz de ceros y unos ,esto es otra metodología nomás
suma=mask.pixel_in_contour(lons,lats,max_curve(CS.allsegs[0]))
print('puntos dentro del contorno: ',suma)


'''