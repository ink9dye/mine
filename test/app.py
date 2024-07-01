from flask import Flask, session, g
# g为global，全局
from flask_migrate import Migrate

import config
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from exts import db, mail  # 导入 exts.py 中的 db
from models import UserModel

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)  # 加载开发环境配置
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
db.init_app(app)  # 使用应用实例初始化 db，即先创建再初始化
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(auth_bp)

# 注册qa蓝图
app.register_blueprint(qa_bp)


# 钩子函数，即在正常流程中插入优先执行的函数


@app.before_request
def load_user():
    user_id = session.get("user_id")
    # 从session中尝试获取user_id。session是一个特殊的字典，
    # 用于在客户端和服务器之间持久化数据，例如，存储已登录用户的ID。
    if user_id:
        # 检查是否成功从session中获取到user_id。如果获取到，表示用户可能已登录。
        if not hasattr(g, 'user'):
            # 检查g对象（每个请求都有一个独立的g对象）是否已经设置了user属性。
            # 这是为了避免在同一个请求中多次从数据库加载用户信息。(即不用把该函数的代码再重复一遍)
            g.user = db.session.get(UserModel, user_id)
            # 如果g对象尚未有user属性，从数据库中加载对应user_id的用户对象，并
            # 将其设置给g.user。这样，应用的其他部分就可以直接使用g.user访问当前用户信息。

    else:
        g.user = None
        #如果session中没有user_id，将g.user设置为None，表示当前没有用户登录。


@app.context_processor
def my_context_processor():
    # 将当前请求的用户对象添加到所有模板的上下文，方便HTML模板访问和显示用户信息。
    # 'g.user' 由 before_request 钩子设置，可能为 None（未登录用户）。
    # 这使得模板中可以通过 {{ user }} 直接访问用户信息，简化了用户状态的展示逻辑。
    return {"user": g.user}



if __name__ == "__main__":
    # with app.app_context():
    # db.drop_all()
    # db.create_all()
    app.run()
