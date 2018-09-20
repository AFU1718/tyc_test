# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request,FormRequest
from tycproject.items import CompanyNameItem
from scrapy.http.cookies import CookieJar
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
import time

# scrapy 信号相关库
from scrapy.utils.project import get_project_settings
from scrapy import signals

# 下面这种方式，即将废弃，所以不用
# from scrapy.xlib.pydispatch import dispatcher
# scrapy最新采用的方案
from pydispatch import dispatcher


class TestTycSpider(scrapy.Spider):
    name = 'testTycSpider'
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED' : True,
        'DOWNLOADER_MIDDLEWARES':{
            'tycproject.middlewares.TestSeleniumMiddleware': 543,
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

    # 将chrome初始化放到spider中，成为spider中的元素
    def __init__(self, timeout=30, isLoadImage=True, windowHeight=None, windowWidth=None):
        # 从settings.py中获取设置参数
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting['SELENIUM_TIMEOUT']
        self.isLoadImage = self.mySetting['LOAD_IMAGE']
        self.windowHeight = self.mySetting['WINDOW_HEIGHT']
        self.windowWidth = self.mySetting['windowWidth']
        # 初始化chrome对象
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('lang=zh_CN.UTF-8')
        self.options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
        self.browser = webdriver.Chrome(chrome_options=self.options)

        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(900, 900)
        self.browser.set_page_load_timeout(self.timeout)  # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, 10)  # 指定元素加载超时时间


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
        # print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        # print(response.request.cookies)

        cookie=response.request.cookies
        print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        print(cookie)
        yield Request('https://www.tianyancha.com/search?key=%E6%AF%8D%E5%A9%B4',  meta={'usedSelenium': False},callback=self.qqq,cookies=cookie)
    def qqq(self,response):

        print(response.text)

