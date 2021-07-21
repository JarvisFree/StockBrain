#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/21 16:59
@Author  ：维斯
@File    ：stock_tool.py
@Version ：1.0
@Function：股票工具
"""
import datetime

import requests


def is_trading(date, is_print=True):
    """
    判断是否是沪深A股交易日
    :param date: 指定日期（格式：yyyymmdd）
    :param is_print:
    :return:True/False
    """
    stock_id = 'sh600601'
    stock_date = '19901219'  # 上市时间
    # 判断传入的代码是否是字母加数字（如 sz002415）
    if stock_id.isalnum():
        stock_id = stock_id[2:]
    # 如果股票代码首位是0或者3则需添加一个1，反之则需添加一个0
    if stock_id[0] == "0" or stock_id[0] == "3":
        stock_id = "1" + stock_id
    else:
        stock_id = "0" + stock_id
    url = "http://quotes.money.163.com/service/chddata.html?"
    params = {
        "code": stock_id,
        "end": date,
        "fields": "TOPEN",
        "start": date
    }
    result = requests.get(url, params=params)
    result = result.text.split("\r\n")[1].split(",")

    if len(result) > 1:
        if is_print:
            print(f'{date}：是交易日')
        return True
    else:
        if is_print:
            if date > stock_id and date > datetime.datetime.now().strftime('%Y%m%d'):
                print(f'{date}此日期无法判断（只能判断 {stock_date}—当前日期 之间的日期是否是交易日）')
                return False
            print(f'{date}：不是交易日')
        return False


if __name__ == '__main__':
    is_trading('20210722', True)
