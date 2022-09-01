import numpy as np

def roi_rectangle():
    print('Select a region of interest. It must be a latitude longitude rectangle.')
    print('Enter the latitude of the northern limit. Type a float number between -90 to 90')

    while True:
        try:
            lat_n=input()
            lat_n = float(lat_n)
        except ValueError:
            print(lat_n, ' is not a number, please enter a number')
        else:
            if -90 <= lat_n <= 90: 
                break
            else:
                print(lat_n, ' is not within range, please enter a valid number')

    print('Enter the latitude of the southern limit')

    while True:
        try:
            lat_s = input()
            lat_s = float(lat_s)
        except ValueError:
            print(lat_s, 'is not a number, please enter a number')
        else:
            if -90 <= lat_s <= 90:
                if lat_s>= lat_n:
                    print('The southern limit must be smaller than the northern limit')
                else:
                    break
            else:
                print(lat_s, 'is not within range, please enter a valid number')

    print('Enter the longitude of the western limit. Type a float number between -180 to 180')

    while True:
        try:
            lon_w = input()
            lon_w = float(lon_w)
        except ValueError:
            print(lon_w, 'is not a number, please enter a number')
        else:
            if -180 <= lon_w <= 180:
                    break
            else:
                print(lon_w, 'is not within range, please enter a valid number')


    print('Enter the longitude of the eastern limit')

    while True:
        try:
            lon_e = input()
            lon_e = float(lon_e)
        except ValueError:
            print(lon_e, 'is not a number, please enter a number')
        else:
            if -180 <= lon_e <= 180:
                if lon_w>= lon_e:
                    print('The western limit must be smaller than the eastern limit')
                else:
                    break
            else:
                print(lon_e, 'is not within range, please enter a valid number')

    
    print('The region of interest is [',lat_s,',',lat_n,']x[',lon_w,',',lon_e,']')
    lat_s=np.round(lat_s,2)
    lat_n=np.round(lat_n,2)
    lon_w=np.round(lon_w,2)
    lon_e=np.round(lon_e,2)
    return  lat_s,lat_n,lon_w,lon_e