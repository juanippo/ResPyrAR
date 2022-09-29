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

. Para poder autenticar seguir las instrucciones de este link: https://developers.google.com/earth-engine/guides/python_install#expandable-2

. Para poder instalar el paquete *respyrar*, primero es necesario instalar GEOS:

###         Debian/Ubuntu:

Correr los siguientes comandos en la terminal

```
$ apt-get install libproj-dev proj-data proj-bin
$ apt-get install libgeos-dev
$ apt-get -qq install python-cartopy python3-cartopy
```


<!-- . Para correr el test, desde la misma ubicacion que este README correr python3 -m test.test -->

# English

. To enable authentication follow these instructions: https://developers.google.com/earth-engine/guides/python_install#expandable-2

. Before being able to install the *respyrar* package, you need to install GEOS:

###         Debian/Ubuntu:

Run the following commands in your terminal

```
$ apt-get install libproj-dev proj-data proj-bin
$ apt-get install libgeos-dev
$ apt-get -qq install python-cartopy python3-cartopy
```

## Functions

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
   
  Optional; An ee.Reducer that defines the reduction method.

    scale:
    
  Optional; A number that defines the nominal scale in meters of the projection to work in.

    crs:
    
  Optional; An ee.Projection or EPSG string ('EPSG:5070') that defines the projection to work in.

    bestEffort:
    
  Optional; A Boolean indicator for whether to use a larger scale if the geometry contains too many pixels at the given scale for the operation to succeed.

    maxPixels:
    
  Optional; A number specifying the maximum number of pixels to reduce.
    
    tileScale:
    
  Optional; A number representing the scaling factor used to reduce aggregation tile size; using a larger tileScale (e.g. 2 or 4) may enable computations that run out of memory with the default.

**Returns:**
  
A function that accepts an ee.Image and reduces it by region, according to the provided arguments. 

This function was taken from the time series tutorial for python of the Google Engine developers group  (for further information visit: https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair)


### fc_to_dict(ee.FeatureCollection):

Transfers feature properties to a dictionary. The result of create_reduce_region_function applied to an `ee.ImageCollection` produces an `ee.FeatureCollection`. This data needs to be transferred to the Python kernel, but serialized feature collections are large and hard to deal with. This step defines a function to convert the feature collection to an `ee.Dictionary` where the keys are feature property names and values are corresponding lists of property values, which `pandas` can deal with handily.

1. Extract the property values from the `ee.FeatureCollection` as a list of lists stored in an `ee.Dictionary` using `reduceColumns()`.
2. Extract the list of lists from the dictionary.
3. Add names to each list by converting to an `ee.Dictionary` where keys are property names and values are the corresponding value lists.

The returned `ee.Dictionary` is essentially a table, where keys define columns and list elements define rows.

**Parameters :**

    fc: 
An ee.FeatureCollection object which is a result of applying create_reduce_region_function to an ‘ee.ImageCollection’.

This function was taken from the time series tutorial for python of the Google Engine developers group  (for further information visit: https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair)


### add_date_info(df):

Add date columns derived from the milliseconds from Unix epoch column. The pandas library provides functions and objects for timestamps and the DataFrame object allows for easy mutation.
Define a function to add date variables to the DataFrame: year, month, day, weekday, and day of year (DOY)

**Parameters:**

    df:
Pandas dataframe.

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

For further information visit https://developers.google.com/earth-engine/apidocs/ee-geometry-rectangle

### time_series_df(roi, start, end, filename = 'NO2trop_series.csv', reducers = [ee.Reducer.mean()], red_names = ['NO2_trop_mean'], collection = None):

Creates a pandas dataframe that includes the time series of the concentration of a gas measured from the Sentinel 5p TROPOMI sensor available in the Google Earth Engine api. By default, it calculates the average tropospheric NO2 series over a region of interest. 

**Parameters: **

    roi:
An ee.Geometry object. It can be a rectangle of latitude and longitude, or a polygon. It is the object returned by the function geometry_rectangle or geometry_polygon.

    start: 
A string indicating the start of the time series. The format should be 'YYYY-MM-DD'. In the case of NO2, the series begins on 2018-06-28.

    end:
A string indicating the end of the time series. The format should be 'YYYY-MM-DD'. 

    filename:
A string indicating the name of the output file.

    reducers:
A list of ee.Reducer objects. For each object, a column is created in the dataframe where that spatial statistic is applied. By default, the average value over a region is taken. For more reducers, visit https://developers.google.com/earth-engine/guides/reducers_intro

    red_names:
A list of strings indicating the name of the reducers used. It must have the same length as the list of reducers and respect the same order as the one used in it. 

    collection:
The name of the google engine collection from which the data is taken. This package is prepared to work with the Sentinel-5P TROPOMI data. To see the other collections available visit: https://developers.google.com/earth-engine/datasets/catalog/sentinel-5p . By default, it takes the NO2 collection.


<!--CONSIDERO QUE “variable” y “var_name” tienen que ser argumentos de la funcion. Para una misma colección, podríamos tomar NO2 troposferico, o TOTAL. -->

### ts_dailydf(df, filename='dailymean_df.csv', statistic = 'mean'):

Returns a daily time series. In case of missing data in the series, it interleaves NaN values. In case of two daily data (this is possible due to overlapping of the satellite pass in some regions) returns the average 

**Parameters:**
    df:
Panda dataframe with the original time series. This time series is the one that is calculated in time_series_df

    filename:
A string indicating the name of the output file.

    statistic:
In case of two daily data, returns the average.


<!-- ACA TENGO DUDAS EN STATISTIC: la serie original ocmo mucho tira dos datos diarios. Hacer la media y la mediana sería lo mismo, no sé si agregar “mediana” como estadistico posible. Tiene sentido para series mensuales y semanales pero nno sé si diarias. -->

### ts_monthlydf(df, filename='monthlymean_df.csv', statistic = 'mean'):

Returns a monthly series of the concentration of the chosen gas. 

**Parameters:**
    df:
Panda dataframe with the original time series. This time series is the one that is calculated in time_series_df

    filename:
A string indicating the name of the output file.

    statistic:
Indicates the type of statistics to be performed on the daily data. The default case calculates the monthly average. It could be the median.

### ts_weeklydf(df, filename='weeklymean_df.csv', statistic = 'mean')

Returns a weekly series of the concentration of the chosen gas. 

**Parameters:**
    df:
Panda dataframe with the original time series. This time series is the one that is calculated in time_series_df

    filename:
A string indicating the name of the output file.

    statistic:
Indicates the type of statistics to be performed on the daily data. The default case calculates the weekly average. It could be the median.







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
