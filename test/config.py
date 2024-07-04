class Config():
    # 通用配置
    SECRET_KEY = 'your_secret_key'
    # SQLAlchemy 特定配置，禁用跟踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 基本数据库配置组件
    DB_USERNAME = 'root'  # 数据库用户名
    DB_PASSWORD = 'Aa1278389701'  # 数据库密码
    DB_HOST = '127.0.0.1'  # 数据库主机地址
    DB_PORT = '3306'  # 默认为mysql监听的端口号
    DB_NAME = 'python'  # 数据库名称

class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True  # 启用调试模式
    SECRET_KEY = 'some_random_secret_key'  # 防止csrf攻击
    # 使用 MySQL 数据库的 URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
    # URI将配置信息都写在一个字符串上，使得配置更加简洁和便于管理。许多框架和库原生支持这种配置方式。

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"  # 邮件服务器
    MAIL_USE_SSL = True  # 使用 SSL
    MAIL_PORT = 465  # 端口号
    MAIL_USERNAME = "1278389701@qq.com"  # 邮件服务器用户名
    MAIL_PASSWORD = "jglnjhznbdcchjdc"  # 邮件服务器密码
    MAIL_DEFAULT_SENDER = "1278389701@qq.com"  # 默认发件人

class TestingConfig(Config):
    # 测试环境配置
    TESTING = True  # 启用测试模式
    # 使用内存中的 SQLite 数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    # 生产环境配置
    PROD_DB_USERNAME = 'user'  # 生产环境数据库用户名
    PROD_DB_PASSWORD = 'password'  # 生产环境数据库密码
    PROD_DB_HOST = 'host'  # 生产环境数据库主机地址
    PROD_DB_PORT = 'port'  # 生产环境数据库端口
    PROD_DB_NAME = 'database'  # 生产环境数据库名称
    # 使用生产环境的 MySQL 数据库 URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{PROD_DB_USERNAME}:{PROD_DB_PASSWORD}@{PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_NAME}'
