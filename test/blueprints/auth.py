import random
import string

from exts import mail, db
from flask import Blueprint, render_template, url_for, request, jsonify, redirect, session, flash, \
    make_response
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
# 当你尝试从当前目录下的模块或包中导入时，在导入语句中使用点（.）表示相对导入。
# 如果没有使用.进行相对导入，Python解释器会在Python的安装路径下的site-packages目录，
# 以及环境变量PYTHONPATH指定的目录中查找forms模块，而不是在当前目录下查找。
# 这就是为什么你遇到了ModuleNotFoundError错误：解释器没有在预期的位置找到forms模块。
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import RegisterForm, LoginForm  # 同一目录的话，就要用.

bp = Blueprint("auth", __name__, url_prefix="/auth")


# 没有指定methods参数则默认get请求,get是获得，post是发送（提交）
@bp.route("/login", methods=["GET", "POST"])
# 在你的login路由处理函数中，当处理POST请求（即用户提交表单时）的逻辑被触发，
# 你通过创建LoginForm实例并传递request.form给它来处理表单数据。
# request.form包含了POST请求体中的数据，这通常是用户在表单字段中输入的数据。
# 即使你没有显式地向登录表单输入数据，request.form依然会捕获表单中所有字段的值，包括密码字段。
def login():
    form = LoginForm(request.form)
    if request.method == "GET":
        return render_template("login.html", form=form)
    else:
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                session["user_id"] = user.id
                return redirect(url_for('qa.index'))
            else:
                flash("邮箱或密码不正确，请重试。", 'error')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", 'error')

    return render_template("login.html", form=form)


@bp.route('/logout')
def logout():
    # 清除Flask会话
    session.clear()
    # 创建响应对象
    response = make_response(redirect(url_for("auth.login")))
    # 清除所有相关Cookies
    response.delete_cookie('session')  # Flask默认的会话Cookie
    return response


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()  # 在处理GET和POST请求之前创建form实例
    if request.method == 'POST':
        if form.validate_on_submit():  # 使用validate_on_submit()来简化验证流程
            # 检查邮箱是否已被注册
            existing_user = UserModel.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('该邮箱已被注册，请使用其他邮箱。', 'error')
                return render_template("register.html", form=form)

            # 邮箱未被注册，处理注册逻辑
            email = form.email.data
            username = form.username.data
            password = form.password.data
            hashed_password = generate_password_hash(password)  # 对密码进行哈希加密
            user = UserModel(email=email, username=username, password=hashed_password)
            try:
                db.session.add(user)
                db.session.commit()
                flash('注册成功，请登录。', 'success')
                return redirect(url_for("auth.login"))
            except Exception as e:
                db.session.rollback()
                flash('注册失败，请稍后再试。', 'error')
                print(e)
        else:
            flash('注册失败，请检查您的输入。', 'error')
            print(form.errors)
    # 对于GET请求和验证失败的POST请求，都重新渲染注册页面并传递form实例
    return render_template("register.html", form=form)


# 渲染注册页面的模板
# 表单验证:flask-wtf:wtforms
# 检验是否提交正确
@bp.route("/captcha/email")
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email/email=xxx@qq.com
    email = request.args.get("email")
    if not email:
        return "No email provided", 400  # Bad Request，验证机制
    # 邮箱验证码要么是4位，要么是6位，数字字母都成，随机
    source = string.digits * 4
    # digits为数字012.....9,*4为四倍(乘字符串可还行)
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)  # 双引号里是去掉的分隔符（由于没有分隔符故空）

    # I/O操作
    try:
        message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
        mail.send(message)
    except Exception as e:
        print(e)
        return "邮件发送失败！", 500  # Internal Server Error

    # memcached（缓存，断电即消失）,redis(定时存硬盘)
    # 此处用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # restful api
    # code:200/400/500(不同的报错)，message："",data:{}
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["1617562300@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"
