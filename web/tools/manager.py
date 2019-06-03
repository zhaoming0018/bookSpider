# -*- coding:utf-8
from tools.db import getdb

def get_managers():
    db = getdb()
    cursor = db.cursor()
    field_list = ['id', 'username', 'passwd']
    sql = "select %s from manager where valid='true'" % ', '.join(field_list)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
