#pensar un mejor nombre :o
import numpy as np
import ee
import 

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
lons = np.array((ee.Array(latlon_new.get("longitude")).getInfo()))  ##Prueben hacer lons.shape y y van a ver que es un horror.

##reshape para que quede tres matrices tipo meshgrid
uniqueLats = np.unique(lats)
uniqueLons = np.unique(lons)
ncols = len(uniqueLons)    
nrows = len(uniqueLats)

no2_2019=no2.reshape(nrows,ncols)
LATS=lats.reshape(nrows,ncols)
LONS=lons.reshape(nrows,ncols)

###repetimos para 2020###

##Podríamos hacer lo mismo, pero las matrices de lat y lon son  iguales. Una forma más corta
##que permite obtener el array de los valores (pero que no nos da la lat y lon) es la funcion
##ee.Image.sampleRectangle. Ya viene con las dimensiones correctas y no hay que reshapear

no2_2020=np.array(collection_img2.sampleRectangle(roi).get('tropospheric_NO2_column_number_density').getInfo())

##para tomar una unica escala de colores tomo el valor maximo de ambos arrays
vmax=np.max([np.max(no2_2020),np.max(no2_2019)])

###Esta es la rutina de graficado. No rompan nada###

##colores
cmap=mpl.cm.get_cmap('seismic',100)  


fig, axs = plt.subplots(nrows=1,ncols=2, subplot_kw={'projection': ccrs.PlateCarree()},figsize=(12,6))
fig.subplots_adjust(top=0.89,right=0.87,wspace=0.05, hspace=0.07)

plt.suptitle('Concentración media mensual de NO2 troposférico (mol/m2)',fontsize=15,y=0.93)

cs=axs[0].pcolormesh(LONS,LATS,no2_2019,vmin=0,vmax=vmax, cmap=cmap)
axs[0].add_feature(cartopy.feature.COASTLINE)
axs[0].add_feature(cartopy.feature.BORDERS)
axs[0].add_geometries(data.geometries(), crs=ccrs.Geodetic(), edgecolor='k', facecolor='none')
axs[0].set_extent([np.min(LONS), np.max(LONS), np.min(LATS), np.max(LATS)])
axs[0].set_title(inicio[:-3])

axs[1].pcolormesh(LONS,LATS,no2_2020,vmin=0,vmax=vmax, cmap=cmap)
axs[1].add_feature(cartopy.feature.COASTLINE)
axs[1].add_feature(cartopy.feature.BORDERS)
axs[1].add_geometries(data.geometries(), crs=ccrs.Geodetic(), edgecolor='k', facecolor='none')
axs[1].set_extent([np.min(LONS), np.max(LONS), np.min(LATS), np.max(LATS)])
axs[1].set_title(inicio2[:-3])

cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.7])
fmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cbar=fig.colorbar(cs, cax=cbar_ax,ticks=np.linspace(0,vmax,10),format=fmt)

