#pensar un mejor nombre :o
import numpy as np
import ee
import collection as col
import matplotlib.cm as mpl
import matplotlib.pyplot as plt

col.initialize()
print("inicializo")
ciudad = 'Buenos Aires'

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33 

delta=0    ## este parámetro es solo para agrandar o achicar la region de manera proporcional.

roi = ee.Geometry.Rectangle([np.round(lon_w-delta,2), np.round(lat_s-delta,2), np.round(lon_e+delta,2), np.round(lat_n+delta,2)],geodesic= False,proj='EPSG:4326')
print("hice geo")

##Este código es para tener una visualización espacial del no2. Vamos a tomar medias mensuales

inicio='2019-04-01'
final ='2019-05-01' #la fecha final que sea 1 mes despues, así calcula la media mensual


collection=ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2').select('tropospheric_NO2_column_number_density').filterDate(inicio,final)

###si quisiéramos otra cosa que no sea la media, hay que cambiar el parámetro .mean() !!
collection_img=collection.mean().setDefaultProjection(collection.first().projection())


##Este codigo es un poco un lío pero básicamente lo que hace, una vez obtenida la imagen de GEE
##en una determinada region de interes (roi),transforma en un array de numpy y tambien
##obtiene las matrices de lat y lon, el tema es que hay que reshapear porque viene todo en una tira de datos. 

latlon=ee.Image.pixelLonLat().addBands(collection_img)
latlon_new = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, maxPixels=1e13,scale=1113.2)

no2 = np.array((ee.Array(latlon_new.get('tropospheric_NO2_column_number_density')).getInfo()))
lats = np.array((ee.Array(latlon_new.get("latitude")).getInfo()))
lons = np.array((ee.Array(latlon_new.get("longitude")).getInfo()))  

##reshape para que quede tres matrices tipo meshgrid
uniqueLats = np.unique(lats)
uniqueLons = np.unique(lons)
ncols = len(uniqueLons)    
nrows = len(uniqueLats)

no2=no2.reshape(nrows,ncols)
LATS=lats.reshape(nrows,ncols)
LONS=lons.reshape(nrows,ncols)

###repetimos para 2020###

##Podríamos hacer lo mismo, pero las matrices de lat y lon son  iguales. Una forma más corta
##que permite obtener el array de los valores (pero que no nos da la lat y lon) es la funcion
##ee.Image.sampleRectangle. Ya viene con las dimensiones correctas y no hay que reshapear

#no2_2020=np.array(collection_img2.sampleRectangle(roi).get('tropospheric_NO2_column_number_density').getInfo())

##para tomar una unica escala de colores tomo el valor maximo de ambos arrays
vmax=np.max(no2)

###Rutina de graficado###

##colores
cmap=mpl.get_cmap('seismic',100)  


print("descargue")

fig, axs = plt.subplots(nrows=1,ncols=2, subplot_kw={'projection': ccrs.PlateCarree()},figsize=(12,6))
fig.subplots_adjust(top=0.89,right=0.87,wspace=0.05, hspace=0.07)

plt.suptitle('Concentración media mensual de NO2 troposférico (mol/m2)',fontsize=15,y=0.93)

cs=axs[0].pcolormesh(LONS,LATS,no2,vmin=0,vmax=vmax, cmap=cmap)
axs[0].add_feature(cartopy.feature.COASTLINE)
axs[0].add_feature(cartopy.feature.BORDERS)
axs[0].add_geometries(data.geometries(), crs=ccrs.Geodetic(), edgecolor='k', facecolor='none')
axs[0].set_extent([np.min(LONS), np.max(LONS), np.min(LATS), np.max(LATS)])
axs[0].set_title(inicio[:-3])

cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.7])
fmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cbar=fig.colorbar(cs, cax=cbar_ax,ticks=np.linspace(0,vmax,10),format=fmt)

