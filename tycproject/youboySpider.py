# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from tycproject.items import CompanyNameItem
import logging


class YouboySpider(scrapy.Spider):
    logger = logging.getLogger(__name__)
    name = 'youboySpider'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        # 'DOWNLOADER_MIDDLEWARES':{
        #     'tycproject.middlewares.RandomUserAgent': 510,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        # },
        'ITEM_PIPELINES':{
            'tycproject.mongodbPipelines.MongodbPipeline_Youboy':300,
        },
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'log/log_youboy'

    }
    provincedict = {'1': '广东',
                    '2': '北京',
                    '3': '福建',
                    '4': '上海',
                    '5': '天津',
                    '6': '辽宁',
                    '7': '浙江',
                    '8': '江苏',
                    '9': '山东',
                    '10': '河南',
                    '11': '四川',
                    '12': '陕西',
                    '13': '重庆',
                    '14': '广西',
                    '15': '青海',
                    '16': '内蒙古',
                    '17': '云南',
                    '18': '新疆',
                    '19': '贵州',
                    '20': '西藏',
                    '21': '宁夏',
                    '22': '山西',
                    '23': '黑龙江',
                    '24': '吉林',
                    '25': '湖南',
                    '26': '河北',
                    '27': '湖北',
                    '28': '海南',
                    '29': '江西',
                    '30': '安徽',
                    '31': '甘肃',
                    }


    def start_requests(self):
        url = 'http://qiye.youboy.com/'
        for i in range(1,32):
            for j in range(1,1001):
                yield Request(url+'pro'+str(i)+'_'+str(j)+'.html', callback=self.parse,meta={'city':self.provincedict[str(i)]})

    def parse(self, response):
        province=response.meta['city']
        html = BeautifulSoup(response.text, 'lxml')
        dqscontit = html.find_all(class_='dqscontit')
        for nameelement in dqscontit:
            name=nameelement.a.string
            companyNameItem = CompanyNameItem()
            companyNameItem['city'] = province
            companyNameItem['name'] = name
            yield companyNameItem



