# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from BookSpider.items import SuningItem
from scrapy.http import Request
import re, time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    driver_path = "./chromedriver"
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    return webdriver.Chrome(driver_path, options=chrome_options)


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/?safp=d488778a.homepage1.99345513004.47']
    #User-Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

    driver = None

    def parse(self, response):
        links=response.xpath('//div[@class="submenu-left"]/ul/li/a/@href').extract()
        for link in links:
            item={}
            item["come_from"]="suning"
            if link is not None:
                # print(link)
                yield scrapy.Request(
                    link,
                    callback=self.parse_book_list,
                    meta={"item":item.copy()}
                    )

    def parse_book_list(self,response):
        item=response.meta["item"]
        other_pages = response.xpath('//div[@id="bottom_pager"]//a/@href').extract()
        if other_pages is not None:
            for page in other_pages:
                yield scrapy.Request(
                        urljoin(response.url, page),
                        callback=self.parse_book_list,
                        meta={"item":item.copy()}
                    )
        #图书列表页文组
        li_list=response.xpath('//ul[@class="clearfix"]/li')
        for li in li_list:
            item["link"]="http:"+li.xpath('.//a[@class="sellPoint"]/@href').extract_first()
            item["pic"]=li.xpath('.//a[@class="sellPoint"]/img/@src').extract_first()
            if item['pic'] is None:
                item["pic"]=li.xpath('.//a[@class="sellPoint"]/img/@src2').extract_first()
            item['pic']="http:"+item['pic']
            item["grade"]=li.xpath('.//div[@class="res-info"]/p[@class="com-cnt"]/a[@class="num"]/text()').extract_first()
            if item["link"] is not None:
                print(item)
                yield scrapy.Request(
                    item["link"],
                    callback=self.parse_book_detail,
                    meta={"item":item.copy()}
                )
    
   

    def get_price(self,url):
        driver = get_driver()
        driver.get(url)
        time.sleep(1)
        price_ele = driver.find_elements_by_class_name('mainprice')
        price_rele = driver.find_elements_by_class_name('small-price')
        price = None
        if len(price_ele) > 0:
            price = price_ele[0].text
        price_r = None
        if len(price_rele) > 0:
            price_r = price_rele[0].text
        return price, price_r

    def parse_book_detail(self,response):
        item=response.meta["item"]
        li=response.xpath('//div[@class="proinfo-main"]')[0]
        item["bookname"]=li.xpath('//h1[@id="itemDisplayName"]/text()').extract_first()
        item["author"]=li.xpath('.//ul[@class="bk-publish clearfix"]/li[1]/text()').extract_first()
        item["publish"]=li.xpath('.//ul[@class="bk-publish clearfix"]/li[2]/text()').extract_first()
        item["price"], item["price_r"]=self.get_price(response.url)
        item["depict"] = None
        for k in item:
            if type(item[k])==str:
                item[k] = item[k].replace(' ','')
                item[k] = item[k].replace('\n','')
                item[k] = item[k].replace('\t','')
                item[k] = item[k].replace('\r','')
        suningItem = SuningItem(item)
        print("item:",item)
        yield suningItem