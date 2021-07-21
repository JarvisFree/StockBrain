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
from stock.comon.decorator import elapsed_time
from stock.comon.stock_tool import is_trading

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
        if is_trading(target_date):
            target_data.append(GetMicData.get_alone_data_by_sina(stock_id, target_date))
        target_date = get_old_date(i + 1)
    return target_data


@elapsed_time('获取包钢股份历史中连续N个交易日持续下跌')
def get_11(day_count: int, stock_id='sh600010'):
    result = get_1(day_count, stock_id)
    all_model = []
    count = 1
    while True:
        if len(result) >= 5:
            print(f'第{count}次循环，result长度={len(result)}')
            count += 1
            if result[0]['F4_CLOSE'] < result[1]['F4_CLOSE'] < \
                    result[2]['F4_CLOSE'] < result[3]['F4_CLOSE'] < result[4]['F4_CLOSE']:
                all_model.append(
                    (
                        result[0],
                        result[1],
                        result[2],
                        result[3],
                        result[4],
                    )
                )
                result.pop(0)
            else:
                result.pop(0)
        else:
            break
    print(f'共有{len(all_model)}次连续5个交易日持续下跌')
    return all_model


if __name__ == '__main__':
    print(*get_11(365 * 2, 'sh600010'), sep='\n')
    # ss = (
    #     {'F0_DATE': '2021-03-24', 'F1_STOCK_ID': "'600010", 'F2_STOCK_NAME': '包钢股份', 'F3_OPEN': '1.58',
    #      'F4_CLOSE': '1.54',
    #      'F5_HIGH': '1.6', 'F6_LOW': '1.53', 'F7_CHG': '-0.06', 'F8_P_CHG': '-3.75', 'F9_TURNOVER': '3.3741',
    #      'F10_VO_TURNOVER': '1068813665', 'F11_VA_TURNOVER': '1666476636.0', 'F12_T_CAP': '70200950277.9',
    #      'F13_M_CAP': '48782905844.0'},
    #     {'F0_DATE': '2021-03-23', 'F1_STOCK_ID': "'600010", 'F2_STOCK_NAME': '包钢股份', 'F3_OPEN': '1.67',
    #      'F4_CLOSE': '1.6',
    #      'F5_HIGH': '1.68', 'F6_LOW': '1.59', 'F7_CHG': '-0.08', 'F8_P_CHG': '-4.7619', 'F9_TURNOVER': '3.9376',
    #      'F10_VO_TURNOVER': '1247333896', 'F11_VA_TURNOVER': '2023953229.0', 'F12_T_CAP': '72936052236.8',
    #      'F13_M_CAP': '50683538539.2'},
    #     {'F0_DATE': '2021-03-22', 'F1_STOCK_ID': "'600010", 'F2_STOCK_NAME': '包钢股份', 'F3_OPEN': '1.71',
    #      'F4_CLOSE': '1.68',
    #      'F5_HIGH': '1.74', 'F6_LOW': '1.65', 'F7_CHG': '-0.03', 'F8_P_CHG': '-1.7544', 'F9_TURNOVER': '3.8398',
    #      'F10_VO_TURNOVER': '1216347331', 'F11_VA_TURNOVER': '2055509637.0', 'F12_T_CAP': '76582854848.6',
    #      'F13_M_CAP': '53217715466.2'},
    #     {'F0_DATE': '2021-03-19', 'F1_STOCK_ID': "'600010", 'F2_STOCK_NAME': '包钢股份', 'F3_OPEN': '1.72',
    #      'F4_CLOSE': '1.71',
    #      'F5_HIGH': '1.76', 'F6_LOW': '1.68', 'F7_CHG': '-0.05', 'F8_P_CHG': '-2.8409', 'F9_TURNOVER': '3.6293',
    #      'F10_VO_TURNOVER': '1149673900', 'F11_VA_TURNOVER': '1974537177.0', 'F12_T_CAP': '77950405828.1',
    #      'F13_M_CAP': '54168031813.8'},
    #     {'F0_DATE': '2021-03-18', 'F1_STOCK_ID': "'600010", 'F2_STOCK_NAME': '包钢股份', 'F3_OPEN': '1.8',
    #      'F4_CLOSE': '1.76',
    #      'F5_HIGH': '1.81', 'F6_LOW': '1.75', 'F7_CHG': '-0.04', 'F8_P_CHG': '-2.2222', 'F9_TURNOVER': '3.63',
    #      'F10_VO_TURNOVER': '1149883261', 'F11_VA_TURNOVER': '2036145249.0', 'F12_T_CAP': '80229657460.5',
    #      'F13_M_CAP': '55751892393.1'})
    # print(*ss, sep='\n')

