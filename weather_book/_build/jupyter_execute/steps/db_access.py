#!/usr/bin/env python
# coding: utf-8

# # Save Data to SQLite
# 
# ## Prepare Data
# Since we have tested request api and sorted the codes in previous chapter. In this exercise, we want to re-use the functions, the good practice is to put functions into py file and import them here.
# 
# ***Note: In Pycharm, software helps to add content root path into syspath, if we are using notebook, we have to add content root path into syspath manuallly.***

# In[1]:


import os
import sys

module_path = os.path.abspath(os.path.join('..'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)


# In[2]:


from weather_app.models.query_api import get_geo_from_city,generate_url,request_weather_info,transform_weather_raw,add_city_info


# In[3]:


city = 'shanghai'
lon, lat = get_geo_from_city(city)
url = generate_url(lon, lat)
text_j = request_weather_info(url)
weather_info_df = transform_weather_raw(text_j)
weather_info_df = add_city_info(weather_info_df, lon, lat, city)
weather_info_df


# ## Using SQLite
# We can use any relational database to save the data. But here I strongly suggest to use SQLite, as it is lightest but still powerful. Even you don't need to waste time to install it.
# 
# SQLite is not directly comparable to client/server SQL database engines such as MySQL, Oracle, PostgreSQL, or SQL Server since SQLite is trying to solve a different problem.
# ## Using sqlalchemy
# Anyway, we are using another powerful library to handle the database access. It is sqlalchemy, indeed.   SQLAlchemy consists of two distinct components, known as the Core and the ORM.
# 
# ```
# pip install sqlalchemy
# ```
# 
# https://docs.sqlalchemy.org/en/14/tutorial/index.html

# In[4]:


from sqlalchemy import create_engine


# In[5]:


engine = create_engine('sqlite:///weather.db')


# In[6]:


engine


# In[7]:


from sqlalchemy.orm import Session


# In[8]:


session = Session(engine)


# In[9]:


session


# ## Create Table by Using ORM 
# The Declarative Mapping is the typical way that mappings are constructed in modern SQLAlchemy. The most common pattern is to first construct a base class using the declarative_base() function, which will apply the declarative mapping process to all subclasses that derive from it. (https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)
# 
# Refering to DataFrame structure, we create a Python class and include each column in DataFrame as attribute in class.
# Each class attribute indicates specific column in the table.

# In[10]:


# create database table by defining python class
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,Float
Base = declarative_base()


# In[11]:


class WeatherInfo(Base):
    __tablename__ = 'weather'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True,autoincrement=True)  # use autoincrement
    timestamp = Column(String(55))
    cloudcover = Column(Integer)
    lifted_index = Column(Integer)
    prec_type = Column(String(10))
    prec_amount = Column(Integer)
    temp2m = Column(Integer)
    rh2m = Column(Integer)
    weather = Column(String(20))
    wind_direction = Column(String(4))
    wind_speed = Column(Integer)
    longitude = Column(Float(precision=10, decimal_return_scale=2))
    latitude = Column(Float(precision=10, decimal_return_scale=2))
    city=Column(String(50))
        


# ## Query and Insert Data from Database
# As you can see below, the query get 0 result since the table is created as brand new.
# 
# After we insert the DataFrame into database, the newer query gets data.
# 
# Keep in mind to close the session after all transactions.

# In[12]:


Base.metadata.create_all(engine)
result = session.query(WeatherInfo).all()
len(result)


# In[13]:


weather_info_df.to_sql('weather',engine,if_exists='append',index=False) # without index


# In[14]:


result = session.query(WeatherInfo).all()
len(result)


# In[15]:


session.close()

