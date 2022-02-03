#!/usr/bin/env python
# coding: utf-8

# # Clean the Code
# we will sort the request api code and make it neater

# ## Create Functions
# To make full use of code, mulitple functions are created. 

# In[1]:


import requests
import json
import pandas as pd
from geopy.geocoders import Nominatim


# In[2]:


# function to get url by inputing the city name

def get_geo_from_city(city):
    geolocator = Nominatim(user_agent='baidu')
    location = geolocator.geocode(city)
    return location.longitude,location.latitude

def generate_url(longitude,latitude):
    url = f'https://www.7timer.info/bin/api.pl?lon={longitude}&lat={latitude}&product=civil&output=json'
    return url

# function get weather raw info
def request_weather_info(url):
    r = requests.get(url)
    text_j= json.loads(r.text)
    return text_j


# In[3]:


# test functions
city='shanghai'
lon,lat = get_geo_from_city(city)
url = generate_url(lon,lat)
text_j = request_weather_info(url)
text_j['dataseries'][0]


# ## More Data Transformation
# 1. we will split the wind information to multiple columns
# 2. For future usage, more info is inserted into dataframe, e.g. city_name, 

# In[4]:


# transform data

def transform_weather_raw(text_j):
    weather_info = pd.DataFrame(text_j['dataseries'])
    start_time = pd.to_datetime(text_j['init'],format='%Y%m%d%H')
    weather_info['timepoint'] = pd.to_timedelta(weather_info['timepoint'],unit='h')
    weather_info['timestamp'] = start_time+ weather_info['timepoint']
    weather_info.drop('timepoint',axis=1,inplace=True)
    # more clean data steps
    wind_df = pd.json_normalize(weather_info['wind10m'])
    wind_df.columns = ['wind_'+col for col in wind_df.columns]
    weather_info = pd.concat([weather_info,wind_df],axis=1)
    weather_info.drop('wind10m',axis=1,inplace=True)
    weather_info['rh2m'] = weather_info['rh2m'].str.rstrip('%')
    #['']
    return weather_info

def add_city_info(weather_info,longitude,latitude,city):
    weather_info['longitude'] = longitude
    weather_info['latitude'] = latitude
    weather_info['city'] = city
    return weather_info

weather_info_df = transform_weather_raw(text_j)
weather_info_df = add_city_info(weather_info_df,lon,lat,city)
weather_info_df

