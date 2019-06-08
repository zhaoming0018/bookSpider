# -*- coding:utf-8
from tools.db import getdb
from functools import wraps
from flask import request, redirect, url_for, session
from pymysql.cursors import DictCursor
import hashlib

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'admin' in session:
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_users(page_num=1, page_size=20):
    db = getdb()
    cursor = db.cursor(DictCursor)
    page_num = int(page_num)
    start = (page_num-1)*page_size
    field_list = ['id', 'username', 'nickname', 'email', 'phone', 'passwd']
    sql = "select %s from user" % ', '.join(field_list)
    sql += " where valid='1'"
    sql += " limit %d, %d" %(start, page_size)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    cursor = db.cursor()
    sql = "select count(*) from user"
    sql += " where valid='1'"
    cursor.execute(sql)
    count = cursor.fetchone()[0]
    return data, count

def get_user_one(id):
    db = getdb()
    cursor = db.cursor()
    fields = ['id', 'username', 'nickname', 'email', 'phone', 'passwd']
    sql = "select %s from user" % ', '.join(fields)
    sql += " where valid='1' limit 1"
    cursor.execute(sql)
    userInfo = cursor.fetchone()
    if userInfo is None:
        return None
    print(userInfo)
    res = dict(zip(fields, userInfo))
    return res

def getBookInfo(id):
    db = getdb()
    cursor = db.cursor(DictCursor)
    sql = "select * from book where id='%s'" % id
    cursor.execute(sql)
    res = cursor.fetchone()
    return res

def getbooks(page_num=1, page_size=20, come_from=None, order=None):
    db = getdb()
    cursor = db.cursor(DictCursor)
    page_num = int(page_num)
    start = (page_num-1)*page_size
    sql = "select id, bookname, link, come_from, author, price, grade from book"
    if come_from is not None:
        sql += " where come_from='%s' "
    sql += " limit %d, %d" %(start, page_size)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    sql = "select count(*) as cnt from book"
    if come_from is not None:
        sql += " where come_from='%s'"
    cursor.execute(sql)
    count = cursor.fetchone()['cnt']
    return data, count

def change_password(passwd):
    m2 = hashlib.md5()
    m2.update(passwd.encode('utf-8'))
    md5_passwd = m2.hexdigest()
    sql = "update manager set passwd='%s'"%md5_passwd
    db = getdb()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def change_valid(cur_passwd, passwd, confirm):
    if cur_passwd == '' or passwd == '' or confirm == '':
        return False
    db = getdb()
    cursor = db.cursor()
    m2 = hashlib.md5()
    m2.update(cur_passwd.encode('utf-8'))
    md5_passwd = m2.hexdigest()
    sql_find_user = "select count(*) from manager where passwd='%s'"% md5_passwd
    print(sql_find_user)
    cursor.execute(sql_find_user)
    res = cursor.fetchone()[0]
    print(res)
    if int(res) == 0:
        return False
    if passwd == confirm:
        return True
    else:
        return False