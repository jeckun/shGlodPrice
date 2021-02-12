# -*- coding: utf-8 -*-
from core.spider import SpiderSelenium
from core.db import TimeSharingChart, session
import time
import re
from datetime import datetime
import pyautogui


class Robot(object):
    isSavetoDB = False

    def __init__(self, url):
        self._url = url
        self._spider = SpiderSelenium()

    def run(self):
        # 加载页面
        self.load(self._url)
        while True:
            self.refresh()
            self.check()
            time.sleep(1)

    def check(self):
        # 检查交易状态
        if self.get_state() == "闭市" and self.isSavetoDB == False:
            # 如果不在交易中，获取最近5天的交易数据
            # 全屏展示
            self._spider.find_element_by_class_name(
                "kke_cfg_fullscreen").click()
            # 显示最近5天的交易数据
            pyautogui.click(150, 170)
            # 获取每天每分钟的行情数据
            pyautogui.click(1630, 500)
            n = 0
            for i in range(780 * 5):
                n += self.get_price()
                if n > 1560:            # 检测到重复数据n次时自动退出
                    break
                pyautogui.typewrite(["left"], 0.25)
                n = 0
                time.sleep(0.1)
            self.isSavetoDB = True
        else:
            # 开始盯盘
            price = {}
            price["quote_time"] = dr.find_element_by_id("quote_time").text

            while dr.find_element_by_id("status_em").text != "交易中":
                try:
                    if price["quote_time"] == dr.find_element_by_id("quote_time", text):
                        price.update({"name": dr.find_element_by_xpath(
                            '//*[@id="realtime_showname"]/span', text)})
                        price.update(
                            {"quote_time": dr.find_element_by_id("quote_time", text)})
                        price.update(
                            {"now_price": dr.find_element_by_id("now_price", text)})
                        price.update(
                            {"average_price": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[2]/span[4]', text)})
                        price.update(
                            {"upordown": dr.find_element_by_id("upOrDown_div", text)})
                        price.update(
                            {"buy_price": dr.find_element_by_id("buy_price", text)})
                        price.update(
                            {"sell_price": dr.find_element_by_id("sell_price", text)})
                        price.update(
                            {"open_price": dr.find_element_by_id("open_price", text)})
                        price.update(
                            {"close_price": dr.find_element_by_id("close_price", text)})
                        price.update(
                            {"high_price": dr.find_element_by_id("high_price", text)})
                        price.update(
                            {"low_price": dr.find_element_by_id("low_price", text)})

                        price.update({
                            "five_leval": dr.find_element_by_class_name("five_leval", text)
                        })

                        if len(price["five_leval"].text) > 0:
                            price.update({
                                "five_leval":
                                [item.split(' ')
                                 for item in price["five_leval"].text.split('\n')]
                            })
                        else:
                            price.update({"five_leval": []})

                        print(price["quote_time"],  price["name"],
                              "最新价格", price["now_price"],
                              "均价", price["average_price"],
                              price["five_leval"][4],
                              price["five_leval"][5])
                except Exception as e:
                    print(e)

    def refresh(self):
        self._spider.find_element_by_xpath(
            '//*[@class="fr clearfix"]/a').click()

    def load(self, url):
        self._spider.open(url)
        self._spider.max_window()

        # 关闭弹幕
        self._spider.find_element_by_class_name("b_controll").click()

        # 显示五档盘口
        dr.find_element_by_xpath(
            "//*[@class='calendar']/div[1]/h3[2]").click()

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

    @staticmethod
    def cutDate(element):
        date = element.text[:10].replace('/', '-')
        time = element.text[12:]+":01"
        week = element.text[11:12]
        return date + " " + time

    def get_price(self):
        price = {}
        price.update(
            {"name": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/thead/tr[1]/th/span', self.text)})
        price.update(
            {"time": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[1]/th/span', self.cutDate)})
        price.update(
            {"price": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[2]/td/span', self.text)})
        price.update(
            {"av_price": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[3]/td/span', self.text)})
        price.update(
            {"upOrdown": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[4]/td/span', self.text)})
        price.update(
            {"deal": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[5]/td/span', self.text)})
        print(price["time"], price["name"], price["price"],
              price["av_price"], price["upOrdown"], price["deal"])
        return self.save_to_db(price)

    @staticmethod
    def convert_float(item):
        val = str(item).replace('%', '').replace(',', '').replace('手', '')
        return 0.0 if len(val) == 0 else float(val)

    @staticmethod
    def exists(table, code, trade_date):
        # 判断交易记录是否已经存在
        our_trade = session.query(
            table).filter_by(trans_date=trade_date).filter_by(code=code).first()
        if our_trade:
            return True
        else:
            return False

    @staticmethod
    def cutupOrdown(element):
        ls = re.split('[()]', element)
        return ls[:2]

    def save_to_db(self, line):
        if not self.exists(TimeSharingChart, line['name'], datetime.strptime(
                line['time'], "%Y-%m-%d %H:%M:%S")):
            row = TimeSharingChart(
                code=line['name'],
                trans_date=datetime.strptime(
                    line['time'], "%Y-%m-%d %H:%M:%S"),
                price=self.convert_float(line['price']),
                VWAP=self.convert_float(line['av_price']),
                spread=self.convert_float(
                    self.cutupOrdown(line['upOrdown'])[0]),
                extent=self.convert_float(
                    self.cutupOrdown(line['upOrdown'])[1]) / 100,
                volume=self.convert_float(line['deal'])
            )
            session.add(row)
            session.commit()
            return 0
        else:
            print('已经存在跳过导入：', line['name'], line['time'])
            return 1