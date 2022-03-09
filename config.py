import os
import pyodbc

from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))

conn_str = "mysql+mysqlconnector://teamixn9@database4:Uclcsixn9@database4.mysql.database.azure.com/ixn9"

engine_azure = create_engine(conn_str,echo=True)
# engine_azure.connect()

# print(engine_azure.table_names())

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'afygawyufgwauyf'
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



