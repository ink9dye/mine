from flask import Flask, session, request, g, jsonify
from flask_migrate import Migrate
from sqlalchemy import inspect
import config
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from exts import db, mail
from models import UserModel
import sys
from flask_cors import CORS
import functools
from flask_wtf.csrf import generate_csrf

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

# 初始化数据库和邮件服务
db.init_app(app)
mail.init_app(app)

# 创建数据库迁移对象
migrate = Migrate(app, db)
CORS(app)

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)

@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id:
        if not hasattr(g, 'user'):
            g.user = db.session.get(UserModel, user_id)
    else:
        g.user = None

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = generate_csrf()
    csrf_token = session['csrf_token'].replace('\n', '').replace('\r', '')
    return jsonify({'csrf_token': csrf_token}), 200

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'error': 'Unauthorized', 'message': '请登录后访问资源'}), 401
        return view(**kwargs)
    return wrapped_view

def check_database_connection():
    try:
        with db.engine.connect() as conn:
            inspector = inspect(conn)
            tables = inspector.get_table_names()
            if tables:
                print(f"数据库连接成功. 库中的表为: {tables}")
            else:
                print("数据库连接成功. 但没找到表")
    except Exception as e:
        print(f"数据库连接失败: {e}")
        sys.exit(1)

@app.context_processor
def my_context_processor():
    return {"user": g.user}

if __name__ == "__main__":
    with app.app_context():
        check_database_connection()
    app.run(debug=True)
