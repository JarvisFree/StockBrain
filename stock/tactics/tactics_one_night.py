#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/19 14:45
@Author  ：维斯
@File    ：tactics_one_night.py
@Version ：1.0
@Function：1夜持股策略

策略来源：https://m.toutiao.com/is/eWsFTGt/

【初步筛选】
1、涨幅：3%-5%
2、量比>1
3、换手率：5%-15%
4、流通市值： <150亿

【详细筛选】
5、日K线中处于上升趋势
    可以通过 T+1的最高价 > T+0的开盘价来计算 或者
    可以通过 T+1的最高价 > T+0的最低价来计算
6、选择筹码集中，并且上方没有密集套牢盘的股票，筹码集中代表有爆发潜力，没有套牢盘说明上涨阻力小
7、对比当天大盘和个股走势的分时图，选择在大盘涨时跟涨，跌时抗跌的股票。
8、最后选择包含有当前热点题材的股票，什么是热点题材，就是近期频繁轮动的，处于市场一线的题材

总结：
最后强调一下，方法固然好用，但是不是每天都有机会，
在大盘处于单边下跌的时候要尽量避免使用，横盘的时候效果最好，选股是一门学问，正是因为有这么多的前提条件，才能有好的结果。
"""
import datetime

from stock.base.get_data_server import GetMicData
from stock.base.stock_base_data import get_a_all_stock
from stock.comon.decorator import elapsed_time


@elapsed_time('1夜持股策略')
def get_one():
    result = get_a_all_stock()
    re_list = result['diff']
    true_results = []
    now_date = datetime.datetime.now().strftime('%Y%m%d')
    for i in re_list:
        print(f'{re_list.index(i) + 1}/{len(re_list)}')
        try:
            # 1、涨幅：3%-5%
            if 3.0 < float(i['f3']) < 5.0:
                # 2、量比>1
                if float(i['f10']) > 1:
                    # 3、换手率：5%-15%
                    if 5.0 < float(i['f8']) < 15.0:
                        # 4、流通市值： <150亿
                        if int(int(i['f21']) / 100000000) < 150:
                            # 5、日K线中处于上升趋势（2日）
                            if GetMicData.continue_up(i['f12'], 1, now_date, 1008602) is not None:
                                true_results.append(i)
        except:
            continue
    print(f'符合【1夜持股策略】的股票，初步筛选结果：{len(true_results)}只')  # 62只
    print(*true_results, sep='\n')


if __name__ == '__main__':
    get_one()
