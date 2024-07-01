class Config(object):
    # 通用配置
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 基本数据库配置组件
    DB_USERNAME = 'root'
    DB_PASSWORD = 'Aa1278389701'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'python'

class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True
    SECRET_KEY = 'some_random_secret_key'  # 添加这一行以使用flask-wtf
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "1278389701@qq.com"
    MAIL_PASSWORD = "jglnjhznbdcchjdc"
    MAIL_DEFAULT_SENDER = "1278389701@qq.com"
class TestingConfig(Config):
    # 测试环境配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    # 生产环境配置
    PROD_DB_USERNAME = 'user'
    PROD_DB_PASSWORD = 'password'
    PROD_DB_HOST = 'host'
    PROD_DB_PORT = 'port'
    PROD_DB_NAME = 'database'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{PROD_DB_USERNAME}:{PROD_DB_PASSWORD}@{PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_NAME}'
