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
