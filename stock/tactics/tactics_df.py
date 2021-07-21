#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/11 16:20
@Author  ：维斯
@File    ：tactics_df.py
@Version ：1.0
@Function：东风策略
    解说：
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


# TODO：P0优先级最高 先搞这个【找出某个股的所有信号股】
def zh_yao():
    def signal_stock(all_stock_list: list):
        stock_set = set(all_stock_list)
        data = []
        for a in stock_set:
            data.append({'name': a, 'count': all_stock_list.count(a)})
        da = sorted(data, key=lambda e: e.__getitem__('count'), reverse=True)
        print(*da, sep='\n')
        return da

    bg_list = '获取包钢股份历史触发过涨停的日期list（bg_list）'
    all_stock = []
    for bgi in bg_list:  # 循环每个日期
        for i in '获取包钢股份在此日涨停时_其他股票在此日/上一个交易日/上上一个交易日(优先级：此日 —> 上一个交易日 —> 上上一个交易日)也涨停的股票list（包含股票代码、股票名称、触发时间）':
            if i['涨停时间(年到秒)'] == '在包钢股份上涨前':
                all_stock.append('在包钢股份上涨前就上涨的股票')
    signal_stock(all_stock)  # 直接调用即可 '找出all_stock二维列表里共有的股票名称，基本就是包钢股份上涨前的信号股票。并给出信号股票出现的次数'
    pass


# if __name__ == '__main__':
#     s_time = datetime.datetime.now()
#     start()
#     print(f'耗时：{datetime.datetime.now() - s_time}')

if __name__ == '__main__':
    """
    问题：找出字符串中重复出现的字符 并求出重复次数 且根据重复次数从大到小排列
    """
    s_time = time.time()
    str_old = '13678432785623904839372284623785123190380192381290765387'
    str_list = list(str_old)  # 将字符串按照单个字符分割成列表
    str_set = set(str_list)  # 对列表去重
    new_list = []
    for i in str_set:
        new_list.append({'key': i, 'value': str_list.count(i)})  # 循环查找某字符出现的次数
    data = sorted(new_list, key=lambda e: e.__getitem__('value'), reverse=True)  # 根据重复次数从大到小排列
    print(*data, sep='\n')
    print(f'耗时：{(time.time()-s_time)*1000000}')
