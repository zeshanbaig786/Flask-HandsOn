#config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mypass@localhost:3306/flaskapp"
    #@staticmethod
    # def init_app(app):
    #     pass

# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mypass@localhost:3306/flaskapp"#os.getenv("DEV_DATABASE_URL")

# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mypass@localhost:3306/flaskapp"#os.getenv("TEST_DATABASE_URL")

# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mypass@localhost:3306/flaskapp"#os.getenv("DATABASE_URL")

# config = {
#     "development": DevelopmentConfig,
#     "testing": TestingConfig,
#     "production": ProductionConfig,
#     "default": DevelopmentConfig
# }