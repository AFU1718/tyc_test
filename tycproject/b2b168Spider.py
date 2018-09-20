# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem
import logging


class B2b168Spider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    name = 'b2b168Spider'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        # 'DOWNLOADER_MIDDLEWARES':{
        #     'tycproject.middlewares.RandomUserAgent': 510,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        # },
        'ITEM_PIPELINES':{
                'tycproject.mongodbPipelines.MongodbPipeline_B2b168':300,
        },
        'LOG_LEVEL' : 'DEBUG',
        'LOG_FILE' : 'log/log_b2b168'

    }


    def start_requests(self):
        url = 'https://www.b2b168.com/page-company.html'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        url = 'https://www.b2b168.com'
        html = BeautifulSoup(response.text, 'lxml')
        cmap = html.find(class_='c-map')
        for provinceelement in cmap.find_all('li'):
            provinceurl=url+provinceelement.a['href']
            province=provinceelement.a.string
            yield Request(provinceurl, callback=self.get_city)

    def get_city(self,response):
        url = 'https://www.b2b168.com'
        html = BeautifulSoup(response.text, 'lxml')
        mach_list=html.find(class_='mach_list clearfix')
        dl=mach_list.find_all('dl')
        for cityelement in dl:
            dt=cityelement.find('dt')
            city=dt.a.string[:-2]
            countyelement =cityelement.find('dd')

            countyurl=url+countyelement.a['href']
            yield Request(countyurl, callback=self.get_company, meta={'city': city})

    def get_company(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        page=int(html.find(class_='pages').text.replace(' ', '').split('共')[1].split('页')[0])

        if (not page) or page == 0:
            page = 0
        for i in range(1,page+1):
            yield Request(response.url+'l-'+str(i)+'.html', callback=self.get_company_detail, meta={'city': city})

    def get_company_detail(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        list=html.find(class_='list-right').find(class_='list')
        for li in list.find_all('li'):
            companyelement=li.find(class_='biaoti')
            name=companyelement.a.string
            companyNameItem = CompanyNameItem()
            companyNameItem['city'] = city
            companyNameItem['name'] = name
            yield companyNameItem

