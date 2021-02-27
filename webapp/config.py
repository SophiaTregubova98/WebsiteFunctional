from datetime import timedelta
import os

basedir = os.path.dirname(__file__)

REMEMBER_COOKIE_DURATION = timedelta(days=10)
SECRET_KEY = 'knbkrciv3$##654eSDFFrfdwuw'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEATHER_CITY = 'Anapa,Russia'
WEATHER_API_KEY = '31dbacb1b6ee4076b85113151200811'
