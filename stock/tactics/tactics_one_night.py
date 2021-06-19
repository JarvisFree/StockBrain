#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/19 14:45
@Author  ：维斯
@File    ：tactics_one_night.py
@Version ：1.0
@Function：1夜持股策略
"""

from stock.base.stock_base_data import get_a_all_stock


def get_one():
    result = get_a_all_stock()
    re_list = result['diff']
    true_results = []
    for i in re_list:
        try:
            # 1 涨幅（3%-5%）
            if float(i['f3']) > 3.0 and float(i['f3']) < 5.0:
                # 2 量比大于等于1
                if float(i['f10']) >= 1:
                    # 3 换手率（5%-10%）
                    if float(i['f8']) > 5.0 and float(i['f8']) < 10.0:
                        # 4 流通市值（50亿-200亿）
                        if int(int(i['f21']) / 100000000) > 50 and int(int(i['f21']) / 100000000) < 200:
                            true_results.append(i)
        except:
            continue
    print(f'符合【1夜持股策略】的股票，初步筛选结果：{len(true_results)}只')
    print(*true_results, sep='\n')


# 13678066240 张
if __name__ == '__main__':
    get_one()
