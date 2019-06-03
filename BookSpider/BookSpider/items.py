# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DangdangItem(scrapy.Item):
    bookname = scrapy.Field()
    link = scrapy.Field()
    come_from = scrapy.Field()
    pic=scrapy.Field()
    author=scrapy.Field()
    publish=scrapy.Field()
    depict=scrapy.Field()
    price=scrapy.Field()
    price_r=scrapy.Field()
    grade = scrapy.Field()
    
class SuningItem(scrapy.Item): 
    bookname = scrapy.Field()
    link = scrapy.Field()
    come_from = scrapy.Field()
    pic=scrapy.Field()
    author=scrapy.Field()
    publish=scrapy.Field()
    depict=scrapy.Field()
    price=scrapy.Field()
    price_r=scrapy.Field()
    grade = scrapy.Field()

class JdItem(scrapy.Item):
    bookname = scrapy.Field()
    link = scrapy.Field()
    come_from = scrapy.Field()
    pic=scrapy.Field()
    author=scrapy.Field()
    publish=scrapy.Field()
    depict=scrapy.Field()
    price=scrapy.Field()
    price_r=scrapy.Field()
    grade = scrapy.Field()