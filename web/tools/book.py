# -*- coding:utf-8 
from tools.db import getdb
from pymysql.cursors import DictCursor

def getbooks(page_num=1, page_size=20, come_from=None, order=None):
    db = getdb()
    cursor = db.cursor(DictCursor)
    page_num = int(page_num)
    start = (page_num-1)*page_size
    sql = "select id, name, link, pic, come_from, author, price, grade, description from book where valid=1"
    if come_from is not None:
        sql += " where come_from='%s' "
    sql += " limit %d, %d" %(start, page_size)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    sql = "select count(*) as cnt from book where valid=1"
    if come_from is not None:
        sql += " where come_from='%s'"
    cursor.execute(sql)
    count = cursor.fetchone()['cnt']
    return data, count

def book_delete(id):
    id = int(id)
    db = getdb()
    cursor = db.cursor()
    sql = "update book set valid=0 where id='%d'" % int(id)
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return 1
    except:
        db.rollback()
        cursor.close()
        db.close()
        return 0
    