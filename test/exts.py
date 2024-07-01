from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
#为了解决循环引用而出现的文件
db = SQLAlchemy()
mail = Mail()