from flask import Flask, session, g  # 导入 Flask、session 和 g 对象
from flask_migrate import Migrate  # 导入 Flask-Migrate，用于数据库迁移
from sqlalchemy import text,inspect  # 导入 sqlalchemy.text
import config  # 导入配置模块
from blueprints.auth import bp as auth_bp  # 导入 auth 蓝图并重命名为 auth_bp
from blueprints.qa import bp as qa_bp  # 导入 qa 蓝图并重命名为 qa_bp
from exts import db, mail  # 从 exts 模块导入 db 和 mail
from models import UserModel  # 从 models 模块导入 UserModel
import sys

app = Flask(__name__)  # 创建 Flask 应用实例
app.config.from_object(config.DevelopmentConfig)  # 加载开发环境配置

# 初始化数据库和邮件服务
db.init_app(app)  # 使用应用实例初始化 db，即先创建再初始化(相当于db = SQLAlchemy(app))
# SQLAlchemy 实例db读取并使用 Flask 应用实例 app 中配置的数据库连接信息
# （主要就是SQLALCHEMY_DATABASE_URI）来初始化和管理与数据库的连接。

mail.init_app(app)

# 创建数据库迁移对象
migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(auth_bp)  # 注册 auth 蓝图
app.register_blueprint(qa_bp)  # 注册 qa 蓝图

# 钩子函数，即在正常流程中插入优先执行的函数
@app.before_request
def load_user():
    user_id = session.get("user_id")
    # 从 session 中尝试获取 user_id。session 是一个特殊的字典，
    # 用于在客户端和服务器之间持久化数据，例如，存储已登录用户的 ID。
    if user_id:
        # 检查是否成功从 session 中获取到 user_id。如果获取到，表示用户可能已登录。
        if not hasattr(g, 'user'):
            # 检查 g 对象（每个请求都有一个独立的 g 对象）是否已经设置了 user 属性。
            # 这是为了避免在同一个请求中多次从数据库加载用户信息。
            g.user = db.session.get(UserModel, user_id)
            # 如果 g 对象尚未有 user 属性，从数据库中加载对应 user_id 的用户对象，并
            # 将其设置给 g.user。这样，应用的其他部分就可以直接使用 g.user 访问当前用户信息。
    else:
        g.user = None
        # 如果 session 中没有 user_id，将 g.user 设置为 None，表示当前没有用户登录。

# 测试数据库是否已经连接
def check_database_connection():
    try:
        # 使用上下文管理器 with 来确保数据库连接在使用后正确关闭
        with db.engine.connect() as conn:
            # 创建一个检查器对象 inspector，允许你检查数据库结构
            inspector = inspect(conn)
            # 获取数据库中的表列表
            tables = inspector.get_table_names()

            # 如果表列表不为空，打印成功消息和表名列表
            if tables:
                print(f"数据库连接成功. 库中的表为: {tables}")
            else:
                print("数据库连接成功. 但没找到表")
    except Exception as e:  # 捕获任何异常
        # 捕获并打印失败消息和异常信息
        print(f"数据库连接失败: {e}")
        # 使用 sys.exit(1) 终止应用并返回状态码 1 表示失败
        sys.exit(1)  # 终止应用


@app.context_processor
def my_context_processor():
    # 将当前请求的用户对象添加到所有模板的上下文，方便 HTML 模板访问和显示用户信息。
    # 'g.user' 由 before_request 钩子设置，可能为 None（未登录用户）。
    # 这使得模板中可以通过 {{ user }} 直接访问用户信息，简化了用户状态的展示逻辑。
    return {"user": g.user}

if __name__ == "__main__":
    # 使用应用上下文检查数据库连接
    with app.app_context():
        check_database_connection()  # 检查数据库连接
    app.run(debug=True)
