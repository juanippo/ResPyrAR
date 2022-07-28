#pensar un mejor nombre :o
import numpy as np
import ee
import collection as col
import matplotlib
import matplotlib.cm as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs             
import cartopy.feature as cfeature           
import cartopy.io.shapereader as shapereader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.feature.nightshade import Nightshade
from copy import deepcopy

col.initialize()

def space_data_meshgrid(roi, start, end, collection = None, statistic = 'mean', export = False):

	if collection == None:
		collection= col.get_collection(start,end)
	else:
		collection = collection.filterDate(start,end)
	
	if statistic == 'mean':	
		collection_img=collection.mean().setDefaultProjection(collection.first().projection())
	elif statistic == 'median':
		collection_img=collection.median().setDefaultProjection(collection.first().projection())
	else:
		print("Error: statistic not valid")

	if export:
		task = ee.batch.Export.image.toDrive(collection_img.toFloat(), 
		                                      description=start,
		                                      folder='NO2',
		                                      fileNamePrefix= "NO2_"+start,
		                                      region = roi,
		                                      dimensions = (256,256), ##ESTA BIEN? 
		                                      fileFormat = 'GeoTIFF',
		                                      maxPixels = 1e10) ##ESTA BIEN?
		task.start()


	latlon=ee.Image.pixelLonLat().addBands(collection_img)
	latlon_new = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, maxPixels=1e13,scale=1113.2,bestEffort = True)

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

	return no2, LATS, LONS


def plot_map(no2, lats, lons, shapefile, title = 'Concentración media de NO2 troposférico (mol/m2)', filename = '../figures/entero.png', width = 8, height = 6, font_size = 15, save = True, show = False):

	data = shapereader.Reader(shapefile)

	vmax=np.max(no2)

	##colores
	cmap=mpl.get_cmap('seismic',100)  

	fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()},figsize=(width,height))

	ax.add_feature(cartopy.feature.COASTLINE)
	ax.add_feature(cartopy.feature.BORDERS)
	ax.add_geometries(data.geometries(), crs=ccrs.Geodetic(), edgecolor='k', facecolor='none')
	ax.set_extent([np.min(lons), np.max(lons), np.min(lats), np.max(lats)])
	cs=ax.pcolormesh(lons,lats,no2,vmin=0,vmax=vmax, cmap=cmap)
	
	raw_fig = deepcopy(fig) 
	raw_ax = deepcopy(ax)
	
	fig.subplots_adjust(top=0.89,right=0.87,wspace=0.05, hspace=0.07)

	fig.suptitle(title,fontsize=font_size)

	cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.7])
	fmt = matplotlib.ticker.ScalarFormatter(useMathText=True)
	fmt.set_powerlimits((0, 0))
	fig.colorbar(cs, cax=cbar_ax,ticks=np.linspace(0,vmax,10),format=fmt)
	
	plt.close(raw_fig)
	plt.close(plt.figure(3))

	if save:
		fig.savefig(filename,dpi=500)	
	if show:
		plt.show()
	return raw_fig, raw_ax

