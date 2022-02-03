#!/usr/bin/env python
# coding: utf-8

# # Present Data in Plotly
# 

# In[1]:


import os
import sys

module_path = os.path.abspath(os.path.join('../..'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)


# In[2]:


from weather_book.weather_app.models.db_models import engine,WeatherInfo

import pandas as pd


# In[3]:


df = pd.read_sql_table(WeatherInfo.__tablename__,engine)


# In[4]:


df.shape


# In[5]:


df.drop_duplicates(subset=['city'], keep='last',inplace=True)
df.shape


# In[6]:


df.head()


# In[7]:


import plotly.graph_objects as go
fig = go.Figure(go.Densitymapbox(lat=df.latitude, lon=df.longitude, z=df.cloudcover,
                                 radius=20))
fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180,mapbox_zoom=1)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


# In[ ]:




