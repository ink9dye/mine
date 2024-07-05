import random
import string
from flask import Blueprint, render_template, url_for, request, jsonify, redirect, session, flash, make_response  # 导入 Flask 相关模块和函数
from flask_mail import Message # 导入 Flask-Mail 的 Message 类，用于创建邮件消息
from werkzeug.security import generate_password_hash, check_password_hash  # 导入用于密码哈希处理的函数
from flask_wtf.csrf import generate_csrf
from exts import mail, db  # 从 exts 模块导入 mail 和 db 对象，分别用于邮件发送和数据库操作
from models import EmailCaptchaModel, UserModel  # 导入数据库模型 EmailCaptchaModel 和 UserModel
from .forms import RegisterForm, LoginForm  # 从当前目录下导入 RegisterForm 和 LoginForm

# 创建一个蓝图对象 auth_bp，命名为 "auth"，URL 前缀为 "/auth"
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])  # 定义 /login 路由，允许 GET 和 POST 请求
def login():
    form = LoginForm(request.form)  # 创建 LoginForm 实例，传递请求中的表单数据
    if request.method == "GET":  # 如果是 GET 请求，渲染登录页面
        return render_template("login.html", form=form)
    else:  # 如果是 POST 请求，处理登录逻辑
        if form.validate_on_submit():  # 验证表单数据是否有效
            user = UserModel.query.filter_by(email=form.email.data).first()  # 根据表单中的邮箱查找用户
            if user and check_password_hash(user.password, form.password.data):  # 检查用户是否存在且密码正确
                session["user_id"] = user.id  # 将用户 ID 存储在会话中
                return redirect(url_for('qa.index'))  # 重定向到问答主页
            else:  # 如果邮箱或密码不正确，显示错误信息
                flash("邮箱或密码不正确，请重试。", 'error')
        else:  # 如果表单验证失败，显示相应的错误信息
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", 'error')

    return render_template("login.html", form=form)  # 重新渲染登录页面并传递表单实例


@bp.route('/logout')  # 定义 /logout 路由，处理用户注销
def logout():
    session.clear()  # 清除 Flask 会话
    response = make_response(redirect(url_for("auth.login")))  # 创建重定向到登录页面的响应对象
    response.delete_cookie('session')  # 清除会话 Cookie
    return response


@bp.route("/register", methods=["GET", "POST"])  # 定义 /register 路由
def register():
    if request.method == "GET":
        # 为GET请求生成CSRF令牌并返回
        csrf_token = generate_csrf()
        return jsonify({"csrf_token": csrf_token}), 200

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = UserModel.query.filter_by(email=form.email.data).first()
        if existing_user:
            return jsonify({"status": "error", "message": "该邮箱已被注册，请使用其他邮箱。"}), 400

        email = form.email.data
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        user = UserModel(email=email, username=username, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({"status": "success", "message": "注册成功，请登录。"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": "注册失败，请稍后再试。", "error": str(e)}), 500
    else:
        errors = form.errors
        return jsonify({"status": "error", "message": "注册失败，请检查您的输入。", "errors": errors}), 400




@bp.route("/captcha/email")  # 定义 /captcha/email 路由，处理 GET 请求
def get_email_captcha():
    email = request.args.get("email")  # 从请求参数中获取 email 值
    if not email:  # 如果 email 参数为空或不存在，返回错误信息和状态码 400
        return "No email provided", 400
    # string.digits 是一个包含数字字符的字符串，即 '0123456789'。
    source = string.digits * 4  # 创建一个包含 40 个数字字符的字符串
    captcha = random.sample(source, 4)  # 随机选择 4 个字符
    captcha = "".join(captcha)  # 将字符列表连接成字符串，如 '1234'

    try:
        message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
        mail.send(message)  # 发送邮件
    except Exception as e:  # 捕获发送邮件过程中发生的任何异常
        print(e)  # 打印异常信息
        return "邮件发送失败！", 500  # 返回错误信息和状态码 500

    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)  # 创建验证码模型实例
    db.session.add(email_captcha)  # 添加到数据库会话
    db.session.commit()  # 提交会话，保存到数据库

    return jsonify({"code": 200, "message": "", "data": None})  # 返回 JSON 响应，表示成功
@bp.route("/mail/test")  # 定义 /mail/test 路由，处理邮件测试
def mail_test():
    message = Message(subject="邮箱测试", recipients=["1617562300@qq.com"], body="这是一条测试邮件")
    mail.send(message)  # 发送邮件
    return "邮件发送成功！"  # 返回成功信息
