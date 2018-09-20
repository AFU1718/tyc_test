# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem
import logging

class Huangye88Spider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    name = 'huangye88Spider'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        # 'DOWNLOADER_MIDDLEWARES':{
        #     'tycproject.middlewares.RandomUserAgent': 510,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        # },
        'ITEM_PIPELINES':{
                'tycproject.mongodbPipelines.MongodbPipeline_Huangye88':300,
        },
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'log/log_huangye88'

    }


    def start_requests(self):
        url = 'http://b2b.huangye88.com/region/'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        clist = html.find(id='clist')
        for dd in clist.find_all('dd'):
            cityelement=dd.find_all('a')
            for detail in cityelement:
                cityurl=detail['href']
                city=detail.string
                yield Request(cityurl, callback=self.get_industry, meta={'city': city})

    def get_industry(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        for tag_tx in html.find_all(class_='tag_tx'):
            for industryelement in tag_tx.find_all('li'):
                industryurl=industryelement.a['href']
                industry=industryelement.a.string
                yield Request(industryurl, callback=self.get_company, meta={'city': city})

    def get_company(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        number=int(html.find(class_='tit tit2').find('span').em.string)
        if (not number) or number==0:
            page=0
        else:
            if (number % 20) == 0:
                page = number // 20
            else:
                page = number // 20 + 1
        for i in range(1,page+1):
            yield Request(response.url+'pn'+str(i), callback=self.get_company_detail, meta={'city': city})

    def get_company_detail(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        for companyelement in html.find_all('h4'):
            name=companyelement.a.string
            companyNameItem = CompanyNameItem()
            companyNameItem['city'] = city
            companyNameItem['name'] = name
            yield companyNameItem




