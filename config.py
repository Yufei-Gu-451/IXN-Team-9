import os
import pyodbc
import urllib

from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))

# params = urllib.parse.quote_plus(r'Driver=/usr/local/lib/libmsodbcsql.17.dylib;Server=tcp:uclcs-ixn-9-2122.database.windows.net,1433;Database=database2;Uid=yufei.gu.20@ucl.ac.uk;Pwd=Uclcsixn9;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')


params = urllib.parse.quote_plus(
    'Driver=%s;' % '/usr/local/lib/libmsodbcsql.17.dylib' +
    'Server=tcp:%s,1433;' % 'uclcs-ixn-9-2122.database.windows.net' +
    'Database=%s;' % 'database2' +
    'Uid=%s;' % 'yufei.gu.20@ucl.ac.uk@uclcs-ixn-9-2122.database.windows.net' +
    'Pwd={%s};' % 'Uclcsixn9' +
    'Encrypt=yes;' +
    'TrustServerCertificate=no;' +
    'Connection Timeout=30;')

# conn_str = "mssql+pyodbc:///?odbc_connect=%s" % params
conn_str = "mysql://root:Shamrock_640@localhost/translAIte"

# conn_str = "mssql://Driver={ODBC Driver 17 for SQL Server};Server=tcp:uclcs-ixn-9-2122.database.windows.net,1433;Database=database2;UserID=yufei.gu.20@ucl.ac.uk@uclcs-ixn-9-2122.database.windows.net;Password=Uclcsixn9;Trusted_Connection=False;Encrypt=True;"
# conn_str = 'mssql+pymssql://yufei.gu.20@ucl.ac.uk@uclcs-ixn-9-2122.database.windows.net:Uclcsixn9@uclcs-ixn-9-2122.database.windows.net'

# conn_str = "mssql+pyodbc://uclcs-ixn-9-2122.database.windows.net/database2?driver=/usr/local/lib/libmsodbcsql.17.dylib?trusted_connection=yes?UID" \
#                               "=database2?PWD=Uclcsixn9"
engine_azure = create_engine(conn_str,echo=True)
engine_azure.connect()

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



