import collection as col
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import math
import matplotlib.path

col.initialize()

def max_curve(curves):
    return max(curves, key=len)

def mask_curve(lon,lat,no2_values,q):  ###dadp un no2_values, una retícula y un percentil devuelve una lista de puntos de latitud longitud
    CS=plt.contour(lon,lat,no2_values,levels=[np.quantile(no2_values,q)]) #por qué se llama CS??
    points=max_curve(CS.allsegs[0])
    ##creo un csv para guardar las coordenadas de la mascara ##
    points_dic={'Lon':points[:,0],'Lat':points[:,1]}
    points_df=pd.DataFrame(data=points_dic)
    points_df.to_csv('coordMask.csv',index=False)
    list_points=points.tolist()
    plt.close()
    if list_points[0]!=list_points[-1]:
        list_points=list_points + [list_points[0]]
    return list_points

def mask_percentil(no2_values,q): ###dado un no2_values devuelve una matriz de 1 y 0 con 1 los puntos donde se supere el percentil q
    perNO2=np.quantile(no2_values,q)
    mask=ma.masked_less_equal(no2_values,perNO2)
    ones_arr= np.ones(no2_values.shape)
    ones_arr= ma.no2_values(ones_arr, mask=mask.mask)
    ones_arr= ma.Maskedno2_values(ones_arr,fill_value=0).filled().astype(int)
    #pix=len(no2_values[no2_values>perNO2])
    return ones_arr

def mask_onescurve(lon,lat,no2_values,q):  ##igual que mask_curve pero sobre la matrices de 1 y 0. No cambia mucho hay que estimar el error  
    ones_arr=mask_percentil(no2_values,q)
    CS=plt.contour(lon,lat,ones_arr,levels=[0.5])
    points=max_curve(CS.allsegs[0])
    points_dic={'Lon':points[:,0],'Lat':points[:,1]}
    points_df=pd.DataFrame(data=points_dic)
    points_df.to_csv('coordMaskOnes.csv',index=False)
    list_points=points.tolist()
    plt.close()
    if list_points[0]!=list_points[-1]:
        list_points=list_points + [list_points[0]]
    return list_points  ##asi como sale puede entrarr a roi=ee.Geometry.Polygon(list_points)

def pixel_in_contour(lon,lat,curve):  ##cuenta la cantidad de pixeles dentro de la mascara
    points = np.hstack((lon.reshape((-1,1)), lat.reshape((-1,1))))
    path = matplotlib.path.Path(curve)
    mask = path.contains_points(points)
    return np.sum(mask)