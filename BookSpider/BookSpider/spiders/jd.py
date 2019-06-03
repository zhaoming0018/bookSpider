# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
import os, time
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
from BookSpider.items import JdItem

'''
    获取一个基于chromedriver的selenuim实例
'''
def get_driver():
    driver_path = "./chromedriver"
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    return webdriver.Chrome(driver_path, options=chrome_options)

'''
    为了方便，封装起selenuim环境下指定url中的基于class的查找
'''
def get_elemenets_by_class(url, classname):
    driver = get_driver()
    driver.get(url)
    time.sleep(2)
    book_nav = driver.find_elements_by_class_name(classname)
    return book_nav

def get_property(ele):
    x = ""
    if len(ele) != 0:
        x = ele[0].text
    return x

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://book.jd.com/']
    
    # '''
    #     由于目录较为复杂，所以用selenium爬取导航栏的链接；
    #     导航栏的链接目标形式不同，故仅爬取包含"list.jd"的链接
    # '''
    def parse(self, response):
        items = get_elemenets_by_class(response.url, "book_nav_sub_main")
        hrefs = []
        for item in items:
            links = item.find_elements_by_tag_name('a')
            for link in links:
                href = link.get_attribute('href')
                if 'list.jd' in href:
                    hrefs.append(href)
        
        for href in hrefs:
            yield scrapy.Request(href,callback=self.parse_book_list)
    
    # '''
    #     为了简化操作，这一步仅获取下一页和商品页的链接
    #     这一步不需要selenium，也可以提升点速度
    # '''
    def parse_book_list(self, response):
        next_url = response.xpath('//a[@class="pn-next"]/@href').extract()
        if len(next_url) != 0:
            next_url = urljoin(response.url, next_url[0])
            # print(next_url)
            yield scrapy.Request(next_url,callback=self.parse_book_list)
        items = response.xpath('//li[@class="gl-item"]//a/@href').extract()
        if len(items) != 0:
            for item in items:
                if 'item.jd' in item:
                    item_link = urljoin(response.url, item)
                    yield scrapy.Request(item_link,callback=self.parse_book_item)
        
    # '''
    #     解析书的界面，可能会有一些奇怪的链接，
    #     故在无法寻找到name属性时退出解析
    # '''
    def parse_book_item(self, response):
        item = JdItem()
        item['come_from'] = 'jd'
        item['link'] = response.url
        driver = get_driver()
        driver.get(response.url)
        time.sleep(1)
        name = driver.find_elements_by_xpath('//div[@id="name"]/div[@class="sku-name"]')
        item['bookname'] = get_property(name)
        if item['bookname'] == '':
            driver.quit()
            return
        shop_div = driver.find_elements_by_xpath('//div[@class="item"]/div[@class="name"]/a')
        item['publish'] = get_property(shop_div)
        pic = driver.find_elements_by_xpath('//div[@id="spec-n1"]/img')
        item['pic'] = ""
        if len(pic) != 0:
            item['pic'] = pic[0].get_attribute('src')
        description = driver.find_elements_by_id('p-ad')
        item['depict'] = get_property(description)
        author = driver.find_elements_by_id('p-author')
        item['author'] = get_property(author)
        rank = driver.find_elements_by_xpath('//div[@id="comment-count"]/a')
        item['grade'] = get_property(rank)
        price = driver.find_elements_by_id('jd-price')
        item['price'] = get_property(price)
        price_r = driver.find_elements_by_id('page_maprice')
        item['price_r'] = get_property(price_r)
        driver.quit()
        print(item)
        yield item
        