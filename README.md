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

**create_reduce_region_function(geometry, reducer=ee.Reducer.mean(),scale=1000,crs='EPSG:4326', bestEffort=True,maxPixels=1e13,tileScale=4)**

Creates a region reduction function.

  Creates a region reduction function intended to be used as the input function
  to ee.ImageCollection.map() for reducing pixels intersecting a provided region
  to a statistic for each image in a collection. See ee.Image.reduceRegion()
  documentation for more details.

Parameters:

  **geometry:**
    
      An ee.Geometry that defines the region over which to reduce data.
    
  **reducer:**
   
      Optional; An ee.Reducer that defines the reduction method.

  **scale:**
    
      Optional; A number that defines the nominal scale in meters of the
      projection to work in.

  **crs:**
    
      Optional; An ee.Projection or EPSG string ('EPSG:5070') that defines
      the projection to work in.

  **bestEffort:**
    
      Optional; A Boolean indicator for whether to use a larger scale if the
      geometry contains too many pixels at the given scale for the operation
      to succeed.

  **maxPixels:**
    
      Optional; A number specifying the maximum number of pixels to reduce.
    
  **tileScale:**
    
      Optional; A number representing the scaling factor used to reduce
      aggregation tile size; using a larger tileScale (e.g. 2 or 4) may enable
      computations that run out of memory with the default.

 **Returns:**
  
    A function that accepts an ee.Image and reduces it by region, according to
    the provided arguments. 

This function was taken from the time series tutorial for python of the Google Engine developers group  (for further information visit: https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair)






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
