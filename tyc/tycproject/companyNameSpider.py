# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem


class CompanynamespiderSpider(scrapy.Spider):
    name = 'companyNameSpider'
    allowed_domains = ['qy.58.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'DOWNLOADER_MIDDLEWARES':{
            'tycproject.middlewares.RandomUserAgent': 510,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        },
        'ITEM_PIPELINES':{
            'tycproject.mongodbPipelines.MongodbPipeline':1,
        }
    }


    def start_requests(self):
        url = 'https://qy.58.com/citylist/?PGTID=0d211266-0000-0bb4-a9e2-ead8a56242a0&ClickID=1'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        html=BeautifulSoup(response.text,'lxml')
        clist=html.find(id='clist')
        dds=clist.find_all('dd')
        count=0
        for dd in dds:
            a= dd.find_all('a')
            for cityelement in a:
                count = count + 1
                if (count<=1):
                    cityurl='https:'+cityelement['href']
                    city=cityelement.string
                    yield Request(cityurl, callback=self.get_city,meta={'city':city,'cityurl':cityurl})

    def get_city(self,response):
        city = response.meta['city']
        cityurl = response.meta['cityurl']
        for i in range(1,100):
            cityurl_page=cityurl+'pn'+str(i)
            yield Request(cityurl_page, callback=self.get_company, meta={'city': city,})

    def get_company(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        compList = html.find(class_='compList')
        spans=compList.find_all('span')
        if spans:
            for span in spans:
                companyurl='https:'+(span.a)['href']
                yield Request(companyurl, callback=self.get_company_detail, meta={'city': city, })

    def get_company_detail(self,response):
        companyNameItem=CompanyNameItem()
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        name=html.find(class_='businessName fl').string
        companyNameItem['city']=city
        companyNameItem['name'] = name
        return companyNameItem



