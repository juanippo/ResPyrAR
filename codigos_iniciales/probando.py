import collection as col
import timeseries as ts
import ee
import subprocess
import requests

col.initialize()

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



"""
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