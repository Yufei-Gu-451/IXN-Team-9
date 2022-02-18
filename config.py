import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'afygawyufgwauyf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:Shamrock_640@localhost/translAIte"

class TestingConfig(Config): 
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:Shamrock_640@localhost/translAIte"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:Shamrock_640@localhost/translAIte"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

