#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/11 16:20
@Author  ：维斯
@File    ：tactics_df.py
@Version ：1.0
@Function：东风策略
"""
import time
import datetime

from stock.GetStockDataServer import GetStockDataServer


class Tool:
    @staticmethod
    def com_calc_date(date_s, model='+'):
        # 时间加减
        # 将时间字符串转换为 datetime 格式的时间
        today = datetime.datetime.strptime(date_s, '%Y%m%d')
        # 计算偏移量
        if model == '+':
            offset = datetime.timedelta(days=+1)
        elif model == '-':
            offset = datetime.timedelta(days=-1)
        else:
            print('模式错误')
        # 获取修改后的时间并格式化
        re_date = (today + offset).strftime('%Y%m%d')
        # print(re_date)  # 2020-11-15 19:48:51
        return re_date


def get_high(stock_id, date):
    """
    判断指定股票在指定日期是否触发过涨停
    @param stock_id: 'sh600010'
    @param date: '20210709'
    @return: True/False
    """
    result = GetStockDataServer.get2_stock_all_data_by_id_and_date(stock_id=stock_id, date=date)
    if len(result) == 0:
        return False
    zhang_ting = float(result[0]) * 1.1
    if float(result[2]) >= zhang_ting:
        return True
    else:
        return False


def start():
    now_date = datetime.datetime.now().strftime('%Y%m%d')
    data = []
    end_date = '20010309'  # 上市日期
    while True:
        if get_high('sh600010', now_date):
            data.append(now_date)
            print('触发涨停：', now_date)
        if now_date == end_date:
            break
        now_date = Tool.com_calc_date(now_date, '-')

    print(f'触发涨停日总数：{len(data)}')
    print(data)


if __name__ == '__main__':
    s_time = datetime.datetime.now()
    start()
    print(f'耗时：{datetime.datetime.now() - s_time}')
