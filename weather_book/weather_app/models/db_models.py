from weather_book.weather_app.models.query_api import generate_url,request_weather_info,transform_weather_raw,add_city_info
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,Float


engine = create_engine('sqlite:///weather.db')
Base = declarative_base()


class WeatherInfo(Base):
    """:param
    create table in database
    """
    __tablename__ = 'weather'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)  # use autoincrement
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
    city = Column(String(50))

Base.metadata.create_all(engine)


if __name__ == '__main__':
    # test functions
    city = 'shanghai'
    url,location = generate_url(city)
    text_j = request_weather_info(url)
    weather_info_df = transform_weather_raw(text_j)
    weather_info_df = add_city_info(weather_info_df,location,city)
    weather_info_df.to_sql('weather',engine,if_exists='append',index=False) # without index
    session = Session(engine)
    result = session.query(WeatherInfo).all()
    print(len(result))
    print(result[0].__dict__)
    session.close()