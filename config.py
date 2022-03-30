import os
import pyodbc

from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))

conn_str = 'mssql+pymssql://sa:UCLCSixn2122@20.127.94.166/ixn' 

engine_azure = create_engine(conn_str,echo=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'afasfsafafs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = conn_str

class TestingConfig(Config): 
    TESTING = True
    SQLALCHEMY_DATABASE_URI = conn_str

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = conn_str

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}



