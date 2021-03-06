# -*- coding: utf-8 -*-
from core.spider import SpiderSelenium
import time
import datetime


class Robot(object):
    def __init__(self, url):
        self._url = url
        self._spider = SpiderSelenium()

    def run(self):
        # 加载页面
        self.load(self._url)
        # 检查交易状态
        if get_state == "闭市":
            # 如果不在交易中，获取最近5天的交易数据
            self.refresh()
            # 全屏展示
            dr.find_element_by_class_name("kke_cfg_fullscreen").click()
            pyautogui.click(150, 170)
            pyautogui.click(1630, 500)
            # 获取每天每分钟的行情数据
            n = 0
            for i in range(780*days):
                n += get_price(dr)
                if n > 1560:            # 检测到重复数据n次时自动退出
                    break
                pyautogui.typewrite(["left"], 0.25)
                n = 0
                time.sleep(0.1)

        else:
            # 如果在交易中，或者即将开盘，就循环获取最近10分钟的最新交易价格和交易量
            self.refresh()

    def refresh(self):
        self._spider.find_element_by_xpath('//*[@id="fr clearfix"]/a').click()

    def load(self, url):
        self._spider.open(url)
        self._spider.max_window()

        # 关闭弹幕
        self._spider.find_element_by_class_name("b_controll").click()

        # 关闭广告条
        elements = self._spider.find_elements_by_class_name("close")
        for el in elements:
            if el.tag_name == 'img':
                el.click()

    def get_state(self):
        return self._spider.find_element_by_id("status_em", self.text)

    @staticmethod
    def text(element):
        return element.text
