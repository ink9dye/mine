from flask import Blueprint, request, render_template, g, redirect, url_for, flash

from decorators import login_required
from exts import db
from models import QuestionModel, AnswerModel
from .forms import QuestionForm, AnswerForm

# 移除蓝图的URL前缀设置
bp = Blueprint("qa", __name__)


# 首页路由，不添加'qa'前缀
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()  # 倒序，最新的在上面
    return render_template("index.html", questions=questions)


# 发布问答路由，手动添加'qa'前缀
@bp.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_question():
    # 对于GET请求，应该实例化QuestionForm，而不是AnswerForm
    form = QuestionForm()  # 正确实例化表单
    if request.method == 'POST':
        # 注意，这里不需要重新实例化form，因为我们已经在函数开始处实例化了
        if form.validate_on_submit():  # 这里改为使用 validate_on_submit() 更加适合 Flask-WTF 的使用方式
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author_id=g.user.id)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for("qa.index"))
        else:
            # 如果表单验证失败，将会重新渲染页面并显示错误
            print(form.errors)
    # 对于GET请求或表单验证失败的情况，都将执行下面的代码渲染模板
    return render_template("public_question.html", form=form)


# 问答详情路由，不需要登录
@bp.route("/qa/detail/<int:qa_id>", methods=['GET'])
def qa_detail(qa_id):
    # 根据传入的问题ID从数据库中查找对应的问题，如果找不到则返回404错误
    question = QuestionModel.query.get_or_404(qa_id)
    # 创建一个AnswerForm实例，用于在详情页面上渲染回答提交表单
    form = AnswerForm()
    # 使用渲染的模板、问题实例和表单实例作为上下文，渲染问题详情页面
    return render_template("detail.html", question=question, form=form)


# 发布回答路由，需要用户登录
@bp.route("/answer/public", methods=['POST'])
@login_required
def public_answer():
    # 创建AnswerForm实例，使用请求的表单数据初始化
    form = AnswerForm(request.form)
    # 验证表单数据。注意：这里使用validate_on_submit()可能是一个错误，因为它是FlaskForm的方法，而不是WTForms的Form，除非AnswerForm确实继承自FlaskForm
    if form.validate_on_submit():  # 如果表单数据验证通过
        # 创建一个新的AnswerModel实例，使用表单提交的数据
        new_answer = AnswerModel(content=form.content.data, question_id=form.question_id.data, author_id=g.user.id)
        # 将新回答添加到数据库会话并提交以保存到数据库
        db.session.add(new_answer)
        db.session.commit()
        # 显示成功提交的闪现消息
        flash('回答已成功提交。', 'success')
        # 重定向到问题详情页面，以便用户可以看到他们的新回答
        return redirect(url_for('qa.qa_detail', qa_id=form.question_id.data))
    else:  # 如果表单数据验证未通过
        # 遍历所有表单字段的错误消息，并为每个错误显示一个闪现消息
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}", 'error')
        # 重定向回问题详情页面，允许用户修正并重新提交表单
        return redirect(url_for('qa.qa_detail', qa_id=form.question_id.data))


@bp.route("/search")
def search():
    # 从请求的查询参数中获取搜索关键词
    q = request.args.get("q")
    # 在数据库中搜索包含关键词的所有问题
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    # 使用搜索结果渲染首页模板，并显示搜索到的问题
    return render_template("index.html", questions=questions)


@bp.route("/my-questions")
@login_required
def my_questions():
    if g.user:
        user_id = g.user.id
        # 查询当前登录用户的所有问题
        questions = QuestionModel.query.filter_by(author_id=user_id).order_by(QuestionModel.create_time.desc()).all()
        # 使用与首页相同的模板渲染用户的问题
        return render_template("index.html", questions=questions)
    else:
        # 如果用户未登录，重定向到登录页面
        flash('请先登录再查看您的问答。', 'warning')
        return redirect(url_for('auth.login'))
