# -*- coding:utf-8 -*-
import pymysql
import configparser
import datetime
import os

def get_item_in_confFile(confFile, section, name):
    conf = configparser.ConfigParser()
    conf.read(confFile, encoding="utf-8")
    return conf.get(section, name)
    

def dbConfig(name):
    path = os.path.dirname(os.path.realpath(__file__))+'/config.ini'
    return get_item_in_confFile(path, "database", name)

def getdb():
    host = dbConfig("host")
    username = dbConfig("username")
    password = dbConfig("password")
    dbname = dbConfig("dbname")
    db = pymysql.connect(host, username, password, dbname)
    return db

def tolist(data):
    a  = []
    for x in data:
        if type(x) == int:
            a.append(str(x))
        elif type(x) == datetime.datetime:
            a.append(x.isoformat())
        elif x == None:
            a.append("")
    return a

def output(db, table, outfile):
    cursor = db.cursor()
    cursor.execute("desc %s" % table)
    colList = []
    while True:
        data = cursor.fetchone()
        if data == None:
            break
        colList.append(data[0])
    print(colList)
    cursor.execute("select * from %s" % table)
    f = open(outfile, "w")
    f.write(",".join(colList)+"\n")
    while True:
        data = cursor.fetchone()
        if data == None:
            break
        f.write(",".join(tolist(data))+"\n")
    f.close()
    db.close()

def main():
    db = getdb()
    cursor = db.cursor()
    cursor.execute("show databases")
    while True:
        data = cursor.fetchone()
        if data == None:
            break
        print(data)
    #output(db, "bk_admission_score", "bk_admission_score.csv")
    

if __name__ == '__main__':
    main()