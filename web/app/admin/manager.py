from flask import request, render_template, make_response, redirect, flash, session
from tools.secure import login_valid
from tools.db import getdb
from app.admin.tool import login_required, getbooks, change_password, change_valid

from app.admin.blue import admin

@admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if login_valid(request.form['username'], request.form['passwd']):   
            resp = make_response(render_template( 'admin/login_redirect.html' ))
            session['admin'] = request.form['username']
            return resp
    return render_template('admin/login.html')

@admin.route('/index/')
@login_required
def admin_index():
    books, _ = getbooks()
    return render_template('admin/index.html', books=books, func="overview")

@admin.route('/manager/change', methods=['GET', 'POST'])
@login_required
def change():
    if request.method == 'GET':
        return render_template('admin/change.html', func='admin')
    cur_passwd = request.form.get('cur_passwd', '')
    passwd = request.form.get('passwd', '')
    confirm = request.form.get('confirm', '')
    print(cur_passwd, passwd, confirm)
    if change_valid(cur_passwd, passwd, confirm):
        change_password(passwd)
        return render_template('admin/change_redirect.html', func='admin', message="修改成功")
    else:
        return render_template('admin/change.html', func='admin', message="修改失败")

@admin.route('/logout', methods=['GET', 'POST'])
def admin_logout():
    session.pop('admin', None)
    return render_template('admin/logout_redirect.html')

