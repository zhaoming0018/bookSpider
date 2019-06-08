# -*- coding:utf-8
from tools.db import getdb
from functools import wraps
from flask import request, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session:
            return redirect(url_for('search.login'))
        return f(*args, **kwargs)
    return decorated_function

def check_register(request):
    username = request.form.get('username', '')
    nickname = request.form.get('nickname', '')
    passwd = request.form.get('passwd', '')
    confirm = request.form.get('confirm', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    error = {}
    if username == '':
        error['username'] = '用户名不能为空'
    if nickname == '':
        error['nickname'] = '请输入昵称'
    if passwd == '':
        error['passwd'] = '密码不能为空'
    if confirm != passwd:
        error['confirm'] = '确认密码与输入密码不相同'
    if email == '':
        error['email'] = '请输入电子邮件'
    if phone == '':
        error['phone'] = '请输入手机号码'
    return error

def do_register(request):
    fields = ['username', 'nickname', 'passwd', 'email', 'phone']
    keys = ', '.join(fields)
    values = ','.join(map(lambda x: '"%s"'%request.form.get(x,''), fields))
    sql = "insert into user(%s) values (%s)"%(keys, values)
    print(sql)
    db = getdb()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        return False

def login_valid(username, passwd):
    db = getdb()
    cursor = db.cursor()
    sql_find_user = "select count(*) from user where username='%s' and passwd='%s' and valid=1"%(username, passwd)
    print(sql_find_user)
    cursor.execute(sql_find_user)
    res = cursor.fetchone()[0]
    print(res)
    if int(res) != 0:
        return True
    else:
        return False