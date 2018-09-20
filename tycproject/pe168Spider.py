# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem
import logging

class YouboySpider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    name = 'pe168Spider'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        # 'DOWNLOADER_MIDDLEWARES':{
        #     'tycproject.middlewares.RandomUserAgent': 510,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        # },
        'ITEM_PIPELINES':{
            'tycproject.mongodbPipelines.MongodbPipeline_Pe168':300,
        },
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'log/log_pe168'

    }

    def start_requests(self):
        url='http://www.pe168.com/sitemap/'
        for i in range(1,2):
            yield Request(url, callback=self.parse)

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        box_body=html.find(class_='map').find(class_='box_body')
        for provinceelement in box_body.find_all('td'):
            provinceurl=provinceelement.a['href']
            province=provinceelement.a.string
            yield Request(provinceurl, callback=self.get_city)

    def get_city(self,response):
        html = BeautifulSoup(response.text, 'lxml')
        box=html.find_all(class_='box')[1]
        for citycontent in box.find_all('li'):
            cityurl=citycontent.a['href']
            city=citycontent.a.string[:-4]
            yield Request(cityurl, callback=self.get_industry,meta={'city': city})

    def get_industry(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        box_body=html.find(class_='box_body border_n_l_r list_qiye')
        for industryelement in box_body.find_all('td'):
            industryurl = industryelement.a['href'].strip(' ')
            industry = industryelement.a.string
            yield Request(industryurl, callback=self.get_industry2, meta={'city': city,'industry':industry})

    def get_industry2(self,response):
        city = response.meta['city']
        industryflag=response.meta['industry']
        html = BeautifulSoup(response.text, 'lxml')
        flag=html.find(class_='box_body border_n_l_r list_qiye')
        if industryflag in flag.__str__():
            yield Request(response.url, callback=self.get_industry3, meta={'city': city})
        else:
            for industryelement in flag.find_all('td'):
                industryurl = industryelement.a['href'].strip(' ')
                industry = industryelement.a.string
                yield Request(industryurl, callback=self.get_industry2, meta={'city': city, 'industry': industry})

    def get_industry3(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        pages = html.find(class_='pages')
        if pages:
            page = int(pages.cite.string[:-1].split('/')[1])
        else:
            page = 1
        for i in range(1, page + 1):
            url=response.url+'pn'+str(i)
            yield Request(url, callback=self.get_company, meta={'city': city})

    def get_company(self,response):
        city = response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        box_body=html.find(class_='box_body border_n_l_r')
        for companyelement in box_body.find('tr'):
            name=companyelement.find('li').a.string
            companyNameItem = CompanyNameItem()
            companyNameItem['city'] = city
            companyNameItem['name'] = name
            yield companyNameItem







