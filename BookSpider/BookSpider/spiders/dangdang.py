# -*- coding: utf-8 -*-
import scrapy
from items import DangdangItem

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/']

    # 解析侧边栏所有包含“category.”的链接
    def parse(self, response):
        href_list = response.xpath('//dl[@class="inner_dl"]/dd/a/@href').extract()
        # print(href_list)
        for href in href_list:
            if 'category.' in href:
                yield scrapy.Request(response.urljoin(href), callback=self.parse_book_list)
    
    # （1） 解析下一页的链接
    # （2） 解析商品链接
    def parse_book_list(self,response):  
        # 下一页
        next_list = response.xpath('//li[@class="next"]/a/@href').extract()
        for next_page in next_list:
            print(len(next_list), next_page)
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_book_list)
        # 商品链接
        li_list = response.xpath('//ul[@class="bigimg"]/li')
        for li in li_list:
            item = DangdangItem()
            item["bookname"]=li.xpath('./p[@class="name"]/a/text()').extract_first()
            item["link"]=li.xpath('./p[@class="name"]/a/@href').extract_first()
            item["come_from"] = "dangdang"
            item["pic"] = li.xpath('.//img/@data-original').extract_first()
            item["author"]=li.xpath('./p[@class="search_book_author"]/span[1]/a/text()').extract_first()
            item["publish"]=li.xpath('./p[@class="search_book_author"]/span[3]/a/text()').extract_first()
            item["depict"]=li.xpath('./p[@class="detail"]/text()').extract_first()
            item["price"]=li.xpath('.//span[@class="search_now_price"]/text()').extract_first()
            item["price_r"]=li.xpath('.//span[@class="search_pre_price"]/text()').extract_first()
            item["grade"]=li.xpath('./p[@class="search_star_line"]/a/text()').extract_first()
            # print(item)
            yield item
    
    # def parse_book_detail(self,response):
    #     item=response.meta["item"]
    #     li_list=response.xpath('//ul[@class="bigimg"]/li')    
    #     for li in li_list :
    #         item["name"]=li.xpath('./p[@class="name"]/a/text()').extract_first()
    #         item["link"]=li.xpath('./p[@class="name"]/a/@href').extract_first()
    #         item["author"]=li.xpath('./p[@class="search_book_author"]/span[1]/a/text()').extract_first()
    #         item["time"]=li.xpath('./p[@class="search_book_author"]/span[2]/text()').extract_first()
    #         item["publish"]=li.xpath('./p[@class="search_book_author"]/span[3]/a/text()').extract_first()
    #         item["dec"]=li.xpath('./p[@class="detail"]/text()').extract_first()
    #         item["price"]=li.xpath('./p[@class="price"]/span[2]/text()').extract_first()
    #         item["price_r"]=li.xpath('./p[@class="price"]/span[1]/text()').extract_first()
    #         item["rank"]=li.xpath('./p[@class="search_star_line"]/a/text()').extract_first()
    #         yield item
           
            
    #     next_url=response.xpath('//div[@class="paging"]/ul/li[@class="next"]/a/@href').extract_first()
    #     if next_url is not None :
    #         next_url = "http://category.dangdang.com"+ next_url
    #         yield scrapy.Request(
    #             next_url,
    #             callback=self.parse_book_detail,
    #             meta={"item":item}
    #             )
            
            
            
            
            
            
            
            
            
            