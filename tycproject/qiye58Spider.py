# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem
import logging

class Qiye58Spider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    name = 'qiye58Spider'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        # 'DOWNLOADER_MIDDLEWARES':{
        #     'tycproject.middlewares.RandomUserAgent': 510,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        # },
        'ITEM_PIPELINES':{
            'tycproject.mongodbPipelines.MongodbPipeline_Qiye58':300,
        },
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'log/log_qiye58'

    }


    def start_requests(self):
        url = 'https://qy.58.com/citylist/?PGTID=0d211266-0000-0bb4-a9e2-ead8a56242a0&ClickID=1'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        html=BeautifulSoup(response.text,'lxml')
        clist=html.find(id='clist')
        dds=clist.find_all('dd')
        for dd in dds:
            a= dd.find_all('a')
            for cityelement in a:
                cityurl='https:'+cityelement['href']
                city=cityelement.string
                yield Request(cityurl, callback=self.get_city,meta={'city':city})

    def get_city(self,response):
        city = response.meta['city']
        cityurl = response.url
        for i in range(1,1001):
            cityurl_page=cityurl+'pn'+str(i)
            yield Request(cityurl_page, callback=self.get_company, meta={'city': city})

    def get_company(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        compList = html.find(class_='compList')
        spans=compList.find_all('span')
        if spans:
            for span in spans:
                companyurl='https:'+(span.a)['href']
                name=span.a.string
                if name[-2]=='.':
                    yield Request(companyurl, callback=self.get_company_detail, meta={'city': city})
                else:
                    companyNameItem = CompanyNameItem()
                    companyNameItem['city'] = city
                    companyNameItem['name'] = span.a.string
                    print(span.a.string)
                    yield companyNameItem

    def get_company_detail(self,response):
        city = response.meta['city']
        companyNameItem=CompanyNameItem()

        html = BeautifulSoup(response.text, 'lxml')
        name=html.find(class_='businessName fl').string
        companyNameItem['city']=city
        companyNameItem['name'] = name
        yield companyNameItem



