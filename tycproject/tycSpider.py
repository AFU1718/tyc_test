# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request,FormRequest
from tycproject.items import CompanyNameItem
from scrapy.http.cookies import CookieJar



class TycSpider(scrapy.Spider):
    name = 'tycSpider'
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED' : False,
        'DOWNLOADER_MIDDLEWARES':{
            'tycproject.middlewares.SeleniumMiddleware': 543,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        },
    #     'ITEM_PIPELINES':{
    #         'tycproject.mongodbPipelines.MongodbPipeline_Qiye58':300,
    #     },
    #
    #
    }
    #
    # headers = {
    #     'Connection': 'keep - alive',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Referer':'https://www.tianyancha.com/',
    #     'Accept-Encoding':'gzip, deflate, br',
    #     'Accept-Language':'zh-CN,zh;q=0.9'
    # }
    # cookie_jar = CookieJar()

    def start_requests(self):
        url = 'https://www.tianyancha.com/'
        for i in range(1,2):
            yield Request(url, meta = {'usedSelenium': True,},callback = self.parse)

    def parse(self, response):
        # self.cookie_jar.extract_cookies(response, response.request)
        html=BeautifulSoup(response.text,'lxml')
        a=html.find(class_='right tyc-nav ')
        # print('~~~~~~~~~~~~~`~~~~~~~~~~~~~~~')
        # print(a)
        # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        # cookies=response.request.cookies
    #     cookies['tyc-user-info']='%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODg5ODQwMDQ5NiIsImlhdCI6MTUzNzQyMjU2OSwiZXhwIjoxNTUyOTc0NTY5fQ.P2mZ8kCQKPhVlzxNpRDeBkDafxAA4HTxMC3Hs8Sj0fSGmIZrSjo_8LsnQpm_ZkCHZO8QoBeqf_GpqQtHFS8zTA%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25221%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218898400496%2522%257D'
    #     cookies['auth_token']='eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODg5ODQwMDQ5NiIsImlhdCI6MTUzNzQyMjU2OSwiZXhwIjoxNTUyOTc0NTY5fQ.P2mZ8kCQKPhVlzxNpRDeBkDafxAA4HTxMC3Hs8Sj0fSGmIZrSjo_8LsnQpm_ZkCHZO8QoBeqf_GpqQtHFS8zTA'
    #     yield Request('https://www.tianyancha.com/cd/login.json',  meta={'usedSelenium': False},callback=self.qqq,cookies=cookies)
    # def qqq(self,response):
    #     print(response.text)

