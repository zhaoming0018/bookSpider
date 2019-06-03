# -*- coding: utf-8 -*-

from tools.db import getdb

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookspiderPipeline(object):

    def runSql(self, sql):
        print(sql)
        db = getdb()
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        cursor.close()
        db.close()

    def getFields(self):
        return ['bookname', 'link', 'come_from', 'pic', 'author',
                 'publish', 'depict', 'price', 'price_r', 'grade']
    
    def insertItem(self, item):
        fields = self.getFields()
        tmp_fields = fields.copy()
        for field in tmp_fields:
            if item[field] is None:
                fields.remove(field)
        sql = "insert into book("+ ', '.join(fields)+") values("
        if item['price'] is not None:
            item['price'] = item['price'][1:]
        if item['price_r'] is not None:
            item['price_r'] = item['price_r'][1:]
        while not item['grade'].isdigit():
            item['grade'] = item['grade'][:-1]
        item['grade'] = int(item['grade'])
        values = map(lambda x : '"'+str(item[x])+'"' if item[x]!= None else '""', fields)
        sql += ', '.join(values) + ")"
        self.runSql(sql)
        
    def process_item(self, item, spider):
        self.insertItem(item)
        
  