#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# https://simplemaps.com/data/world-cities

# In[2]:


city_file = '../data/worldcities.csv'
city_df = pd.read_csv(city_file,encoding='utf-8')


# In[3]:


city_df


# In[4]:


capital_china = city_df[(city_df['country']=='China') & (city_df['capital'] is not None)]
capital_china


# In[5]:


import os
import sys

module_path = os.path.abspath(os.path.join('..'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)


# In[6]:


from weather_app.models.query_api import get_geo_from_city,generate_url,request_weather_info,transform_weather_raw,add_city_info


# In[7]:


city_info = capital_china.iloc[0,:].to_dict()
city_info


# https://github.com/spyoungtech/grequests
# 
# 

# In[8]:


city = city_info['city']
lon = city_info['lng']
lat = city_info['lat']
url = generate_url(longitude=lon,latitude=lat)
text_j = request_weather_info(url)
weather_info_df = transform_weather_raw(text_j)
weather_info_df = add_city_info(weather_info_df,lon,lat,city)
weather_info_df


# In[9]:


from tqdm.notebook  import tqdm
all_cities_df = pd.DataFrame()
for index,city_info in tqdm(capital_china.iloc[0:20,:].iterrows()):
    city = city_info['city']
    print(city)
    lon = city_info['lng']
    lat = city_info['lat']
    url = generate_url(longitude=lon,latitude=lat)
    text_j = request_weather_info(url)
    weather_info_df = transform_weather_raw(text_j)
    weather_info_df = add_city_info(weather_info_df,lon,lat,city)
    all_cities_df = pd.concat([all_cities_df,weather_info_df],axis=0)


# In[11]:


all_cities_df.head()


# In[ ]:




