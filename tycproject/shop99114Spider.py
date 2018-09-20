# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem


class Shop99114Spider(scrapy.Spider):
    name = 'shop99114Spider'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        # 'DOWNLOADER_MIDDLEWARES':{
        #     'tycproject.middlewares.RandomUserAgent': 510,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        # },
        'ITEM_PIPELINES':{
            'tycproject.mongodbPipelines.MongodbPipeline_Shop99114':300,
        },

    }


    def start_requests(self):
        url = 'http://shop.99114.com/'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        td_p = html.find_all(class_='td_p')
        for provinceelement in td_p:
            cities=provinceelement.find_all('a')
            for cityelement in cities:
                city=cityelement.string
                cityurl=cityelement['href']
                yield Request(cityurl, callback=self.get_city,meta={'city':city})

    def get_city(self, response):
        city=response.meta['city']
        url=response.url[:-1]
        for i in range(1,100):
            yield Request(url+str(i), callback=self.get_company,meta={'city':city,'number':i})

    def get_company(self, response):
        number=response.meta['number']
        city=response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        cony_div = html.find(class_='cony_div')
        lis=cony_div.find_all('li')
        if lis[0].a:
            for li in lis:
                a=li.find_all('a')
                for companyelement in a:
                    # companyurl=companyelement['href']
                    name=companyelement.b.string
                    companyNameItem = CompanyNameItem()
                    companyNameItem['city'] = city
                    companyNameItem['name'] = name
                    print(name)
                    yield companyNameItem







