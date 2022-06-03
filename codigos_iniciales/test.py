import collection as col
import timeseries as ts
import csv

def compare_csv(filename1, filename2):
    t1 = open(filename1, 'r')
    t2 = open(filename2, 'r')
    fileone = t1.readlines()
    filetwo = t2.readlines()
    t1.close()
    t2.close()

    return (fileone == filetwo)

initial_date = '2018-07-01'
final_date = '2018-10-01'

col.initialize()
col.collection_mean(initial_date, final_date)

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

df = ts.time_series_df(lon_w,lat_s,lon_e,lat_n,initial_date,final_date,file_name='../actual_outcomes/raw.csv')
ts.ts_dailydf(df, file_name= '../actual_outcomes/daily.csv')
ts.ts_monthlydf(df, file_name= '../actual_outcomes/monthly.csv')
ts.ts_weeklydf(df, file_name= '../actual_outcomes/weekly.csv')

assert(compare_csv('../actual_outcomes/raw.csv','../expected_outcomes/NO2trop_series.csv'))
assert(compare_csv('../actual_outcomes/daily.csv','../expected_outcomes/dailymean_df.csv'))
assert(compare_csv('../actual_outcomes/monthly.csv','../expected_outcomes/monthlymean_df.csv'))
assert(compare_csv('../actual_outcomes/weekly.csv','../expected_outcomes/weeklymean_df.csv'))
