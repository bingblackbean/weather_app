#!/usr/bin/env python
# coding: utf-8

# # Data Collection
# 
# We are using free open api to get the data.A credit to: https://www.7timer.info/. It provide API to get the weather forecast infomation by given geolocation. 
# For example, inputting shanghai will get unique endpoint: https://www.7timer.info/bin/api.pl?lon=121.474&lat=31.23&product=civil&output=json
# 
# Weather forecast information for next few days is returned in this endpoint. 
# By default,CIVIL product is used to present the result.

# ## Send Request
# 
# If we want to use Python to get response from url, we have to use some packages, like requests.
# 
# ```
# ! pip install requests
# 
# ```
# https://docs.python-requests.org/en/latest/
# jump to quickstart of document, and start coding.
# https://docs.python-requests.org/en/latest/user/quickstart/

# In[1]:


import requests


# In[2]:


url = 'https://www.7timer.info/bin/api.pl?lon=121.474&lat=31.23&product=civil&output=json'


# In[3]:


r = requests.get(url)
print(r)
print(r.encoding)
print(type(r.text))


# It is time to parase the response contents to python object, like dict. Keep in mind, by default, requests return the response in json format. Python is integrated standard json package, so we just need to import it and loads the contents.

# In[4]:


import json


# In[5]:


text_j= json.loads(r.text)
print(type(text_j))


# Let us have a glance at text_j dict.

# In[6]:


text_j.keys()


# In[7]:


text_j['product']


# In[8]:


text_j['init']


# In[9]:


text_j['dataseries'][0]

# https://github.com/Yeqzids/7timer-issues/wiki/Wiki


# ## Parse Result
# We are noted that most useful information is kept in "dataseries" element. For this type of data (list of dict), we suggest to use DataFrame to parse it. 
# 

# In[10]:


import pandas as pd


# In[11]:


weather_info = pd.DataFrame(text_j['dataseries'])
weather_info.head(5)


# ## Transform Data
# 
# ### string to datetime
# 
# "init" datetime is quite important, but it is returned as str. It is good practice to convert it to datatime. Since we decide to use DataFrame to parse raw text, consistently, we are using pd.to_datetime function rather than datetime package.

# In[12]:


start_time = pd.to_datetime(text_j['init'],format='%Y%m%d%H')
start_time


# ### int to timedelta
# timepoint column is recorded as "next N" hours from init time, so we can reverse them back to real timestamps.
# 1. convert int to timedelta
# 2. shift init time by using each timedelta

# In[13]:


# convert timepoint to timestamp
weather_info['timepoint'] = pd.to_timedelta(weather_info['timepoint'],unit='h')


# In[14]:


weather_info['timestamp'] = start_time+ weather_info['timepoint']


# In[15]:


weather_info.head(5)


# 
# ## From City Name to Geolocation
# what if we want to get weather info by inputing the city name? We have to get the geolocation (longitude and latitude) from city name. Luckily, there are multiple wheels for this and geopy is one of them.
# 
# ```
# pip install geopy
# ```
# ***More info about geopy: ***
# https://geopy.readthedocs.io/en/stable/

# In[16]:


from geopy.geocoders import Nominatim


# In[17]:


geolocator = Nominatim(user_agent='baidu')
location = geolocator.geocode("shanghai")
print(location.address)
print((location.latitude, location.longitude))


# So far, we know how to request the weather info by inputing the city name step by step. The codes shall be sorted somehow before we move to next functionality design.
