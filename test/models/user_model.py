from exts import db
from datetime import  datetime
class UserModel(db.Model):
    __tablename__ = 'user_model'  # 确保表名定义正确
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 定义主键列
    username=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(512), nullable=False)#因为哈希算法，所以要大一点
    email=db.Column(db.String(100), nullable=False,unique=True)

