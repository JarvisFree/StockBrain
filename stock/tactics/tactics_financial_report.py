#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/10 8:51
@Author  ：维斯
@File    ：tactics_financial_report.py
@Version ：1.0
@Function：财务报告策略

主要是校验财务报告公布后股价的走势
4个财报：第一季度、半年、第三季度、年报
"""
import datetime
import json
import random
import re
import time

import requests
import tushare
from pyutilitytool.tool_excel import PyUtilExcel

from stock.AIOldDataServer import AIOldDataServer
from stock.GetStockDataServer import GetStockDataServer
from stock.comon.jx_jquery_result import jx_jquery_result


def __get_report(stock_id, index):
    # 单页最大只能获取100个 需要循环获取
    url = 'http://np-anotice-stock.eastmoney.com/api/security/ann?'
    params = {
        "ann_type": "A",
        "cb": "jQuery112308833717395319984_1625877631269",
        "client_source": "web",
        "f_node": "1",
        "page_index": str(index),
        "page_size": "1000",
        "s_node": "1",
        "sr": "-1",
        "stock_list": stock_id
    }
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "qgqp_b_id=c256402d8ed5580dd7c9143757f4ae4a; em_hq_fls=js; emshistory=%5B%22%E6%B1%9F%E4%B8%B0%E7%94%B5%E5%AD%90(300666)%22%2C%22%E6%81%92%E7%8E%84%E7%A7%91%E6%8A%80%22%5D; st_si=08409951526361; em-quote-version=topspeed; cowCookie=true; intellpositionL=1186.4px; HAList=a-sh-600010-%u5305%u94A2%u80A1%u4EFD%2Ca-sh-600519-%u8D35%u5DDE%u8305%u53F0%2Ca-sh-600096-%u4E91%u5929%u5316%2Ca-sz-300131-%u82F1%u5510%u667A%u63A7%2Ca-sz-300274-%u9633%u5149%u7535%u6E90; cowminicookie=true; st_asi=delete; st_pvi=56381201324798; st_sp=2021-05-20%2010%3A20%3A43; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=61; st_psi=2021071008462741-111000300841-1665689519; intellpositionT=2451px",
        "Host": "np-anotice-stock.eastmoney.com",
        "Pragma": "no-cache",
        "Referer": "http://data.eastmoney.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    result = requests.get(url=url, params=params, headers=header).content.decode('utf-8')
    # print(result)
    result = jx_jquery_result(result)
    return result


def __get_report_alone(stock_id):
    index = 1
    data_list = []
    result = __get_report(stock_id, index)
    data_list += result['data']['list']
    all_count = int(result['data']['total_hits'])
    while True:
        if len(data_list) != all_count:
            index += 1
            data_list += __get_report(stock_id, index)['data']['list']
        else:
            break
    print(f'预期：{all_count}个，实际：{len(data_list)}')
    return data_list


def get_all_report(stock_id='600010'):
    """
    返回示例：
    {
        "2021":{
            "第1季度":[
                [
                    "2021-04-30",
                    "600010:包钢股份2021年一季度报告"
                ]
            ]
        },
        "2020":{
            "第4季度":[
                [
                    "2021-04-30",
                    "600010:包钢股份2020年年度报告"
                ]
            ],
            "第3季度":[
                [
                    "2020-10-30",
                    "600010:包钢股份2020年第三季度报告正文"
                ]
            ],
            "第2季度":[
                [
                    "2020-08-31",
                    "600010:包钢股份2020年半年度报告"
                ]
            ],
            "第1季度":[
                [
                    "2020-04-30",
                    "600010:包钢股份2020年第一季度报告"
                ]
            ]
        }
    }
    """
    data = __get_report_alone(stock_id)
    now_year = time.strftime('%Y')
    new_data = []
    while True:
        n_data = []
        is_have = False
        for i in data:
            if i["title"].find('摘要') == -1:  # 1 删除含“摘要”的
                res = re.search('\D\d{4}\D', i["title"])
                if res is not None:
                    if res.group()[1:-1] == str(now_year):
                        aa = re.search("(\d{4}-\d{2}-\d{2})", i["notice_date"]).group()
                        print(f'{aa} ,  {i["title"]}')
                        n_data.append((aa, i["title"],))
                        is_have = True
        if not is_have:
            break
        nn_data = {now_year: n_data}
        now_year = str(int(now_year) - 1)
        new_data.append(nn_data)
    year_all = {}

    for i in new_data:
        i_ll = list(i.items())[0]

        year_alone = {}
        for j in i_ll[1]:  # 循环某一年
            # 第一季度（关键字：一）
            key_1 = ['一']
            # 第二季度（关键字：二、半、中）
            key_2 = ['二', '半', '中']
            # 第三季度（关键字：三）
            key_3 = ['三']
            # 第四季度（关键字：年年度）
            key_4 = ['年年度', '年年报', '年度报告']
            # 汇总
            key_all = [key_1, key_2, key_3, key_4]
            for key in key_all:
                j_da = []
                if any(have in j[1] for have in key):
                    j_da.append(j)
                    # 判断是否已有（若有 则用时间最近的那个）
                    if year_alone.get(f'第{key_all.index(key) + 1}季度') is not None and \
                            year_alone.get(f'第{key_all.index(key) + 1}季度')[0][0] >= j_da[0][0]:
                        pass
                    else:
                        year_alone.update({f'第{key_all.index(key) + 1}季度': j_da})
        # 去重

        year_all.update({f'{i_ll[0]}': year_alone})

    # print(*new_data, sep='\n')
    print('\r\n\r\n')
    print(json.dumps(year_all, ensure_ascii=False))
    return year_all


def get_jia_ge(stock_id: str, date: str, count: int):
    """
    @param stock_id: 股票ID（‘sh600010’）
    @param date: '20210709'
    @param count: 未来几个（含）交易日 （7）
    """

    def calc_date(date_s):
        # 时间加减
        # 将时间字符串转换为 datetime 格式的时间
        today = datetime.datetime.strptime(date_s, '%Y%m%d')
        # 计算偏移量
        offset = datetime.timedelta(days=+1)
        # 获取修改后的时间并格式化
        re_date = (today + offset).strftime('%Y%m%d')
        print(re_date)  # 2020-11-15 19:48:51
        return re_date

    c = 0
    a_d = []
    while True:
        if c == count or datetime.datetime.now().strftime('%Y%m%d') < date: break
        close = GetStockDataServer().get6_close_by_id_and_date([stock_id], [''], [date])[0]['data'][date]
        if len(close) != 0:
            a_d.append([date, close])
            c += 1
        date = calc_date(date)
    return a_d


if __name__ == '__main__':
    s_time = datetime.datetime.now()
    stock_id = '600010'
    stock_id_xl = 'sh600010'
    count = 5
    result = get_all_report(stock_id)
    for k, v in result.items():
        cc_model = ['第1季度', '第2季度', '第3季度', '第4季度']
        try:
            for i in cc_model:
                date_s = v.get(i)[0][0]
                date_s = ''.join(date_s.split('-'))
                # print(date_s)
                result_close = get_jia_ge(stock_id_xl, date_s, count)
                v.get(i).append(result_close)
        except:
            pass
    # print(*get_jia_ge(stock_id_xl, '20210701', 100), sep='\n')
    print(json.dumps(result, ensure_ascii=False))

    # 写入excel
    header_list = [
        ['财报项'],  # 表格第0列[此列表头名称]
        ['公布时间'],
    ]
    for h_i in range(count):
        header_list.append([f'T+{h_i}'])
    header_list.append([f'{count}日后涨幅'])
    header_list.append(['备注'])
    data_body = []
    c_model = ['第4季度', '第3季度', '第2季度', '第1季度']
    for k, v in result.items():
        for i in c_model:
            try:
                v.get(i)
                d_b = [f'{k}年{i}']
                d_b.append(f'{v.get(i)[0][0]}')
                note = ''
                s_close = ''
                e_close = ''
                for c_i in range(count):
                    if c_i == 0: s_close = v.get(i)[1][c_i][1]
                    if c_i == count - 1: e_close = v.get(i)[1][c_i][1]
                    d_b.append(f'{v.get(i)[1][c_i][1]}')  # T+0 ... T+n
                    note += v.get(i)[1][c_i][0] + ','
                c_close = str(float('%.2f' % float((float(e_close) - float(s_close)) / float(s_close) * 100))) + '%'
                d_b.append(c_close)
                d_b.append(note)
                data_body.append(d_b)
            except:
                pass
    PyUtilExcel(header_list).write(f'财报公布后的价格走势_{stock_id_xl}.xlsx', data_body, '财报公布后的价格走势')
    print(f'耗时：{datetime.datetime.now() - s_time}')
