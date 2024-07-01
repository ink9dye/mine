from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import Email, Length, EqualTo, InputRequired, ValidationError

from models import UserModel


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(message="邮箱格式错误！"),
        InputRequired(message="邮箱不能为空！")
    ])
    captcha = StringField('Captcha', validators=[
        Length(min=4, max=4, message="验证码格式错误！"),
        InputRequired(message="验证码不能为空！")
    ])
    username = StringField('Username', validators=[
        Length(min=1, max=20, message="用户名格式错误！"),
        InputRequired(message="用户名不能为空！")
    ])
    password = PasswordField('Password', validators=[
        Length(min=4, max=20, message="密码格式错误！"),
        InputRequired(message="密码不能为空！")
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        EqualTo('password', message="两次密码不一致"),
        InputRequired(message="确认密码不能为空！")
    ])

    # 自定义验证方法保持不变
    def validate_username(self, field):
        if UserModel.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已被占用，请选择其他用户名。")


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Email(), InputRequired()])
    password = PasswordField('密码', validators=[InputRequired()])
    remember = BooleanField('记住密码')
    autologin = BooleanField('自动登录')


class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=1), InputRequired()])
    content = StringField('Content', validators=[Length(min=1), InputRequired()])


class AnswerForm(FlaskForm):
    question_id = IntegerField('Question ID', validators=[InputRequired()])
    content = StringField('Content', validators=[Length(min=1), InputRequired()])
