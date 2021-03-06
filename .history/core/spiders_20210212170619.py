# -*- coding: utf-8 -*-

import requests
from lxml import etree
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from lib.db import Engine


# 定义的爬虫类
# 默认采用BeautifulSoup作为解析器，使用CSS定位或者Tag定位
# 主要负责网页爬取和网页元素的查找
# 爬虫不负责网页数据的转换与处理，由Module负责处理
class Spider:
    parser = None
    parser_xpath = None

    def __init__(self, module):
        self.module = module

    def load(self, url=None, headers=None, cookies=None):
        if url:
            return self.load_by_params(url=url, params=None, headers=headers, cookies=cookies)
        else:
            return self.load_by_params(url=self.module.url, params=None, headers=headers, cookies=cookies)

    def load_by_params(self, url, params, headers=None, cookies=None):
        try:
            self.module.url = url
            if params:
                response = requests.get(
                    url, params=params, headers=headers, cookies=cookies)
            else:
                response = requests.get(url, headers=headers, cookies=cookies)
            response.encode = 'utf-8'
            html_doc = response.text
            self.parser = BeautifulSoup(html_doc, 'lxml')
            self.parser_xpath = etree.HTML(self._html)
            self.module.parser = self.parser
        except Exception as e:
            print('Error: %s' % e)


# 定义的机器人
# 用来自动执行脚本
class Robot(object):
    def __init__(self, spider: Spider, script: list):
        self.spider = spider
        self.module = spider.module
        self.script = script

    def run(self, **kwargs):
        self.module.run(self, **kwargs)


# 这个模块用来定义爬虫要爬取对象的爬取动作
# 主要的实现逻辑就是在这个类中实现的
# 你需要继承这个类并且重写他的方法
class Module:
    __hostname__ = ''
    __domainname__ = ''
    parser = None
    url = ''
    catalog_list = []

    def __init__(self, url, engine: Engine):
        ul = urlparse(url)
        if ul.scheme and ul.hostname:
            self.__domainname__ = ul.scheme + '://' + ul.hostname
        self.url = url
        self.engine = engine

    # 执行脚本
    def run(self, robot: Robot, **kwargs):
        pass

    @property
    def domainname(self):
        return self.__domainname__

    @property
    def hostname(self):
        return self.__hostname__

    def get_catalog_list(self, xpath):
        pass

    def get_table(self, tbody, row, col):
        pass

    def save_to_db(self, data):
        pass
