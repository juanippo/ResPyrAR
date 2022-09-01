import collection as col
import timeseries as ts
import ee
import subprocess
import requests

col.initialize()


coords = [ [-6218000.0,-3830999.999999998],
[-6219000.0,-3830999.999999998],
[-6221000.0,-3830999.999999998],
[-6222007.812499998,-3829007.8125],
[-6224000.0,-3828000.000000002],
[-6224000.0,-3825000.000000001],
[-6224999.999999998,-3825000.000000001],
[-6225876.798629761,-3823630.3968429575],
[-6229000.0,-3825000.000000001],
[-6229999.999999996,-3825000.000000001],
[-6218000.0,-3830999.999999998] ]

geom = ee.Geometry.Polygon(coords)

print("Geo: ",geom)

boun = geom.bounds()

print("Bounds: ", boun)

"""
inicio='2020-04-01'
final ='2020-05-01' 

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

roi = ts.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)

cole = col.get_collection(inicio,final)
collection_img=cole.mean().setDefaultProjection(cole.first().projection())
latlon=ee.Image.pixelLonLat().addBands(collection_img)
latlon_new = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, maxPixels=1e13,scale=1113.2)


# opcion 1: exportar a drive

task = ee.batch.Export.image.toDrive(collection_img.toFloat(), 
                                      description=inicio,
                                      folder='NO2',
                                      fileNamePrefix= "NO2_"+inicio,
                                      region = roi,
                                      dimensions = (256,256), 
                                      fileFormat = 'GeoTIFF',
                                      maxPixels = 1e10)
task.start()



# opcion 2: obtengo link de descarga y ...
path = collection_img.getDownloadUrl({
'region': roi 
})

print(path)

# opcion 2.1 : lo descargo llamando a sistema (FEA porque solo anda en linux y tiene que tener bien instalado eso, etc)

bash_command = "curl " + path + " --output ../figures/comprimido"
process = subprocess.run(bash_command.split())
bash_command = "unzip ../figures/comprimido"
process = subprocess.run(bash_command.split())
bash_command = "rm ../figures/comprimido"
process = subprocess.run(bash_command.split())

# opcion 2.2: lo descargo desde esta biblioteca para descargar (piola pero me funciona)

x = requests.get(path,allow_redirects=True)
print(x) #en vez de esto, descargarlo




"""


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