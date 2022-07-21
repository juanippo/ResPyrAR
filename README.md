# paquete_NO2

En la carpeta codigos_iniciales están los script iniciales que fui armando.

La notebook es la clase que preparamos para el curso de postgrado. En ella esta explicado paso a paso el proceso de descarga de datos.
El script tiff_generator.py toma un cuadrado de latitud y longitud y un periodo en meses. Y devuelve un mapa .tiff con la media mensual en esa región. Tiene dos versiones de funciones, una en la que traté de modularizar un poco las funciones metidas. Mi objetivo sería dejar de usar la libreria geemap. Pero no sé bien aun cómo.

El script timeseries.py tiene las funciones de reducción y tres funciones que generan series promediadas en el día, mes y año. Esto puede ampliarse un montón.

El script collection.py quería modularizar un par de pasos que repito mucho en varios scripts pero no me funciona del todo bien.

El script roi.py es un poco más "interactivo" es simplemente para elegir una región de interes (Region Of Interest) pero me parece que esto es un paso posterior en el diseñor del paquete.

El script date_selection.py también es un poco interactivo, pero la idea es que pueda armar una selección de días o meses a la hora de pedirle a google engine que te devuelva una serie o un mapa.

## Instrucciones de uso
. [Estaría bueno hacer un archivo de requirements para instalar todas las librerías necesarias en un solo paso]
. Para autenticar seguir las instrucciones de este link: https://developers.google.com/earth-engine/guides/python_install#expandable-2

<!--  fijarse qué de esto va y articularlo
apt-get install libproj-dev proj-data proj-bin
apt-get install libgeos-dev
pip install cython
pip install cartopy
apt-get -qq install python-cartopy python3-cartopy
pip uninstall -y shapely    # cartopy and shapely aren't friends (early 2020)
pip install shapely --no-binary shapely
