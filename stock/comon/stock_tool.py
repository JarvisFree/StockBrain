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

from stock.comon.decorator import elapsed_time
from stock.db.db import DB


def is_trading_by_db(date, is_print=True):
    """
    判断是否是沪深A股交易日（请求数据库）
    :param date: 指定日期（格式：yyyymmdd）
    :param is_print:
    :return:True/False/错误提示
    """
    result_list = DB().select_ta_check_trading(date)
    if is_print:
        if len(result_list) == 1:
            if result_list[0][1] == 0:
                print(f'{date}：不是交易日_by_db')
                return False
            if result_list[0][1] == 1:
                print(f'{date}：是交易日_by_db')
                return True
        else:
            if len(result_list) == 0:
                res = f'{date}数据库无此日期_by_db'
                print(res)
                return res
            if len(result_list) > 1:
                res = f'{date}数据库有多个此日期_by_db'
                print(res)
                return res
    else:
        if len(result_list) == 1:
            if result_list[0][1] == 0: return False
            if result_list[0][1] == 1: return True
        else:
            if len(result_list) == 0: return f'{date}数据库无此日期'
            if len(result_list) > 1: return f'{date}数据库有多个此日期'


def is_trading(date, is_print=True):
    """
    TODO:如 今天是7.28周三  则7.27、7.28未获取到数据（数据不正常） 7.26有获取到数据（是交易日 数据正常）
    判断是否是沪深A股交易日
    :param date: 指定日期（格式：yyyymmdd）
    :param is_print:
    :return:True/False/错误提示
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
    result_o = requests.get(url, params=params)
    # print(result)
    result = result_o.text.split("\r\n")[1].split(",")

    if stock_date <= date <= datetime.datetime.now().strftime('%Y%m%d'):
        if len(result) > 1:
            if is_print:
                print(f'{date}：是交易日_by_sina')
            return True
        else:
            if is_print:
                print(f'{date}：不是交易日_by_sina（{result_o.text}）')
            return False
    else:
        res = f'{date}此日期无法判断（只能判断 {stock_date}—当前日期 之间的日期是否是交易日）_by_sina'
        if is_print:
            print(res)
        return res


def get_last_day(refer_day):
    """
    获取指定日期的的上一个交易日
    @param refer_day: 指定日期 yyyymmdd
    @return:
    """
    d = datetime.datetime.strptime(refer_day, '%Y%m%d')
    offset = datetime.timedelta(days=-1)
    new_day = (d + offset).strftime('%Y%m%d')
    if is_trading_by_db(new_day):
        return new_day
    else:
        return get_last_day(new_day)


def get_next_day(refer_day):
    """
    获取指定日期的的下一个交易日
    @param refer_day: 指定日期 yyyymmdd
    @return:
    """
    d = datetime.datetime.strptime(refer_day, '%Y%m%d')
    offset = datetime.timedelta(days=+1)
    new_day = (d + offset).strftime('%Y%m%d')
    if is_trading_by_db(new_day):
        return new_day
    else:
        return get_next_day(new_day)


@elapsed_time('判断日期是否是交易日')
def to_db(day_count: int):
    """
    日期是否是交易日期 写入数据库（已有的不会重复写入）
    @param day_count: 距今天数
    @return:
    """
    date_list = []
    now_date = datetime.datetime.now().strftime('%Y%m%d')
    db = DB()

    def last_day(now_date):
        d = datetime.datetime.strptime(now_date, '%Y%m%d')
        offset = datetime.timedelta(days=-1)
        return (d + offset).strftime('%Y%m%d')

    for i in range(day_count):
        if len(db.select_ta_check_trading(now_date)) != 0:
            # 上一日
            print(f'{now_date}数据已有')
            now_date = last_day(now_date)
            continue
        print(f'第{i + 1}次：{now_date}')
        r_t = is_trading(now_date, is_print=True)
        if type(r_t).__name__ == 'bool':
            if r_t:
                db.add_ta_check_trading(now_date, 1)
            else:
                db.add_ta_check_trading(now_date, 0)
        else:
            print(r_t)
            break
        # 上一日
        now_date = last_day(now_date)
        # 结束
    db.cur.close()
    db.con.close()


# if __name__ == '__main__':
#     print('aaa:', get_next_day('20210804'))

if __name__ == '__main__':
    to_db(365 * 1)
