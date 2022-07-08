import collection as col
import timeseries as ts
import figures as figu
import csv
import matplotlib.pyplot as plt

def compare_csv(filename1, filename2):
    t1 = open(filename1, 'r')
    t2 = open(filename2, 'r')
    fileone = t1.readlines()
    filetwo = t2.readlines()
    t1.close()
    t2.close()

    return (fileone == filetwo)

#initial_date = '2018-07-01'
#final_date = '2018-10-01'

initial_date='2018-07-01'
final_date   ='2021-01-01'

col.initialize()
col.collection_mean(initial_date, final_date) #esta funcion igual creo que la vamos a sacar

print("Initialize y collection_mean corrieron")

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

roi = ts.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)

print("geometría creada")

df = ts.time_series_df(roi,initial_date,final_date,file_name='../actual_outcomes/raw.csv')
df_daily = ts.ts_dailydf(df, file_name= '../actual_outcomes/daily.csv')
df_monthly = ts.ts_monthlydf(df, file_name= '../actual_outcomes/monthly.csv')
df_w = ts.ts_weeklydf(df, file_name= '../actual_outcomes/weekly.csv')

print("time_series_df, daily, monthly y weekly corrieron")
"""
#tener los expected_outcomes de antes
assert(compare_csv('../actual_outcomes/raw.csv','../expected_outcomes/NO2trop_series.csv'))
assert(compare_csv('../actual_outcomes/daily.csv','../expected_outcomes/dailymean_df.csv'))
assert(compare_csv('../actual_outcomes/monthly.csv','../expected_outcomes/monthlymean_df.csv'))
assert(compare_csv('../actual_outcomes/weekly.csv','../expected_outcomes/weeklymean_df.csv'))

print("time_series_df, daily, monthly y weekly dieron bien")

ts.ts_dailydf(df, statistic = 'median')
ts.ts_monthlydf(df, statistic = 'median')
ts.ts_weeklydf(df, statistic = 'median')

print("daily, monthly y weekly con median corrieron")
"""
#figu.plot_series(df_daily)
#figu.plot_series(df_w, filename = "weekly_series.png", show = True)


inicio = '2018-08-15'
fin = '2018-09-06'

#figu.plot_series(df_daily, start = inicio, end = fin, show = True)

#figu.plot_autocorr(df_daily, lags = 22, show = True)

figu.barplot_year_cmp(df_monthly, 2019, 2020, show=True)

var = figu.interanual_variation(df_monthly, 2019, 2020, month_num = 3)
print("La variación interanual para abril 2020-2019 es: ",var)
