# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
import time

class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o=cls(random.choice(crawler.settings.getlist['USER_AGENTS']))
        # o = cls(crawler.settings.get['USER_AGENT'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)

class SeleniumMiddleware():
    # 经常需要在pipeline或者中间件中获取settings的属性，可以通过scrapy.crawler.Crawler.settings属性
    @classmethod
    def from_crawler(cls, crawler):
        # 从settings.py中，提取selenium设置参数，初始化类
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   isLoadImage=crawler.settings.get('LOAD_IMAGE'),
                   windowHeight=crawler.settings.get('WINDOW_HEIGHT'),
                   windowWidth=crawler.settings.get('WINDOW_WIDTH')
                   )

    def __init__(self, timeout=30, isLoadImage=True, windowHeight=None, windowWidth=None):
        self.timeout = timeout
        self.isLoadImage = isLoadImage

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('lang=zh_CN.UTF-8')
        self.options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
        self.browser = webdriver.Chrome(chrome_options=self.options)

        if windowHeight and windowWidth:
            self.browser.set_window_size(900, 900)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, 10)

    def process_request(self, request, spider):
        print(f"chrome is getting page")
            # 依靠meta中的标记，来决定是否需要使用selenium来爬取
        usedSelenium = request.meta.get('usedSelenium', False)
        if usedSelenium:
            try:
                self.browser.get(request.url)
                submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                '#web-content > div > div.tyc-home-top.bgtyc > div.mt-74 > div > div > div.right.tyc-nav > div:nth-child(1) > a')))
                submit.click()
                login_user_password = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             '#_modal_container > div > div > div.body.-detail.modal-scroll > div > div > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein2.message_box.pl15.pr15.f-base.collapse.in > div.mt10.mb10.link-click.text-right')))
                login_user_password.click()
                input_user = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[2]/input')))
                input_password = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/input')))
                input_user.send_keys('18898400496')
                input_password.send_keys('fu1718fu1718')
                submit_user_password = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[5]')))
                submit_user_password.click()
                seleniumCookies = self.browser.get_cookies()

            except Exception as e:
                return HtmlResponse(url=request.url, status=500, request=request)
            else:
                time.sleep(2)
                cookie = [item["name"] + ":" + item["value"] for item in seleniumCookies]
                cookMap = {}
                for elem in cookie:
                    str = elem.split(':')
                    cookMap[str[0]] = str[1]

                request.cookies = cookMap  # 让这个带有登录后cookie的Request继续爬取
                print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                print(cookMap)
                request.meta['usedSelenium'] = False
                return HtmlResponse(url=request.url,body=self.browser.page_source,
                                    request=request,
                                    # 最好根据网页的具体编码而定
                                    encoding='utf-8',
                                    status=200,)


class TestSeleniumMiddleware():
    def process_request(self, request, spider):
        usedSelenium = request.meta.get('usedSelenium', False)
        if usedSelenium:
            try:
                # 会自动跳转到登录页面
                spider.browser.get(request.url)
                submit = spider.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                     '#web-content > div > div.tyc-home-top.bgtyc > div.mt-74 > div > div > div.right.tyc-nav > div:nth-child(1) > a')))
                submit.click()
                login_user_password = spider.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                  '#_modal_container > div > div > div.body.-detail.modal-scroll > div > div > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein2.message_box.pl15.pr15.f-base.collapse.in > div.mt10.mb10.link-click.text-right')))
                login_user_password.click()
                input_user = spider.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[2]/input')))
                input_password = spider.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/input')))
                input_user.send_keys('18898400496')
                input_password.send_keys('fu1718fu1718')
                submit_user_password = spider.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[5]')))
                submit_user_password.click()
                seleniumCookies = spider.browser.get_cookies()
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                print(seleniumCookies)

            except Exception as e:
                return HtmlResponse(url=request.url, status=500, request=request)
            else:


                cookie = [item["name"] + ":" + item["value"] for item in seleniumCookies]
                cookMap = {}
                for elem in cookie:
                    str = elem.split(':')
                    cookMap[str[0]] = str[1]
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                print(cookMap)
                request.cookies = cookMap  # 让这个带有登录后cookie的Request继续爬取
                request.meta['usedSelenium'] = False
                return HtmlResponse(url=request.url, body=spider.browser.page_source,
                                    request=request,
                                    # 最好根据网页的具体编码而定
                                    encoding='utf-8',
                                    status=200, )