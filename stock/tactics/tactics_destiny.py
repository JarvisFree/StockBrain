#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/28 21:21
@Author  ：维斯
@File    ：tactics_destiny.py
@Version ：1.0
@Function：天命策略

解说：
step1：T-1收盘后筛选
    1.1、涨幅前10的概念，作为股票基础一级池
    1.2、涨幅：>=4%
    1.3、量比>1
    1.4、换手率：>=6%
    结果、筛选出的股票作为T_1股票池
step2：T购买当天下午14：30左右筛选
    2.1、涨幅前10的概念，作为股票基础一级池
    2.2、涨幅：>=4%
    2.3、量比>1
    2.4、换手率：>=6%
    结果、筛选出的股票作为T股票池
step3：查找命中股并购买
    3.1、T与T_1股票池中的交集股票即为命中股票，作为MZ股票池
    3.2、人工筛选MZ股票池中资金博弈为红、黄线居上的个股，作为JC股票池
    3.3、JC股票池中任意挑选一只个股进行建仓
step4：个股数据跟踪
    4.1、已建仓的个股设置止盈止损提醒（止盈：5%，止损：5%），自己写程序设置提醒
"""

import datetime
import time

from stock.base.get_data_server import GetMicData, MonitorData
from stock.comon.message import send_sms


def step4(stock_id: str, start_price: float, phone_list: list):
    """
    个股数据跟踪
    @param stock_id: sh600010
    @param start_price: 建仓价格
    @param phone_list: 接收手机号列表
    """
    win_range = 0.05
    lose_range = -0.05
    stop_win = float('%.3f' % (start_price * (1 + win_range)))
    stop_lose = float('%.3f' % (start_price * (1 + lose_range)))

    while True:
        result = MonitorData.monitor_price(stock_id)
        message = f'\r\n名称：{stock_id}\r\n开始：{start_price}\r\n上限：{stop_win}（+{win_range * 100}%）\r\n下限：{stop_lose}（{lose_range * 100}%）\r\n当前：{result[1]}'
        end_with = f'\r\n检测：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\r\n实际：{result[0]}'
        message += end_with
        if float(result[1]) <= stop_lose:
            message += '\r\n\r\n结论：已触发下限'
            send_sms(phone_list, message)
            print(message)
            break
        elif float(result[1]) >= stop_win:
            message += '\r\n\r\n结论：已触发上限'
            send_sms(phone_list, message)
            print(message)
            break
        time.sleep(5)


if __name__ == '__main__':
    step4('sh600010', 2.530, ['13678066240'])
