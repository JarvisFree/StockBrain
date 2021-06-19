#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/4/13 12:58
@Author  ：维斯
@File    ：stock_base_data.py
@Version ：1.0
@Function：股票相关基础数据
"""

import time

import requests
from stock.comon.jx_jquery_result import jx_jquery_result

base = {
    'f1': '',
    'f2': '最新价',  # 如31.42，则此字段为：31.42
    'f3': '涨幅',  # 如3.89%，则此字段为：3.89
    'f4': '',
    'f5': '',
    'f6': '',
    'f7': '振幅',  # 如5.36%，则此字段为：5.36
    'f8': '换手率',  # 如3.73%，则此字段为：3.72
    'f9': '市盈率',  # 如9.26，则此字段为：9.26
    'f10': '量比',  # 如1.76，则此字段为：1.76
    'f12': '',
    'f13': '',
    'f14': '',
    'f15': '',
    'f16': '',
    'f17': '',
    'f18': '昨收',  # 如31.3，则此字段为：31.3
    'f20': '',
    'f21': '流通市值',  # 如50亿，则此字段为：5000000000 （备注：此字段有可能为“-”）
    'f23': '市净率',  # 如9.26，则此字段为：9.26
    'f24': '60日涨跌幅',  # 如24.34%，则此字段为：24.34
    'f25': '',
    'f26': '',
    'f22': '',
    'f33': '',
    'f11': '',
    'f62': '',
    'f128': '',
    'f136': '',
    'f115': '',
    'f152': '',
    'f124': '',
    'f107': '',
    'f104': '',
    'f105': '',
    'f140': '',
    'f141': '',
    'f207': '',
    'f208': '',
    'f209': '',
    'f222': ''
}


def get_hang_ye():
    """
    获取行业板块数据
    """
    url = 'http://81.push2.eastmoney.com/api/qt/clist/get?'
    params = {
        "cb": "jQuery112408297466168838283_1620571811003",
        "pn": "1",
        "pz": "10000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:90+t:2+f:!50",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222",
        "_": "1620571811004"
    }
    result = requests.get(url, params=params).content.decode('utf-8')
    result = jx_jquery_result(result)
    # print(result)
    result = result['data']
    if result["total"] == len(result["diff"]):
        print(f'行业数据已全部获取：{result["total"]}条')
    else:
        print(f'行业数据获取不全：预期{result["total"]}条，实际{len(result["diff"])}条')
    return result


def get_a_all_stock():
    """
    获取沪深A股所有股票（预计：4488只 21.5.27日统计）
    :return:
    """
    url = 'http://35.push2.eastmoney.com/api/qt/clist/get?'
    params = {
        "cb": f"jQuery112408618214212067554_{str(int(time.time() * 1000))}",
        "pn": "1",  # 第n页
        "pz": "6000",  # 每页数量
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": str(int(time.time() * 1000))
    }
    result = requests.get(url, params=params).content.decode('utf-8')
    result = jx_jquery_result(result)
    result = result['data']
    if result["total"] == len(result["diff"]):
        print(f'沪深A股所有股票已全部获取：{result["total"]}条')
    else:
        print(f'沪深A股股票数据获取不全：预期{result["total"]}条，实际{len(result["diff"])}条')
    return result


if __name__ == '__main__':
    # get_hang_ye()
    get_a_all_stock()
