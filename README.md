# respyrAR

<!-- En la carpeta codigos_iniciales están los script iniciales que fui armando.

La notebook es la clase que preparamos para el curso de postgrado. En ella esta explicado paso a paso el proceso de descarga de datos.
El script tiff_generator.py toma un cuadrado de latitud y longitud y un periodo en meses. Y devuelve un mapa .tiff con la media mensual en esa región. Tiene dos versiones de funciones, una en la que traté de modularizar un poco las funciones metidas. Mi objetivo sería dejar de usar la libreria geemap. Pero no sé bien aun cómo.

El script timeseries.py tiene las funciones de reducción y tres funciones que generan series promediadas en el día, mes y año. Esto puede ampliarse un montón.

El script collection.py quería modularizar un par de pasos que repito mucho en varios scripts pero no me funciona del todo bien.

El script roi.py es un poco más "interactivo" es simplemente para elegir una región de interes (Region Of Interest) pero me parece que esto es un paso posterior en el diseñor del paquete.

El script date_selection.py también es un poco interactivo, pero la idea es que pueda armar una selección de días o meses a la hora de pedirle a google engine que te devuelva una serie o un mapa.

-->

# Español

## Instalación

1. Para poder autenticar seguir las instrucciones de este [link](https://developers.google.com/earth-engine/guides/python_install#expandable-2 "Authentication")

2. Para poder instalar dependencias del paquete *respyrar* (en particular la bilbioteca ```cartopy```), primero es necesario instalar algunas dependencias. Se puede encontrar información detallada para Linux, Windows y iOS [aquí](https://scitools.org.uk/cartopy/docs/latest/installing.html "Cartopy") y particularmente para Windows [aquí](https://stackoverflow.com/questions/70177062/cartopy-not-able-to-identify-geos-for-proj-install-on-windows "Cartopy on Windows"). Para sistemas de linux basados en Debian (como Ubuntu) alcanza con correr los siguientes comandos en la terminal:

```
$ apt-get install libproj-dev proj-data proj-bin
$ apt-get install libgeos-dev
$ apt-get -qq install python-cartopy python3-cartopy
```
3. Una vez resueltos estos dos pasos, sólo queda instalar el paquete ejecutando en la terminal el siguiente comando

```
$ pip install respyrar
```

# English

1. To enable authentication follow [these](https://developers.google.com/earth-engine/guides/python_install#expandable-2 "Authentication") instructions.

2. Before installing *respyrar* you'll need to enable some dependencies installation (particularly, ```cartopy```). You can find detailed instructions for  Linux, Windows and iOS [here](https://scitools.org.uk/cartopy/docs/latest/installing.html "Cartopy") and particularly  for Windows [here](https://stackoverflow.com/questions/70177062/cartopy-not-able-to-identify-geos-for-proj-install-on-windows "Cartopy on Windows"). For Debian-based linux systems (like Ubuntu) run the following commands in your terminal:

```
$ apt-get install libproj-dev proj-data proj-bin
$ apt-get install libgeos-dev
$ apt-get -qq install python-cartopy python3-cartopy
```

3. Once these two steps are completed, all you need to do is run the following command

```
$ pip install respyrar
```


## Functions

### get_collection(ini,fin, sat = 'COPERNICUS/S5P/OFFL/L3_NO2', column ='tropospheric_NO2_column_number_density')

Returns the image collection (as an Earth Engine object) of a column from the indicated satellite for a determined period of time. 

**Parameters:**

    ini:

The start date (inclusive), of Date/Number/String type.

    fin:

The finalization date (exclusive), of Date/Number/String type.

    sat:

Optional; A string indicating the desired satellite and variable. By default it is set to the L3_NO2 variable, of the S5P satellite of the Copernicus Programme, on offline mode.

    column:

Optional; A string indicating the desired column. By default it is set to tropospheric NO2 column number density.


### create_reduce_region_function(geometry, reducer=ee.Reducer.mean(),scale=1000,crs='EPSG:4326', bestEffort=True,maxPixels=1e13,tileScale=4)

Creates a region reduction function.

  Creates a region reduction function intended to be used as the input function
  to `ee.ImageCollection.map()` for reducing pixels intersecting a provided region
  to a statistic for each image in a collection. See ee.Image.reduceRegion()
  documentation for more details.

**Parameters:**

    geometry:
    
  An ee.Geometry that defines the region over which to reduce data.

    reducer:
   
  Optional; An ee.Reducer that defines the reduction method. By default set to ee.Reducer.mean(), which calculates the mean of the specified region.

    scale:
    
  Optional; A number that defines the nominal scale in meters of the projection to work in. By default set to 1000.

    crs:
    
  Optional; An ee.Projection or EPSG string ('EPSG:5070') that defines the projection to work in. By default set to 'EPSG:4326'.

    bestEffort:
    
  Optional; A Boolean indicator for whether to use a larger scale if the geometry contains too many pixels at the given scale for the operation to succeed. By default set to True.

    maxPixels:
    
  Optional; A number specifying the maximum number of pixels to reduce. By default set to 1e13.
    
    tileScale:
    
  Optional; A number representing the scaling factor used to reduce aggregation tile size; using a larger tileScale (e.g. 2 or 4) may enable computations that run out of memory with the default. By default set to 4.

**Returns:**
  
A function that accepts an ee.Image and reduces it by region, according to the provided arguments. 

This function was taken from the time series tutorial for python of the Google Engine developers group  (for further information visit: https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair)


### fc_to_dict(ee.FeatureCollection)

Transfers feature properties to a dictionary. The result of create_reduce_region_function applied to an `ee.ImageCollection` produces an `ee.FeatureCollection`. This data needs to be transferred to the Python kernel, but serialized feature collections are large and hard to deal with. This step defines a function to convert the feature collection to an `ee.Dictionary` where the keys are feature property names and values are corresponding lists of property values, which `pandas` can deal with handily.

1. Extract the property values from the `ee.FeatureCollection` as a list of lists stored in an `ee.Dictionary` using `reduceColumns()`.
2. Extract the list of lists from the dictionary.
3. Add names to each list by converting to an `ee.Dictionary` where keys are property names and values are the corresponding value lists.

The returned `ee.Dictionary` is essentially a table, where keys define columns and list elements define rows.

**Parameters :**

    fc: 
An ee.FeatureCollection object which is a result of applying create_reduce_region_function to an ‘ee.ImageCollection’.

**Returns:**

The correspondent `ee.Dictionary`.

This function was taken from the time series tutorial for python of the Google Engine developers group  (for further information visit: https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair)


### add_date_info(df)

Add date columns derived from the milliseconds from Unix epoch column. The pandas library provides functions and objects for timestamps and the DataFrame object allows for easy mutation.
Define a function to add date variables to the DataFrame: year, month, day, weekday, and day of year (DOY)

**Parameters:**

    df:
Pandas dataframe.

**Returns:**

The modified Pandas dataframe.

This function was taken from the time series tutorial for python of the Google Engine developers group  (for further information visit: https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair)

### geometry_rectangle(lon_w,lat_s,lon_e,lat_n)
Returns an ee.Geometry that defines the region over which to reduce data in create_reduce_region_function . The region is a latitude-longitude rectangle. 

**Parameters:**

    lon_w:
West boundary of the rectangle. Must be a float between -180° and 180°.

    lat_s:
South boundary of the rectangle. Must be a float between -90° and 90°.

    lon_e:
East boundary of the rectangle. Must be a float between -180° and 180°.

    lat_n:
North boundary of the rectangle. Must be a float between -90° and 90°.

**Returns:**

The `ee.Geometry.Rectangle` correspondent to those coordinates.

For further information visit https://developers.google.com/earth-engine/apidocs/ee-geometry-rectangle

### time_series_df(roi, start, end, filename = 'NO2trop_series.csv', reducers = [ee.Reducer.mean()], red_names = ['NO2_trop_mean'], collection = None)

Creates a pandas dataframe that includes the time series of the concentration of a gas measured from the Sentinel 5p TROPOMI sensor available in the Google Earth Engine api. By default, it calculates the average tropospheric NO2 series over a region of interest. 

**Parameters:**

    roi:
An ee.Geometry object. It can be a rectangle of latitude and longitude, a polygon, or other Geometries. You can create a rectangle with the function `geometry_rectangle`.

    start: 
A string indicating the start of the time series. The format should be 'YYYY-MM-DD'. In the case of NO2, the series begins on 2018-06-28.

    end:
A string indicating the end of the time series. The format should be 'YYYY-MM-DD'. 

    filename:
Optional; A string indicating the name of the output file. By default set to 'NO2trop_series.csv'.

    reducers:
Optional; An array of ee.Reducer objects. For each object, a column is created in the dataframe where that spatial statistic is applied. By default, the average value over a region is taken. For more reducers, visit https://developers.google.com/earth-engine/guides/reducers_intro

    red_names:
Optional; An array of strings indicating the name of the reducers used. It must have the same length as the list of reducers and respect the same order as the one used in it. By default it is an array containing only 'NO2_trop_mean'.

    collection:
Optional; An `ee.ImageCollection` object for the desired satellite, variable and column, and for a period containing the desired one. It can be created with `get_collection`. If the same collection is used several times, it is more efficient to get it just once and pass it as a parameter. By default it is set to None, so that it is obtained automatically.  

**Returns:**

A Pandas dataframe with a column for each reducer in `reducers`, respectively named with the names in `red_names`. Also contains the columns Timestamp, Year, Month, Day and Weekday.


<!--CONSIDERO QUE “variable” y “var_name” tienen que ser argumentos de la funcion. Para una misma colección, podríamos tomar NO2 troposferico, o TOTAL. -->

### ts_dailydf(df, filename='dailymean_df.csv', statistic = 'mean')

Returns a daily time series. In case of missing data in the series, it interleaves NaN values. In case of two daily data (this is possible due to overlapping of the satellite pass in some regions) returns the average 

**Parameters:**
    df:
Panda dataframe with the original time series. This is the one calculated in `time_series_df`.

    filename:
Optional; A string indicating the name of the output file. By default set to 'dailymean_df.csv'.

    statistic:
Optional; A string indicating the statistic reduction to be performed on each day of the time series. It can be set to 'mean' or 'median'. By default it is set to 'mean'. 

**Returns:**

A Pandas dataframe collapsed by day. 

<!-- ACA TENGO DUDAS EN STATISTIC: la serie original ocmo mucho tira dos datos diarios. Hacer la media y la mediana sería lo mismo, no sé si agregar “mediana” como estadistico posible. Tiene sentido para series mensuales y semanales pero nno sé si diarias. -->

### ts_monthlydf(df, filename='monthlymean_df.csv', statistic = 'mean')

Returns a monthly series of the concentration of the chosen gas. 

**Parameters:**
    df:
Panda dataframe with the original time series. This time series is the one that is calculated in time_series_df

    filename:
Optional; A string indicating the name of the output file. By default set to 

    statistic:
Optional; A string indicating the statistic reduction to be performed on each month of the time series. It can be set to 'mean' or 'median'. By default it is set to 'mean'. 

**Returns:**

A Pandas dataframe collapsed by month. 

### ts_weeklydf(df, filename='weeklymean_df.csv', statistic = 'mean')

Returns a weekly series of the concentration of the chosen gas. 

**Parameters:**
    df:
Panda dataframe with the original time series. This time series is the one that is calculated in time_series_df

    filename:
Optional; A string indicating the name of the output file.

    statistic:
Optional; A string indicating the statistic reduction to be performed on each week of the time series. It can be set to 'mean' or 'median'. By default it is set to 'mean'. 

**Returns:**

A Pandas dataframe collapsed by week. 

### space_data_meshgrid(roi, start, end, collection = None, statistic = 'mean', export = False)

Obtains a meshgrid with the no2 values in the indicated region for the specified period.

**Parameters:**

    roi:

An ee.Geometry object. It can be a rectangle of latitude and longitude, a polygon, or other Geometries. You can create a rectangle with the function `geometry_rectangle`. (ROI stands for Region Of Interest)

    start:

String indicating start date (inclusive).

    end:

String indicating end date (exclusive).

    collection:

Optional; An `ee.ImageCollection` object for the desired satellite, variable and column, and for a period containing the desired one. It can be created with `get_collection`. If the same collection is used several times, it is more efficient to get it just once and pass it as a parameter. By default it is set to None, so that it is obtained automatically.  
    
    statistic:
    
Optional; A string indicating the statistic reduction to be performed on each pixel of the spatial data for the specified period. It can be set to 'mean' or 'median'. By default it is set to 'mean'. 

    export:

Optional; Boolean value. If set to True, exports to the Google Drive of the user the calcullated meshgrid as a GeoTIFF file. It is saved in the folder "NO2", with the filename "NO2_"+_start_ (where _start_ is the homonym parameter). By default it is set to False.

**Returns:**

    values:

NumPy ndarray of with as many rows as different latitude values, and as many columns as different longitude values. Each cell contains the value of NO2 correspondent to the latitude and longitude (these expressed in the following objects) 

    lats:

NumPy ndarray of with as many rows as different latitude values, and as many columns as different longitude values. Each cell contains the correspondent latitude value.

    lons: 

NumPy ndarray of with as many rows as different latitude values, and as many columns as different longitude values. Each cell contains the correspondent longitude value.

### interanual_variation(df_m, year1, year2, month_num, column = 'NO2_trop_mean')

Calculate the interanual variation of NO2 (or the specified column) for the indicated month of two different years.

**Parameters:**

    df_m:
Pandas Dataframe, collpased by month, containing data for the specified month of the specified years.
    
    year1:
    
Numeric value, the first year to be considered.

    year2:
    
Numeric value, the second year to be considered.
    
    month_num:

Numeric value, the number of the month to be considered (e.g. The number for January is 1, the one for April is 4, etc.).    
    
    column:

Optional; A string with the name of the column of the dataframe to evaluate the variation over. By default it is set to 'NO2_trop_mean'.

**Returns:**

A float number indicating the porcentual variation of the column, in terms of the first year, i.e. (NO2 of year2 - NO2 of year1) / (NO2 of year1) .

### plot_map(no2, lats, lons, shapefile, title = 'Concentración media de NO2 troposférico (mol/m2)', filename = 'map.png', width = 8, height = 6, font_size = 15, save = True, show = False)

Plots a map for the specified latitudes and longitudes, colored as indicated by `no2`. Designed to be used with the result of `space_data_meshgrid`. Can be saved, shown, and/or returned.

**Parameters:**

    no2:

NumPy ndarray of with as many rows as different latitude values, and as many columns as different longitude values. Each cell contains the value of NO2 correspondent to the latitude and longitude (these expressed in the following objects) 

    lats:

NumPy ndarray of with as many rows as different latitude values, and as many columns as different longitude values. Each cell contains the correspondent latitude value.

    lons: 

NumPy ndarray of with as many rows as different latitude values, and as many columns as different longitude values. Each cell contains the correspondent longitude value.

    shapefile:

String with the path to a .shp file containing borders of the region to be drawn.

    title:

Optional; A string with the title the figure will show. By default it is 'Concentración media de NO2 troposférico (mol/m2)' (spanish for Tropospheric NO2 mean concentration (mol/m2)) .

    filename:

Optional; String with the name of the output file (in the case `save` is set to True). By default set to 'map.png'.

    width:

Optional; Int, the width of the figure to be generated. By default set to 8.

    height:

Optional; Int, the height of the figure to be generated. By default set to 6.

    font_size:

Optional; Int, the font size of the figure to be generated. By default set to 15.

    save:

Optional; Boolean value, if set to True saves the figure in the location indicated by 'filename'. By default set to True.

    show:

Optional; Boolean value, if set to True shows the figure with `matplotlib` interactive interface. By default set to False.

**Returns:**

    raw_fig, raw_ax:

`matplotlib` figure and axes respectively, before adding any formatting (title, color scale, etc.)

<!-- aca podria agregar una imagen final y raw, para mostrar de ejemplo -->


### plot_series(df, start = pd.Timestamp.min, end = pd.Timestamp.max, column = 'NO2_trop_mean', filename = 'series.png', width = 15, height = 4, save = True, show = False)

Plot the time series passed as a Pandas dataframe.

**Parameters:**

    df:

Pandas dataframe, with a 'Fecha_datetime' column containing timestamps in YYYY-MM-DD date format.

    start:

Optional; String in YYYY-MM-DD date format indicating start time. Values previous to this date won't be plotted. By default set to Pandas minimum timestamp (no filter).

    end:

Optional; String in YYYY-MM-DD date format indicating end time. Values posterior to this date won't be plotted. By default set to Pandas maximum timestamp (no filter).

    column:

Optional; String indicating the dataframe column name from which to plot values. By default set to 'NO2_trop_mean'.

    filename:

Optional; String with the name of the output file (in the case `save` is set to True). By default set to 'series.png'.

    width:

Optional; Int, the width of the figure to be generated. By default set to 15.

    height:

Optional; Int, the height of the figure to be generated. By default set to 4.

    save:

Optional; Boolean value, if set to True saves the figure in the location indicated by 'filename'. By default set to True.

    show:

Optional; Boolean value, if set to True shows the figure with `matplotlib` interactive interface. By default set to False.

**Returns:**

    fig, ax:

`matplotlib` figure and axes, respectively.


### plot_autocorr(df, lags, column = 'NO2_trop_mean', filename = 'autocorrelogram.png', width = 30, height=5, save = True, show = False)

Plot autocorrelogram of the indicated dataframe. Plots lags on the horizontal and the correlations on vertical axis.  

    df:

Pandas dataframe, with a 'Fecha_datetime' column containing timestamps in YYYY-MM-DD date format.

    lags:

An int or array of lag values, used on horizontal axis. Uses np.arange(lags) when lags is an int.

    column:

Optional; String indicating the dataframe column name from which to plot values. By default set to 'NO2_trop_mean'.

    filename:

Optional; String with the name of the output file (in the case `save` is set to True). By default set to 'autocorrelogram.png'.

    width:

Optional; Int, the width of the figure to be generated. By default set to 30.

    height:

Optional; Int, the height of the figure to be generated. By default set to 5.

    save:

Optional; Boolean value, if set to True saves the figure in the location indicated by 'filename'. By default set to True.

    show:

Optional; Boolean value, if set to True shows the figure with `matplotlib` interactive interface. By default set to False.

**Returns:**

    fig, ax:

`matplotlib` figure and axes, respectively.

### barplot_year_cmp(df_m, year1, year2, column = 'NO2_trop_mean', filename='compared_series.png', width = 10, height=4, save = True, show = False)

Draw a bar graph comparing the monthly values between two years.

**Parameters:**

    df_m:
    
Pandas dataframe aggregated by month, and containing at least some values for the indicated years.    
    
    year1:
    
One of the years to be compared, as Int/String.
    
    year2:

The other of the years to be compared, as Int/String.  

    column:

Optional; String indicating the dataframe column name from which to plot values. By default set to 'NO2_trop_mean'.

    filename:

Optional; String with the name of the output file (in the case `save` is set to True). By default set to 'compared_series.png'.

    width:

Optional; Int, the width of the figure to be generated. By default set to 10.

    height:

Optional; Int, the height of the figure to be generated. By default set to 4.

    save:

Optional; Boolean value, if set to True saves the figure in the location indicated by 'filename'. By default set to True.

    show:

Optional; Boolean value, if set to True shows the figure with `matplotlib` interactive interface. By default set to False.

**Returns:**

    fig, ax:

`matplotlib` figure and axes, respectively.



<!--

## TO DO
. armar un script de example / test razonable
. minima documentación acá
. poner todo en español
. corregir typo interanual es interannual

--

. para dibujar el mapa estoy usando un shp que dibuja contornos. hacer que sea opcional 
. polygon funciona bien pero space_date_meshgrid se rompe si no es rectangular
. bounds de polygon redondean un poco mal (o está desfasado respecto al otro shape)
. hacer algo que descargue los datos del mapa aun si hay algunos pixeles que tienen solo nans (geemap lo hizo)
. cuando uso una coleccion que me pasan, agregar un chequeo que vea que el período que quiero esté adentro (cómo?)
. agregar un chequeo de fecha bien pasada
. está buena la solucion a lo de los reductores? pasan un arreglo de reductores y uno de nombres, tienen que medir lo mismo...
. mascara
. arreglar el warning de pandas index en lo de isocalendar
. desarrollar la documentacion
. reducir cantidad de bibliotecas a usar
. crear poligonos a partir del nombre de la ciudad-prov-pais?


<!--  NECESARIO CORRER ANTES DE INSTALAR (QUÈ PASA SI TIENEN WINDOWS?)

apt-get install libproj-dev proj-data proj-bin
apt-get install libgeos-dev
apt-get -qq install python-cartopy python3-cartopy

#sugerir esto?:
pip uninstall -y shapely    # cartopy and shapely aren't friends (early 2020)
pip install shapely --no-binary shapely
