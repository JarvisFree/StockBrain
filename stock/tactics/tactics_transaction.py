#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/19 15:25
@Author  ：维斯
@File    ：tactics_transaction.py
@Version ：1.0
@Function：交易策略（止盈止损）
    解说：阶梯式买卖进行止盈止损，最大程度降低成本（比如：分4次操作）
    备注：忽略手续费
    规则1：第一次建仓在尾盘买入
"""

from prettytable import PrettyTable

from stock.base.get_data_server import GetMicData
from stock.comon.stock_tool import get_next_day


class Old_Test:
    def __init__(self):
        # self.stock_info = [
        #     {
        #         'stock_id': 'sh600010',  # 股票代码
        #         'plan_money': 100000,  # 计划资金
        #         'start_price': 1.5,  # 买入价格（第一次建仓）
        #         'start_date': '20210706',  # 买入日期（第一次建仓）
        #         'test_days': 30  # 测试天数
        #     }
        # ]
        self.stock_info = None

    @staticmethod
    def calc_alone(par, stock_info):
        result = s_check(par)
        if not result:
            return print(result['message'])
        days = stock_info['test_days']  # 测试天数
        s1 = True
        s2 = False
        s3 = False
        data = []
        # 获取下一个交易日
        d = get_next_day(stock_info['start_date'])
        dd = d
        for i in range(days):
            # 判断是否第一次建仓止损或者达到第二次加仓价格
            result = GetMicData.get_alone_data_by_sina(stock_info['stock_id'], d)
            if s1:
                if float(result['F6_LOW']) <= float(par['input_price'] * (1 + par['s1_stop'])):  # 达到第一次建仓止损
                    s1 = False
                    s2 = True
                    data.append([
                        stock_info['stock_id'],
                        '第一次建仓',
                        '%.2f' % (par['input_price']),  # 买入价格
                        '%.2f' % (par['plan_money'] * par['s1_money']),  # 投入资金
                        '%.2f' % (par['input_price'] * (1 + par['s1_stop'])),  # 清仓价格
                        s1_calc(par)[6],  # 清仓盈利
                        int(d) - int(stock_info['start_date']),  # 持仓天数
                        stock_info['start_date'],  # 买入日期
                        d  # 清仓日期
                    ])
                    return data
                if float(result['F5_HIGH']) >= float(par['input_price'] * (1 + par['s2_signal'])):  # 达到第二次加仓
                    s1 = False
                    s2 = True
                    data.append([
                        stock_info['stock_id'],
                        '第一次建仓',
                        '%.2f' % par['input_price'],  # 买入价格
                        '%.2f' % (par['plan_money'] * par['s1_money']),  # 投入资金
                        '/',  # 清仓价格
                        '/',  # 清仓盈利
                        '/',  # 持仓天数
                        '/',  # 买入日期
                        '/'  # 清仓日期
                    ])
                    d = get_next_day(d)
                    continue
            # 判断是否第二次加仓止损或者达到第三次加仓价格
            if s2 and s1 is False:
                if float(result['F6_LOW']) <= float(par['input_price'] * (1 + par['s2_stop'])):  # 达到第二次加仓止损
                    s2 = False
                    s3 = True
                    data.append([
                        stock_info['stock_id'],
                        '第二次加仓',
                        '%.2f' % (par['input_price'] * (1 + par['s2_signal'])),  # 买入价格
                        '%.2f' % (par['plan_money'] * par['s2_money']),  # 投入资金
                        '%.2f' % (par['input_price'] * (1 + par['s2_stop'])),  # 清仓价格
                        s2_calc(par)[6],  # 清仓盈利
                        int(d) - int(stock_info['start_date']),  # 持仓天数
                        stock_info['start_date'],  # 买入日期
                        d  # 清仓日期
                    ])
                    return data
                if float(result['F5_HIGH']) >= float(par['input_price'] * (1 + par['s3_signal'])):  # 达到第三次加仓
                    s2 = False
                    s3 = True
                    data.append([
                        stock_info['stock_id'],
                        '第二次加仓',
                        '%.2f' % (par['input_price'] * (1 + par['s2_signal'])),  # 买入价格
                        '%.2f' % (par['plan_money'] * par['s2_money']),  # 投入资金
                        '/',  # 清仓价格
                        '/',  # 清仓盈利
                        '/',  # 持仓天数
                        '/',  # 买入日期
                        '/'  # 清仓日期
                    ])
                    d = get_next_day(d)
                    continue
            # 判断是否达到第三次加仓止损或者止盈
            if s3 and not all([s1, s2]):
                if float(result['F6_LOW']) <= float(par['input_price'] * (1 + par['s3_stop'])):  # 达到第三次加仓止损
                    s3 = False
                    data.append([
                        stock_info['stock_id'],
                        '第三次加仓',
                        '%.2f' % (par['input_price'] * (1 + par['s3_signal'])),  # 买入价格
                        '%.2f' % (par['plan_money'] * par['s3_money']),  # 投入资金
                        '%.2f' % (par['input_price'] * (1 + par['s3_stop'])),  # 清仓价格
                        s3_calc(par)[6][0],  # 清仓盈利
                        int(d) - int(stock_info['start_date']),  # 持仓天数
                        stock_info['start_date'],  # 买入日期
                        d  # 清仓日期
                    ])
                    return data
                if float(result['F5_HIGH']) >= float(par['input_price'] * (1 + par['s3_win'])):  # 达到第三次加仓止盈
                    s3 = False
                    data.append([
                        stock_info['stock_id'],
                        '第三次加仓',
                        '%.2f' % (par['input_price'] * (1 + par['s3_signal'])),  # 买入价格
                        '%.2f' % (par['plan_money'] * par['s3_money']),  # 投入资金
                        '%.2f' % (par['input_price'] * (1 + par['s3_win'])),  # 清仓价格
                        s3_calc(par)[6][1],  # 清仓盈利
                        int(d) - int(stock_info['start_date']),  # 持仓天数
                        stock_info['start_date'],  # 买入日期
                        d  # 清仓日期
                    ])
                    return data
            d = get_next_day(d)
        if all([s1, s2, s3]):
            print(f'测试{days}天后，均未触发')


def s_check(par: dict):
    # 校验投资资金总和是否超过总资金
    if par['s1_money'] + par['s2_money'] + par['s3_money'] <= 1:
        return {'success': True, 'message': ''}
    else:
        return {'success': False, 'message': '投入资金占比之和需小于或等于100%'}


def s1_calc(par: dict):
    # 清仓后盈利
    win_money = par['plan_money'] * par['s1_money'] * par['s1_stop']
    return [
        1,
        '第一次（建仓）',
        '%.2f' % (par['input_price']),
        '%.2f' % (par['plan_money'] * par['s1_money']),
        '%.2f' % (par['input_price'] * (1 + par['s1_stop'])),
        '/',
        '%.2f' % win_money
    ]


def s2_calc(par: dict):
    # 清仓后盈利
    win1_money = par['plan_money'] * par['s1_money'] * par['s2_stop']
    win2_money = par['plan_money'] * par['s2_money'] * (par['s2_stop'] - par['s2_signal'])
    return [
        2,
        '第二次（加仓）',
        '%.2f' % (par['input_price'] * (1 + par['s2_signal'])),
        '%.2f' % (par['plan_money'] * par['s2_money']),
        '%.2f' % (par['input_price'] * (1 + par['s2_stop'])),
        '/',
        '%.2f' % (win1_money + win2_money)
    ]


def s3_calc(par: dict):
    # 清仓后盈利（止损）
    a_win1_money = par['plan_money'] * par['s1_money'] * par['s3_stop']
    a_win2_money = par['plan_money'] * par['s2_money'] * (par['s3_stop'] - par['s2_signal'])
    a_win3_money = par['plan_money'] * par['s3_money'] * (par['s3_stop'] - par['s3_signal'])
    # 清仓后盈利（止盈）
    b_win1_money = par['plan_money'] * par['s1_money'] * par['s3_win']
    b_win2_money = par['plan_money'] * par['s2_money'] * (par['s3_win'] - par['s2_signal'])
    b_win3_money = par['plan_money'] * par['s3_money'] * (par['s3_win'] - par['s3_signal'])
    return [
        3,
        '第三次（加仓）',
        '%.2f' % (par['input_price'] * (1 + par['s3_signal'])),
        '%.2f' % (par['plan_money'] * par['s3_money']),
        '%.2f' % (par['input_price'] * (1 + par['s3_stop'])),
        '%.2f' % (par['input_price'] * (1 + par['s3_win'])),
        ('%.2f' % (a_win1_money + a_win2_money + a_win3_money), '%.2f' % (b_win1_money + b_win2_money + b_win3_money))
    ]


def calc(par: dict):
    result = s_check(par)
    if result['success']:
        tb = PrettyTable()
        tb.field_names = ['序号', '交易类型', '买入价格', '买入资金', '止损价格', '止盈价格', '清仓盈利']
        tb.add_rows([
            s1_calc(par),
            s2_calc(par),
            s3_calc(par),
        ])
        print(tb)
    else:
        return print(result['message'])


# if __name__ == '__main__':
#     p_m = {
#         'plan_money': 100000,  # 计划资金（元）
#         'input_price': 1,  # 入场价格
#         # 第一次建仓
#         's1_money': 0.15,  # 投入资金比例
#         's1_stop': -0.05,  # 止损比例
#         # 第二次加仓
#         's2_signal': 0.18,  # 买入信号
#         's2_money': 0.35,  # 投入资金比例
#         's2_stop': 0.15,  # 止损比例
#         # 第三次加仓
#         's3_signal': 0.3,  # 买入信号
#         's3_money': 0.50,  # 投入资金比例
#         's3_stop': 0.25,  # 止损比例
#         's3_win': 0.5  # 止盈比例
#     }
#     calc(p_m)

if __name__ == '__main__':
    ot = Old_Test()
    ot.stock_info = [
        {
            'stock_id': 'sh000630',  # 股票代码
            'plan_money': 100000,  # 计划资金
            'start_price': 3,  # 买入价格（第一次建仓）
            'start_date': '20210720',  # 买入日期（第一次建仓）
            'test_days': 30  # 测试天数
        },
        {
            'stock_id': 'sh600010',  # 股票代码
            'plan_money': 100000,  # 计划资金
            'start_price': 1.8,  # 买入价格（第一次建仓）
            'start_date': '20210709',  # 买入日期（第一次建仓）
            'test_days': 30  # 测试天数
        },
        {
            'stock_id': 'sh000155',  # 股票代码
            'plan_money': 100000,  # 计划资金
            'start_price': 14,  # 买入价格（第一次建仓）
            'start_date': '20210707',  # 买入日期（第一次建仓）
            'test_days': 30  # 测试天数
        }
    ]
    p_m = {
        'plan_money': 100000,  # 计划资金（元）
        'input_price': None,  # 入场价格
        # 第一次建仓
        's1_money': 0.15,  # 投入资金比例
        's1_stop': -0.05,  # 止损比例
        # 第二次加仓
        's2_signal': 0.18,  # 买入信号
        's2_money': 0.35,  # 投入资金比例
        's2_stop': 0.15,  # 止损比例
        # 第三次加仓
        's3_signal': 0.3,  # 买入信号
        's3_money': 0.50,  # 投入资金比例
        's3_stop': 0.25,  # 止损比例
        's3_win': 0.5  # 止盈比例
    }
    data_all = []
    for j in ot.stock_info:
        p_m['input_price'] = j['start_price']
        data = ot.calc_alone(p_m, j)
        data_all += data
        data_all += [['----', '----', '----', '----', '----', '----', '----', '----', '----', ]]
    tb = PrettyTable(['股票ID', '类型', '买入价格', '投入资金', '清仓价格', '清仓盈利', '持仓天数', '买入日期', '清仓日期'])
    tb.add_rows(data_all)
    print(f'\n\n{tb}')
