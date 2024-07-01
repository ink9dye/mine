from exts import db
from datetime import  datetime
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'  # 确保表名定义正确
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 定义主键列
    email=db.Column(db.String(100), nullable=False,unique=False)
    captcha=db.Column(db.String(100), nullable=False)