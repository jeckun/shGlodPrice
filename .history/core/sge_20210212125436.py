# -*- coding: utf-8 -*-

# 从上海黄金交易所下载每日交易数据
# 网址：https://www.sge.com.cn/sjzx/mrhqsj?p=1

from .spiders import Module
from .robots import Robot
from config import sge_xpath


class Sge(Module):
    __hostname__ = '上海黄金交易所'
    trade_record = {}

    def run(self, robot: Robot):
        for task in robot.script:
            if task == 'load':
                robot.spider.load()
            elif task == 'get_catalog_list':
                robot.module.get_catalog_list(sge_xpath['catalog_list'])
            elif task == 'get_table':
                robot.module.get_table(
                    sge_xpath['tbody'], sge_xpath['row'], sge_xpath['col'])
            elif task == 'save_to_db':
                robot.module.save_to_db(robot.module.trade_record, Engine)
                pass
