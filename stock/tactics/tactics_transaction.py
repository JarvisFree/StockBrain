#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/19 15:25
@Author  ：维斯
@File    ：tactics_transaction.py
@Version ：1.0
@Function：止盈止损策略
    解说：阶梯式买卖进行止盈止损，最大程度降低成本（比如：分4次操作）
    备注：忽略手续费
"""

if __name__ == '__main__':
    buying_price = 2.02  # 买入价格
    selling_price = 0.00  # 卖出价格
    day_count = [1, 2, 3, 4, 5]
