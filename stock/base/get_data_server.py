#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/17 18:24
@Author  ：维斯
@File    ：get_data_server.py
@Version ：1.0
@Function：股票数据获取服务（以后以这个为准了）
"""
import json
import time

import requests

from stock.comon.decorator import elapsed_time
from stock.comon.jx_jquery_result import jx_jquery_result


class DataSet:
    F0_DATE = 'F0_DATE'  # 日期
    F1_STOCK_ID = 'F1_STOCK_ID'  # 股票ID
    F2_STOCK_NAME = 'F2_STOCK_NAME'  # 股票名称
    F3_OPEN = 'F3_OPEN'  # 开盘价
    F4_CLOSE = 'F4_CLOSE'  # 收盘价
    F5_HIGH = 'F5_HIGH'  # 最高价
    F6_LOW = 'F6_LOW'  # 最低价
    F7_CHG = 'F7_CHG'  # 涨跌额
    F8_P_CHG = 'F8_P_CHG'  # 涨跌幅
    F9_TURNOVER = 'F9_TURNOVER'  # 换手率
    F10_VO_TURNOVER = 'F10_VO_TURNOVER'  # 成交量
    F11_VA_TURNOVER = 'F11_VA_TURNOVER'  # 成交金额
    F12_T_CAP = 'F12_T_CAP'  # 总市值
    F13_M_CAP = 'F13_M_CAP'  # 流通市值


class GetMicData:
    """
    微观数据获取
    """

    @staticmethod
    @elapsed_time('新浪接口获取股票所有信息')
    def get_alone_data_by_sina(stock_id, date, is_print=False):
        """
        【新浪财经】获取指定股票指定交易日的所有信息
        备注：1、量比数据获取；2、振幅数据获取
        :param stock_id: 股票代码（如包钢股份：sh600010）
        :param date: 指定日期（格式：yyyymmdd）
        :param is_print:
        :return:
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
        # 判断传入的代码是否是字母加数字（如 sz002415）
        if stock_id.isalnum():
            stock_id = stock_id[2:]
        # 如果股票代码首位是0或者3则需添加一个1，反之则需添加一个0
        if stock_id[0] == "0" or stock_id[0] == "3":
            stock_id = "1" + stock_id
        else:
            stock_id = "0" + stock_id
        url = "http://quotes.money.163.com/service/chddata.html?"
        params = {
            "code": stock_id,
            "end": date,
            "fields": "TOPEN;TCLOSE;HIGH;LOW;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP",
            "start": date
        }
        result = requests.get(url, params=params)
        print(result.text)
        result = result.text.split("\r\n")[1].split(",")
        result_json = {
            DataSet.F0_DATE: result[0],
            DataSet.F1_STOCK_ID: result[1],
            DataSet.F2_STOCK_NAME: result[2],
            DataSet.F3_OPEN: result[3],
            DataSet.F4_CLOSE: result[4],
            DataSet.F5_HIGH: result[5],
            DataSet.F6_LOW: result[6],
            DataSet.F7_CHG: result[7],
            DataSet.F8_P_CHG: result[8],
            DataSet.F9_TURNOVER: result[9],
            DataSet.F10_VO_TURNOVER: result[10],
            DataSet.F11_VA_TURNOVER: result[11],
            DataSet.F12_T_CAP: result[12],
            DataSet.F13_M_CAP: result[13],
        }

        if is_print:
            print(
                "[{}] {}股票在 {} 的所有数据为：{}".format(GetMicData.__name__ + '.' + GetMicData.get_alone_data_by_sina.__name__,
                                                 stock_id[1:],
                                                 date, json.dumps(result_json, ensure_ascii=False)))
        return result_json

    @staticmethod
    @elapsed_time('东方财富获取股票所有数据')
    def get_alone_data_by_df(stock_id: list = []):
        """
        【东方财富】获取沪深A股所有股票（数据很全 可以获取很多参数 比如到f500 但耗时较长 获取f1-f500 大概需要14s左右）
        @param stock_id: 若给值 则返回指定股票的数据 若不给值 则返回沪深A股所有股票的数据
        @return:
            [
                {
                    'f14': '股票名称',
                    'f12': '股票代码',
                    'f17': '开盘价',
                    'f15': '最高价',
                    'f16': '最低价',
                    'f350': '涨停价',
                    'f351': '跌停价',
                    'f3': '涨跌幅',
                    'f4': '涨跌额',
                    'f18': '上一个交易日收盘价',
                    'f10': '量比',
                    'f8': '换手率',
                    'f5': '成交量',
                    'f6': '成交金额',
                    'f20': '总市值',
                    'f21': '流通市值',
                    'f9': '动态市盈率',
                    'f114': '静态市盈率',
                    'f115': '滚动市盈率',
                    'f7': '振幅',
                }
            ]

        """
        url = 'http://35.push2.eastmoney.com/api/qt/clist/get?'
        params = {
            "cb": f"jQuery112408618214212067554_{str(int(time.time() * 1000))}",
            "pn": "1",  # 第n页
            "pz": "8000",  # 每页数量
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
            # "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100,f101,f102,f103,f104,f105,f106,f107,f108,f109,f110,f111,f112,f113,f114,f115,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203,f204,f205,f206,f207,f208,f209,f210,f211,f212,f213,f214,f215,f216,f217,f218,f219,f220,f221,f222,f223,f224,f225,f226,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f243,f244,f245,f246,f247,f248,f249,f250,f251,f252,f253,f254,f255,f256,f257,f258,f259,f260,f261,f262,f263,f264,f265,f266,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f277,f278,f279,f280,f281,f282,f283,f284,f285,f286,f287,f288,f289,f290,f291,f292,f293,f294,f295,f296,f297,f298,f299,f300,f301,f302,f303,f304,f305,f306,f307,f308,f309,f310,f311,f312,f313,f314,f315,f316,f317,f318,f319,f320,f321,f322,f323,f324,f325,f326,f327,f328,f329,f330,f331,f332,f333,f334,f335,f336,f337,f338,f339,f340,f341,f342,f343,f344,f345,f346,f347,f348,f349,f350,f351,f352,f353,f354,f355,f356,f357,f358,f359,f360,f361,f362,f363,f364,f365,f366,f367,f368,f369,f370,f371,f372,f373,f374,f375,f376,f377,f378,f379,f380,f381,f382,f383,f384,f385,f386,f387,f388,f389,f390,f391,f392,f393,f394,f395,f396,f397,f398,f399,f400,f401,f402,f403,f404,f405,f406,f407,f408,f409,f410,f411,f412,f413,f414,f415,f416,f417,f418,f419,f420,f421,f422,f423,f424,f425,f426,f427,f428,f429,f430,f431,f432,f433,f434,f435,f436,f437,f438,f439,f440,f441,f442,f443,f444,f445,f446,f447,f448,f449,f450,f451,f452,f453,f454,f455,f456,f457,f458,f459,f460,f461,f462,f463,f464,f465,f466,f467,f468,f469,f470,f471,f472,f473,f474,f475,f476,f477,f478,f479,f480,f481,f482,f483,f484,f485,f486,f487,f488,f489,f490,f491,f492,f493,f494,f495,f496,f497,f498,f499,f500",
            "fields": "f14,f12,f17,f15,f16,f350,f351,f3,f4,f18,f10,f8,f5,f6,f20,f21,f9,f114,f115,f7",
            "_": str(int(time.time() * 1000))
        }
        result = requests.get(url, params=params).content.decode('utf-8')
        result = jx_jquery_result(result)
        result = result['data']
        data_alone = []
        if result["total"] == len(result["diff"]):
            print(f'沪深A股所有股票已全部获取：{result["total"]}条')
            if len(stock_id) != 0:
                for j in stock_id:
                    for i in result['diff']:
                        if j == i['f12']:
                            data_alone.append(i)
                            break
            else:
                data_alone = result
        else:
            print(f'沪深A股股票数据获取不全：预期{result["total"]}条，实际{len(result["diff"])}条')
        return data_alone


class GetMacData:
    """
    宏观数据获取
    """

    def __init__(self):
        pass


if __name__ == '__main__':
    # result = GetMicData.get_alone_data_by_sina('sh600010', '20210716', True)  # ['301027', '600010'] 301027
    result = GetMicData.get_alone_data_by_df(['600010'])
    print(*result, sep='\n')
