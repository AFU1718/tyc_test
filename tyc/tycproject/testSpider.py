# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
# from tycproject.items import CompanyNameItem


class TestSpider(scrapy.Spider):
    name = 'TestSpider'
    allowed_domains = ['qy.58.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'DOWNLOADER_MIDDLEWARES':{
            'tycproject.middlewares.RandomUserAgent': 510,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        },
        # 'ITEM_PIPELINES':{
        #     'tycproject.mongodbPipelines.MongodbPipeline':1,
        # }
    }


    def start_requests(self):
        url = 'https://qy.58.com/cd/pn39'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        compList = html.find(class_='compList')
        spans = compList.find_all('span')
        if not spans:
            print('kkkkkkkkkkkkkkkkkkk')
