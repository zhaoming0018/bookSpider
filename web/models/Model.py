from tools.db import getdb
from pymysql.cursors import DictCursor

class Model():
    
    def __init__(self, tableName):
        self.db = getdb()
        self.cursor = self.db.cursor(DictCursor)
        self.tableName = tableName
    
    def add(self, one:dict):
        keys = ', '.join(one.keys())
        values = ','.join(map(lambda x: '"%s"'%one.get(x,''), one.keys()))
        sql = "insert into %s(%s) values (%s)"%(self.tableName, keys, values)
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

    def update(self, bookId, one:dict):
        values = ','.join(map(lambda x: '%s = "%s"'%(x,one.get(x,'')), one.keys()))
        sql = "update %s set %s where id='%d'"%(self.tableName, values, int(bookId))
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