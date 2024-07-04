from datetime import datetime  # 导入datetime模块，用于设置默认时间

from exts import db  # 从扩展模块导入数据库实例

from .questionmodel import QuestionModel  # 导入QuestionModel类
from .user_model import UserModel  # 导入UserModel类


# 定义AnswerModel类，表示数据库中的“answer”表
class AnswerModel(db.Model):
    # 设置表名
    __tablename__ = "answer"

    # 定义表的列
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)  # 回答内容，不能为空
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间，默认当前时间

    # 定义外键，关联到问题和用户表
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))  # 外键，关联到问题表的id
    author_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))  # 外键，关联到用户表的id

    # 定义关系，用于ORM查询和操作
    # 关系：一个问题可以有多个答案，backref用于在QuestionModel中添加一个虚拟列“answers”，方便查询
    question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))
    # 关系：一个用户可以有多个答案，backref在UserModel中添加一个虚拟列“answers”
    author = db.relationship(UserModel, backref="answers")
