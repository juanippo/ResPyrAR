import collection as col
import timeseries as ts
import figures as figu
import csv
import matplotlib.pyplot as plt
import spacedata as sd 
import mask

def compare_csv(filename1, filename2):
    t1 = open(filename1, 'r')
    t2 = open(filename2, 'r')
    fileone = t1.readlines()
    filetwo = t2.readlines()
    t1.close()
    t2.close()

    return (fileone == filetwo)


#initial_date = '2018-07-01'
#final_date = '2018-10-01'

initial_date='2018-07-01'
final_date   ='2021-01-01'

shapefile = "../data/gadm36_ARG_2.shp" 

#col.initialize()
#col.get_collection(initial_date, final_date) #esta funcion igual creo que la vamos a sacar

#print("Initialize y get_collection corrieron")

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

roi = ts.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)
'''
print("geometría creada")

df = ts.time_series_df(roi,initial_date,final_date,file_name='../actual_outcomes/raw.csv')
df_daily = ts.ts_dailydf(df, file_name= '../actual_outcomes/daily.csv')
df_monthly = ts.ts_monthlydf(df, file_name= '../actual_outcomes/monthly.csv')
#df_w = ts.ts_weeklydf(df, file_name= '../actual_outcomes/weekly.csv')

print("time_series_df, daily, monthly y weekly corrieron")
"""
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
"""
figu.plot_series(df_daily)
#figu.plot_series(df_w, filename = "weekly_series.png", show = True)


inicio = '2018-08-15'
fin = '2018-09-06'

figu.plot_series(df_daily, start = inicio, end = fin, show = True)

figu.plot_autocorr(df_daily, lags = 22, show = True)

figu.barplot_year_cmp(df_monthly, 2019, 2020, show = True)

var = figu.interanual_variation(df_monthly, 2019, 2020, month_num = 3)
print("La variación interanual para abril 2020-2019 es: ",var)


##Este código es para tener una visualización espacial del no2. Vamos a tomar medias mensuales

inicio='2020-04-01'
final ='2020-05-01' 

values, lon, lat = sd.space_data_meshgrid(roi, inicio, final)
raw, _ = sd.plot_map(values, lon, lat, shapefile, show=True)
raw.savefig("../figures/crudo.png")


# Podes descargar los datos a una coleccion y despues pasarlos a los distintos comandos, en vez de crear la coleccion cada vez.
# Ejemplo:

'''

cole = col.get_collection(initial_date, final_date)

#df = ts.time_series_df(roi,initial_date,final_date,file_name='../actual_outcomes/raw.csv', collection = cole)
#df_daily = ts.ts_dailydf(df, file_name= '../actual_outcomes/daily.csv')

inicio = '2018-08-15'
fin = '2018-09-06'

#figu.plot_series(df_daily, start = inicio, end = fin, show = True)


inicio='2019-04-01'
final ='2019-05-01' 

#values, lon, lat = sd.space_data_meshgrid(roi, inicio, final, collection = cole, export = True)
#raw_fig, raw_ax = sd.plot_map(values, lon, lat, shapefile, show=True)


shape_sjuan = "../../chagas/poligono_sJuan/poligono_sJuan.shp"
roi_sjuan = ts.geometry_polygon(shape_sjuan)

values, lon, lat = sd.space_data_meshgrid(roi_sjuan, inicio, final, collection = cole, export = True)
sd.plot_map(values, lon, lat, shapefile, show=True)


mask=mask.mask_percentil(values,0.7)  #array de 0 y 1 
mask_list=mask.mask_curve(lons,lats,values,0.7)  ## curva calculada con la matriz original
maskones_list=mask.mask_onescurve(lons,lats,values,0.7) ##curva calculada con la matriz de ceros y unos ,esto es otra metodología nomás
suma=mask.pixel_in_contour(lons,lats,max_curve(CS.allsegs[0]))
print('puntos dentro del contorno: ',suma)

