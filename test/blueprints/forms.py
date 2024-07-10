from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import Email, Length, EqualTo, InputRequired, ValidationError

# 从 models 模块中导入 UserModel，用于自定义验证逻辑
from models import UserModel


# 注册表单类
class RegisterForm(FlaskForm):
    # class Meta:
    #     csrf = False  # 禁用 CSRF
    # 邮箱字段，验证器包括邮箱格式和输入不能为空
    email = StringField('Email', validators=[
        Email(message="邮箱格式错误！"),  # 验证邮箱格式
        InputRequired(message="邮箱不能为空！")  # 验证输入是否为空
    ])

    # 验证码字段，验证器包括长度和输入不能为空
    captcha = StringField('Captcha', validators=[
        Length(min=4, max=4, message="验证码格式错误！"),  # 验证长度为4
        InputRequired(message="验证码不能为空！")  # 验证输入是否为空
    ])

    # 用户名字段，验证器包括长度和输入不能为空
    username = StringField('Username', validators=[
        Length(min=1, max=20, message="用户名格式错误！"),  # 验证长度在1到20之间
        InputRequired(message="用户名不能为空！")  # 验证输入是否为空
    ])

    # 密码字段，验证器包括长度和输入不能为空
    password = PasswordField('Password', validators=[
        Length(min=4, max=20, message="密码格式错误！"),  # 验证长度在4到20之间
        InputRequired(message="密码不能为空！")  # 验证输入是否为空
    ])

    # 确认密码字段，验证器包括与密码字段相等和输入不能为空
    password_confirm = PasswordField('Confirm Password', validators=[
        EqualTo('password', message="两次密码不一致"),  # 验证是否与密码字段相等
        InputRequired(message="确认密码不能为空！")  # 验证输入是否为空
    ])

    # 自定义验证方法，用于检查用户名是否唯一
    def validate_username(self, field):
        if UserModel.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已被占用，请选择其他用户名。")


# 登录表单类
class LoginForm(FlaskForm):
    # class Meta:
    #     csrf = False  # 禁用 CSRF
    # 邮箱字段，验证器包括邮箱格式和输入不能为空
    email = StringField('邮箱', validators=[Email(), InputRequired()])

    # 密码字段，验证器包括输入不能为空
    password = PasswordField('密码', validators=[InputRequired()])

    # 记住密码字段，布尔类型，无需验证器
    remember = BooleanField('记住密码')

    # 自动登录字段，布尔类型，无需验证器
    autologin = BooleanField('自动登录')


# 问题表单类
class QuestionForm(FlaskForm):
    # class Meta:
    #     csrf = False  # 禁用 CSRF
    # 标题字段，验证器包括长度最小为1和输入不能为空
    title = StringField('Title', validators=[Length(min=1), InputRequired()])

    # 内容字段，验证器包括长度最小为1和输入不能为空
    content = StringField('Content', validators=[Length(min=1), InputRequired()])


# 回答表单类
class AnswerForm(FlaskForm):
    # class Meta:
    #     csrf = False  # 禁用 CSRF
    # 问题ID字段，整数类型，验证器包括输入不能为空
    question_id = IntegerField('Question ID', validators=[InputRequired()])

    # 内容字段，验证器包括长度最小为1和输入不能为空
    content = StringField('Content', validators=[Length(min=1), InputRequired()])
