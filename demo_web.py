import pandas as pd
import matplotlib.pyplot as plt
import respyrar as rs 
from datetime import datetime
import streamlit as st

st. set_page_config(layout="wide") 

st.write("""
# ResPyrAR
## El sitio de prueba oficial
""")
 

import ee

# Definitions

jan19 = '2019-01-01'
march19 = '2019-03-01'
may19 = '2019-05-01'
jan21 = '2021-01-01'

date_format = "%Y-%m-%d"

jan19_object = datetime.strptime(jan19, date_format)
march19_object = datetime.strptime(march19, date_format)
may19_object = datetime.strptime(may19, date_format)
jan21_object = datetime.strptime(jan21, date_format)

lat_n=-34.52
lat_s=-34.73
lon_w=-58.56
lon_e=-58.33

reds = [ee.Reducer.mean(), ee.Reducer.min()] # the spatial reducers we'll be using
names = ['NO2_trop_mean','NO2_trop_min'] # their names

arg_shapefile = "./ResPyrAR/data/arg/departamento.shp" 

def test_time_series(start, end, roi):
    
    df = rs.time_series_df(roi,start,end,filename='raw.csv',reducers = reds, red_names = names)
    df_daily = rs.ts_dailydf(df, filename= 'daily.csv')
    df_weekly = rs.ts_weeklydf(df, filename= 'weekly.csv')
    df_monthly = rs.ts_monthlydf(df, filename= 'monthly.csv')

    return df, df_daily, df_weekly, df_monthly

def test_tseries_median(df):
    median_daily = rs.ts_dailydf(df, statistic = 'median')
    median_weekly = rs.ts_weeklydf(df, statistic = 'median')
    median_monthly = rs.ts_monthlydf(df, statistic = 'median')

    return median_daily, median_weekly, median_monthly

print("Create geometry of Buenos Aires")
ba_roi = rs.geometry_rectangle(lon_w,lat_s,lon_e,lat_n)

# Basics

d_start, d_end = st.date_input(
    "Select the time period to analyze",
    (march19_object, may19_object),
    format="DD-MM-YYYY"
)
d_start = d_start.strftime(date_format)
d_end = d_end.strftime(date_format)


print("Obtain dataframes with NO2 time series. Aggregate using mean")
df, df_d, df_w, df_m = test_time_series(d_start, d_end, ba_roi)

print("Show and save plots for these series")
fig_d, ax_d = rs.plot_series(df_d,show = False) #save with default name: series.png
fig_w, ax_w = rs.plot_series(df_w, filename = 'weekly.png', show = False)
fig_m, ax_m = rs.plot_series(df_m, filename = 'monthy.png', show = False)

period = st.radio(
    "Granularity",
    ["Daily", "Weekly", "Monthly"])

if period == 'Daily':
    st.pyplot(fig_d)
elif period == 'Weekly':
    st.pyplot(fig_w)
elif period == 'Monthly':
    st.pyplot(fig_m)





