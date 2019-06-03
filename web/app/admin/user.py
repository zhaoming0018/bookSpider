from flask import request, redirect, render_template
from flask_paginate import Pagination
from app.admin.tool import get_user_one, get_users, login_required
from app.admin.blue import admin
from tools.db import getdb
from tools.user import User

@admin.route('/user/show')
@login_required
def user_show():
    id = request.args.get('id',None)
    if id is None:
        return redirect('/admin/user/list')
    userInfo = get_user_one(id)
    if userInfo is None:
        return redirect('/admin/user/list')
    return render_template('admin/user_view.html', userInfo=userInfo, func="user")

@admin.route('/user/modify', methods=['POST'])
@login_required
def user_modify():
    id = request.args.get('id', None)
    if id is None:
        return redirect('/admin/user/list')
    user = User()
    if user.modify(id, request.form):
        return redirect('/admin/user/list')
    else:
        return redirect('/admin/user/show?id='+str(id))

@admin.route('/user/delete')
@login_required
def user_delete():
    id = request.args.get('id', None)
    if id is None:
        return redirect('/admin/user/list')
    db = getdb()
    cursor = db.cursor()
    sql = "update user set valid='0' where id = '%s'" %id
    cursor.execute(sql)
    db.commit()
    return render_template('admin/user_delete.html')

@admin.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    if request.method == "POST":
        user = User()
        user.addUser(request.form)
        return redirect('/admin/user/list/')
    return render_template('admin/user_add.html', func='user')

@admin.route('/user/list/')
@login_required
def list_user():
    page = int(request.args.get('page', 1))
    data, count = get_users(page_num=page)  
    page_obj = Pagination(page=page, total=int(count)//20, per_page_count=20, bs_version='3')
    html = page_obj.links
    return render_template('admin/userList.html', data=data, pageinfo=html, func="user")