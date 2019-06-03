from tools.db import getdb
from pymysql.cursors import DictCursor

class User():

    def __init__(self):
        self.db = getdb()
        self.cursor = self.db.cursor(DictCursor)
    
    def getUser(self, id):
        pass
    
    def getUserByName(self, name):
        sql = "select * from user where username='%s' limit 1" % name
        self.cursor.execute(sql)
        userInfo = self.cursor.fetchone()
        print(userInfo)
        return userInfo

    def addUser(self, userOne: dict):
        fields = ['username', 'nickname', 'passwd', 'email', 'phone']
        keys = ', '.join(fields)
        values = ','.join(map(lambda x: '"%s"'%userOne.get(x,''), fields))
        sql = "insert into user(%s) values (%s)"%(keys, values)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
            return True
        except:
            self.db.rollback()
            self.db.close()
            return False
        
    def modify(self, id, userOne:dict):
        fields = ['username', 'nickname', 'passwd', 'email', 'phone']
        values = ','.join(map(lambda x: '%s = "%s"'%(x,userOne.get(x,'')), fields))
        sql = "update user set %s where id='%d'"%(values, int(id))
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
            return True
        except:
            self.db.rollback()
            self.db.close()
            return False