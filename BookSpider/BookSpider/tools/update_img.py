# -*- coding:utf-8
from tools.db import getdb
import json, time

def set_image(pic, link):
    sql = "update book set pic='%s' where link = '%s' " % (pic, link) 
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


db = getdb()
cursor = db.cursor()
f = open('img.txt', 'r')
cnt = 0
start = time.time()
while True:
    line = f.readline()
    if line is None or line == '':
        break
    line = line.replace("'",'"').replace(': None',': ""')
    x = json.loads(line)
    # print(x['image'], x['link'])
    set_image(x['image'], x['link'])
    cnt = cnt + 1
    if cnt % 1000 == 0:
        end = time.time()
        print("Step:", cnt, "time:", end-start, "s")
f.close()
cursor.close()
db.close()
