from functools import wraps  # 导入wraps函数，用于保留被装饰函数的元信息

from flask import g, redirect, url_for  # 导入Flask的g全局对象、重定向和URL生成函数


# 定义login_required装饰器
def login_required(func):
    @wraps(func)  # 使用wraps装饰器来保留func的原始信息，如名称、文档字符串等
    def inner(*args, **kwargs):  # 定义一个内部函数inner，它将接收任意数量的位置参数和关键字参数
        if g.user:  # 检查g对象是否有user属性，g.user在用户登录成功时设置
            return func(*args, **kwargs)  # 如果用户已登录，调用原始函数func并传递所有参数
        else:
            return redirect(url_for("auth.login"))  # 如果用户未登录，重定向到登录页面

    return inner  # 返回装饰过的函数
