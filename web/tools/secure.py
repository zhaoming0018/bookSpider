#-*- coding:utf-8
from tools.db import getdb
import hashlib

def login_valid(username, passwd):
    db = getdb()
    cursor = db.cursor()
    m2 = hashlib.md5()
    m2.update(passwd.encode('utf-8'))
    md5_passwd = m2.hexdigest()
    sql_find_user = "select count(*) from manager where username='%s' and passwd='%s'"%(username, md5_passwd)
    print(sql_find_user)
    cursor.execute(sql_find_user)
    res = cursor.fetchone()[0]
    print(res)
    if int(res) == 1:
        return True
    else:
        return False