# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem
import logging

class Qiye56yeSpider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    name = 'qiye56yeSpider'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        # 'DOWNLOADER_MIDDLEWARES':{
        #     'tycproject.middlewares.RandomUserAgent': 510,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        # },
        'ITEM_PIPELINES':{
                'tycproject.mongodbPipelines.MongodbPipeline_Qiye56ye':300,
        },
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'log/log_qiye56ye'

    }


    def start_requests(self):
        url = 'http://qiye.56ye.net/'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        category_qye = html.find(class_='category_qye')
        for provinceelement in category_qye.find_all('td'):
            provinceurl=provinceelement.a['href']
            province=provinceelement.a.string
            yield Request(provinceurl, callback=self.get_company, meta={'city': province})


    def get_company(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        pages=html.find(class_='pages')
        if pages:
            page=int(pages.cite.string[:-1].split('/')[1])
        else:
            page=1
        for i in range(1,page+1):
            url=response.url[:-5]
            yield Request(url+'-page-'+str(i)+'.html', callback=self.get_company_detail, meta={'city': city})


    def get_company_detail(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        list=html.find_all(class_='list')
        for companyelement in list:
            name=companyelement.find(class_='sup-name').a.string
            companyNameItem = CompanyNameItem()
            companyNameItem['city'] = city
            companyNameItem['name'] = name
            yield companyNameItem

