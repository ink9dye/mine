import random
import string
from exts import mail, db
from flask import Blueprint, request, jsonify, session, make_response
from flask_mail import Message
from flask_wtf.csrf import generate_csrf
from models import EmailCaptchaModel, UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    data = request.json
    form = LoginForm(data=data)
    if request.method == "GET":
        msg = request.args.get('msg')
        if msg == '12783':
            csrf_token = generate_csrf()
            return jsonify({"csrf_token": csrf_token}), 200
        else:
            return jsonify({"msg": "请使用POST方法登录", "code": 100}), 200
    else:
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                session["user_id"] = user.id
                return jsonify({"msg": "success", "code": 200}), 200
            else:
                return jsonify({"msg": "error", "code": 300}), 200
        else:
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    errors.append(f"{getattr(form, field).label.text} - {error}")
            return jsonify({"msg": "验证错误", "errors": errors, "code": 400}), 200

@bp.route('/logout')
def logout():
    session.clear()
    response = make_response(jsonify({"message": "注销成功"}))
    response.delete_cookie('session')
    return response

@bp.route("/register", methods=["POST"])
def register():
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

@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    if not email:
        return "未提供邮箱", 400

    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)

    try:
        message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
        mail.send(message)
    except Exception as e:
        print(e)
        return "邮件发送失败！", 500

    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    return jsonify({"code": 200, "message": "", "data": None})

@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["your_email@example.com"], body="这是一条测试邮件")
    mail.send(message)
    return jsonify({"message": "邮件发送成功！", "status": "success", "code": 200}), 200
