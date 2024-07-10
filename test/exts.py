from flask_sqlalchemy import SQLAlchemy  # 导入 Flask-SQLAlchemy，用于数据库操作
from flask_mail import Mail  # 导入 Flask-Mail，用于发送电子邮件
# from flask_wtf.csrf import CSRFProtect
# 创建 SQLAlchemy 实例
db = SQLAlchemy()

# 创建 Mail 实例
mail = Mail()

# csrf = CSRFProtect()