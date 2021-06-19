#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/19 10:45
@Author  ：维斯
@File    ：tactics_hot.py
@Version ：1.0
@Function：热点策略
    解说：
    1.1、找到热点行业
    1.2、找到某热点行业中的龙头股票
    1.3、找到某热点行业 历史中 龙头股票大涨后 带领其他次龙头股票上涨的股票
    1.4、根据某行业的龙头股票大涨信号 提前布局该行业的次龙头股票
"""

from stock.base.stock_base_data import get_hang_ye
from operator import itemgetter


def get_now_hot():
    """
    获取当前热点行业
    解说：涨跌幅前10名 中 上涨家数前3的行业为当前热点行业
    """
    percent = 5
    count = 3
    result_dict = get_hang_ye()
    result_list = result_dict['diff']

    # 涨跌幅前n名
    result_list = sorted(result_list, key=itemgetter('f3'), reverse=True)
    result_list = result_list[:percent]
    # 上涨家数前n
    result_list = sorted(result_list, key=itemgetter('f104'), reverse=True)
    result_list = result_list[:count]

    # print(*result_list, sep='\n')

    print(f'{"行业名称": <7}{"涨跌幅": <6}{"上涨家数": <4}')
    for i in result_list:
        print(f'{i["f14"]: <7}{str(i["f3"]) + "%": ^6}{i["f104"]: ^8}')


if __name__ == '__main__':
    get_now_hot()
