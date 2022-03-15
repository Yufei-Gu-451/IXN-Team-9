import os
import pyodbc

from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))

conn_str = "mysql+mysqlconnector://teamixn9@ixn9:Uclcsixn9@ixn9.mysql.database.azure.com/ixn9"

engine_azure = create_engine(conn_str,echo=True)
# engine_azure.connect()

# print(engine_azure.table_names())

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



