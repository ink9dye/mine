from exts import db
from datetime import datetime
from .user_model import UserModel

class QuestionModel(db.Model):
    __tablename__ = "question"  # 注意是两个下划线，并确保这里使用正确的属性名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 正确的类型是 db.DateTime
    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))  # 确保外键的字符串引用的是正确的表名和字段名
    author = db.relationship(UserModel, backref="questions")
