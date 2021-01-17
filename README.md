# shGlodPrice

*采用爬虫每天自动获取每天上海黄金交易所各类合约的交易价格*

## 数据来源

数据来自上海黄金交易所[每日行情](https://www.sge.com.cn/sjzx/mrhqsj?p=1)
计划每天早盘和午盘收盘后更新。

## 目录结构

```
shGlodPrice
|__ manager.py           程序入口
```

## 使用方法

修改 manager.py 中的 number 值，这个表示需要爬取的列表页数，默认一页10天的数据。然后执行下面的命令即可。
```
$ python manager.py
```

## 更新记录

- 2021-1-18 实现数据保存时去重与爬取效率提升
- 2021-1-17 实现上海黄金交易所每日交易数据爬取以及保存数据库


## Api接口

计划写一个API接口，待上诉问题解决以后就开始。
