from tools.db import getdb
from pymysql.cursors import DictCursor
from models.Model import Model

class BookModel(Model):
    
    def __init__(self):
        Model.__init__(self, 'book')

    # 读取一页book的数据
    def find(self, page_num=1, page_size=20, condition=None):
        def clause(x):
            if x == 'bookname' or x=='author':
                return x+" like '%"+ str(condition[x]) +"%'"
            else:
                return x+"='"+str(condition[x])+"'"
        sql = "select * from " + self.tableName
        # where 子句
        if condition is None:
            condition = {}
        condition['valid'] = 1
        order = None
        if 'order' in condition:
            order = condition['order']
            del condition['order']
        print(condition)
        where_clause = " and ".join(map(clause, condition))
        sql += " where " + where_clause
        print(sql)
        order_clause = ""
        if order is not None:
            if order == '1':
                order_clause = "order by price"
            elif order == '2':
                order_clause = "order by price desc"
            elif order == '3':
                order_clause = "order by grade"
            elif order == '4':
                order_clause = "order by grade desc"
        sql += order_clause     
        print(sql)
        # 页
        page_num = int(page_num)
        start = (page_num-1)*page_size
        sql += " limit %d, %d" %(start, page_size)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        sql = "select count(*) as cnt from book"
        sql += " where "+where_clause
        print(sql)
        self.cursor.execute(sql)
        count = self.cursor.fetchone()['cnt']
        # print(data)
        return data, count
    
    # 根据id删除一本书
    def delete(self, id):
        sql = "update book set valid=0 where id='%d'" % int(id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.cursor.close()
            self.db.close()
            return 1
        except:
            self.db.rollback()
            self.cursor.close()
            self.db.close()
            return 0
    
    def getInfo(self, id):
        sql = "select * from book where id='%s'" % id
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res