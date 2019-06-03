# -*- coding:utf-8
from tools.db import getdb
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

db = getdb()
cursor = db.cursor()


def get_driver():
    driver_path = os.path.dirname(os.path.realpath(__file__))+"/chromedriver"
    chrome_options=Options()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('--headless')
    return webdriver.Chrome(driver_path, options=chrome_options)

driver = get_driver()

def get_price(url):
    if driver == None:
        get_driver()
    driver.get(url)
    try:
        price = driver.find_element_by_class_name('mainprice').text
        # print("price", price)
    except:
        price = None
    try:
        price_r = driver.find_element_by_class_name('small-price').text
        # print("price_r", price_r)
    except:
        price_r = None
    return price, price_r

def set_price(price, link, column='price'):
    sql = "update book set "+ column + "='"+ price +"' where link = '" + link + "'" 
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    

def list_to_crawl():
    sql = "select link from book where price is null"
    cursor.execute(sql)
    while True:
        data = cursor.fetchone()
        if data is None:
            break
        # print(data[0])
        price, price_r = get_price(data[0])
        if price == None:
            price = ''
        if price_r == None:
            price_r = ''
        price_json = {'link':data[0], 'price':price, 'price_r':price_r}
        print(price_json)
        # if price is not None:
        #     set_price(price, data[0])
        # if price_r is not None:
        #     set_price(price_r, data[0], column='price_r')

# def list_to_crawl_1():
#     sql = "select link from book where price is null limit 100"
#     cursor.execute(sql)
#     while True:
#         data = cursor.fetchone()
#         if data is None:
#             break
#         print(data[0])
#         price, price_r = get_price(data[0])
#         print(price, price_r)
#         if price is not None:
#             set_price(price, data[0])
#         if price_r is not None:
#             set_price(price_r, data[0], column='price_r')

def main():
    while True:
        list_to_crawl()

if __name__ == '__main__':
    main()