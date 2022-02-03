#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


city_file = '../data/worldcities.csv'
city_df = pd.read_csv(city_file,encoding='utf-8')
city_df


# In[3]:


capital_china = city_df[(city_df['country']=='China') & (city_df['capital'] is not None)]
capital_china


# In[4]:


def generate_url(longitude,latitude):
    url = f'https://www.7timer.info/bin/api.pl?lon={longitude}&lat={latitude}&product=civil&output=json'
    return url

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


# In[5]:


import grequests
import json
from tqdm.notebook import tqdm
city_list = []
lon_list = []
lat_list = []
url_list = []
for index,city_info in capital_china.iterrows():
    city = city_info['city']
    city_list.append(city)
    lon = city_info['lng']
    lon_list.append(lon)
    lat = city_info['lat']
    lat_list.append(lat)
    url = generate_url(longitude=lon,latitude=lat)
    url_list.append(url)
    
rs = (grequests.get(u) for u in url_list)
all_cities_df = pd.DataFrame()
for i,r in tqdm(enumerate(grequests.imap(rs, size=50))):
    text_j= json.loads(r.text)
    weather_info_df = transform_weather_raw(text_j)
    weather_info_df = add_city_info(weather_info_df,lon_list[i],lat_list[i],city_list[i])
    all_cities_df = pd.concat([all_cities_df,weather_info_df],axis=0)


# In[8]:


import os
import sys

module_path = os.path.abspath(os.path.join('../..'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)
from weather_book.weather_app.models.db_models import engine,WeatherInfo
all_cities_df['id'] = [i for i in range(all_cities_df.shape[0])]
all_cities_df.to_sql('weather',engine,if_exists='append',index=False) # without index


# In[ ]:




