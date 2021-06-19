#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/19 18:49
@Author  ：维斯
@File    ：tactics_average.py
@Version ：1.0
@Function：平均策略
    解说：
    1、计算平均购买N只股票的买入价格及数量
    2、在指定涨幅情况下 计算N只股票的卖出价格
"""
import json


class Params:
    # 将要投资的总资金
    total_money = 4 * 10000
    # 将要投资的股票价格列表
    price = [
        {'now_price': 1.29},
        {'now_price': 2.29},
        {'now_price': 3.29},
        {'now_price': 1.19},
        {'now_price': 7.19},
        {'now_price': 6.29},
        {'now_price': 9.09},
        {'now_price': 9.99},
        {'now_price': 8.00},
        {'now_price': 1.09},
    ]
    # 预期涨幅
    expect_range = 0.03


def calc_a(total_money, prices, expect_range):
    """
    计算平均投资数据
    :param total_money: 将要投资的总资金
    :param prices: 将要投资的股票价格列表
    :param expect_range: 预期涨幅
    :return: json
    """
    # 将要投资的总资金
    total_money = total_money
    # 将要投资的股票价格列表
    price = prices
    # 预期涨幅
    expect_range = expect_range
    tem = total_money / len(price)  # 每支股票平均投资金额
    for i in price:
        i.update({'expect_price': round(float(i.get('now_price')) * (expect_range + 1), 2)})
        i.update({'expect_number': int((tem / i.get('expect_price')) / 100) * 100})
        i.update({'expect_profit': int((i.get('expect_price') - i.get('now_price')) * i.get('expect_number'))})

    print(f'买入价格 卖出价格 数量 预期盈利')
    money_sum = 0
    profit_sum = 0
    result_json = {}
    result_list = []
    for i in price:
        print(
            f"{i.get('now_price'):^6}{i.get('expect_price'):^8}{i.get('expect_number'):^5}{i.get('expect_profit'):^8}")
        result_list.append({
            'i_price': i.get('now_price'),
            'o_price': i.get('expect_price'),
            'number': i.get('expect_number'),
            'expect_profit': i.get('expect_profit'),
        })
        money_sum += i.get('now_price') * i.get('expect_number')
        profit_sum += i.get('expect_profit')
    result_json.update({'stocks': result_list})
    result_json.update({
        'total_money': int(money_sum),
        'profit_sum': profit_sum,
    })
    print(f'投资总额：{int(money_sum)}\r\n预期盈利：{profit_sum}')
    return result_json


if __name__ == '__main__':
    result = calc_a(total_money=Params.total_money, prices=Params.price, expect_range=Params.expect_range)
    # print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
