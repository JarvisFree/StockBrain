#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/21 16:33
@Author  ：维斯
@File    ：tactics_eat_harden.py
@Version ：1.0
@Function：吃涨停策略
    解说：
    一、策略验证
    1、5+个交易日收盘价持续下跌的个股（返回：个股代码，个股名称，持续下跌的交易日列表）
    2、开始出现上涨后的第一根阴线的最低价（返回：此阴线交易日，此阴线最低价）
    3、

    二、策略选股
"""
import datetime

from stock.base.get_data_server import GetMicData
from stock.comon.calc_tool import find_desc, find_asc
from stock.comon.decorator import elapsed_time
from stock.comon.stock_tool import is_trading, is_trading_by_db

"""
            {
                "F0_DATE": "2021-07-16",  # 日期
                "F1_STOCK_ID": "'600010",  # 股票代码
                "F2_STOCK_NAME": "包钢股份",  # 股票名称
                "F3_OPEN": "2.18",  # 开盘价
                "F4_CLOSE": "2.15",  # 收盘价
                "F5_HIGH": "2.27",  # 最高价
                "F6_LOW": "2.12",  # 最低价
                "F7_CHG": "-0.1",  # 涨跌额
                "F8_P_CHG": "-4.4444",  # 涨跌幅（表示：-4.4444%）
                "F9_TURNOVER": "7.1349",  # 换手率（表示：7.1349%）
                "F10_VO_TURNOVER": "2260138773",  # 成交量（表示：2260万手）
                "F11_VA_TURNOVER": "4963746153.0",  # 成交金额（元）
                "F12_T_CAP": "98007820193.2",  # 总市值（元）
                "F13_M_CAP": "68106004912.1" # 流通市值（元）
            }
"""


@elapsed_time('获取指定股票最近N个自然日的数据')
def get_1(day_count: int, stock_id='sh600010'):
    def get_old_date(count=1):
        """
        获取前N天日期
        """
        now_date = datetime.datetime.now().strptime(datetime.datetime.now().strftime('%Y%m%d'), '%Y%m%d')
        offset_day = datetime.timedelta(days=-count)
        new_date = (now_date + offset_day).strftime('%Y%m%d')
        print(f'前{count}天日期为：{new_date}')
        return new_date

    target_date = datetime.datetime.now().strftime('%Y%m%d')
    target_data = []
    for i in range(day_count):
        if is_trading_by_db(target_date):
            target_data.append(GetMicData.get_alone_data_by_sina(stock_id, target_date))
        target_date = get_old_date(i + 1)
    return target_data


@elapsed_time('获取包钢股份历史中连续N个交易日持续下跌')
def get_11(day_count: int, min_limit, stock_id):
    """
    获取指定个股历史中连续N及以上个交易日持续下跌的数据
    @param day_count: 历史天数（365：最近365个自然日）
    @param min_limit: 连续N天
    @param stock_id: 股票ID（sh600010）
    @return:
    """
    result = get_1(day_count, stock_id)
    re_data = find_asc(result, min_limit, keyword='F4_CLOSE')
    print(f'共有{len(re_data)}次连续{min_limit}个及以上交易日持续下跌')
    return re_data


if __name__ == '__main__':
    print(*get_11(100, 5, 'sh600010'), sep='\n')
