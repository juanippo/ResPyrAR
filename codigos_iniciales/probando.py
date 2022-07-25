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

"""
task = ee.batch.Export.image.toDrive(collection_img.toFloat(), 
                                      description=inicio,
                                      folder='gugl erz enshín',
                                      fileNamePrefix= inicio,
                                      region = roi,
                                      dimensions = (256,256), 
                                      fileFormat = 'GeoTIFF',
                                      maxPixels = 1e10)
task.start()




path = collection_img.getDownloadUrl({
'region': roi 
})

bash_command = "curl " + path + " --output ../figures/comprimido"
process = subprocess.run(bash_command.split())
bash_command = "unzip ../figures/comprimido"
process = subprocess.run(bash_command.split())
bash_command = "rm ../figures/comprimido"
process = subprocess.run(bash_command.split())
"""

x = requests.get("https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/thumbnails/18e40b9aa750453da5f08502bffeefce-999d601cee1061c1af5913f5b8237248:getPixels")
print(x)
