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
from enum import Enum

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


class EnumPlateType(Enum):
    """
    板块类型
    """
    gai_lian = '概念板块'
    di_yu = '地域板块'
    hang_ye = '行业板块'


class EnumPointerType(Enum):
    """
    指标类型
    """
    RSI = 'RSI'
    KDJ = 'KDJ'
    MACD = 'MACD'
    DMI = 'DMI'
    BIAS = 'BIAS'
    OBV = 'OBV'
    CCI = 'CCI'
    ROC = 'ROC'


class GetMicData:
    """
    微观数据获取
    """

    @staticmethod
    @elapsed_time('新浪接口获取指定股票所有信息')
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
        # print(result.text)
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

    @staticmethod
    @elapsed_time('东方财富获取ETF基金所有数据')
    def get_jj_by_df(etf_id: list = []):
        """
        【东方财富】获取ETF基金所有数据
        界面： http://quote.eastmoney.com/center/gridlist.html#fund_etf
        @param etf_id: 若给值 则返回指定基金的数据 若不给值 则返回沪所有ETF基金的数据
        @return
            [
                {
                    'f14': '基金名称',
                    'f12': '基金代码',
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
                    'f7': '振幅',
                }
            ]
        """
        url = 'http://20.push2.eastmoney.com/api/qt/clist/get?'
        params = {
            "cb": f"jQuery112407586323830979016_{str(time.time() * 1000)}",
            "pn": "1",
            "pz": "100000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "b:MK0021,b:MK0022,b:MK0023,b:MK0024",
            "fields": "f14,f12,f17,f15,f16,f350,f351,f3,f4,f18,f10,f8,f5,f6,f7",
            "_": str(time.time() * 1000)
        }
        result = requests.get(url, params=params).content.decode('utf-8')
        result = jx_jquery_result(result)
        if len(result['data']['diff']) == result['data']['total']:
            print(f"所有ETF基金数据获取完成：{len(result['data']['diff'])}条")
        else:
            print(f"所有ETF基金数据获取不全：预期{result['data']['total']}条，实际{len(result['data']['diff'])}条")
        result_list = result['data']['diff']
        result_new = []
        if len(etf_id) != 0:
            for i in etf_id:
                for j in result_list:
                    if j['f12'] == i:
                        result_new.append(j)
            return result_new
        return result_list

    @staticmethod
    def get_image(pointer_type=EnumPointerType.MACD):
        """
        获取近3个月指定股票的K线即指标图
        @param pointer_type: 指标类型
        """
        url = 'http://webquoteklinepic.eastmoney.com/GetPic.aspx?'
        params = {
            "token": "44c9d251add88e27b65ed86506f6e5da",
            "nid": "1.510120",
            "type": "",
            "unitWidth": "-6",
            "ef": "",
            "formula": pointer_type.value,  # RSI、KDJ、MACD
            "imageType": "KXL"
        }
        result = requests.get(url, params=params).content
        with open('a.png', 'wb') as f:
            f.write(result)


class GetMacData:
    """
    宏观数据获取
    """

    @staticmethod
    def get_plate_data(plate_type=EnumPlateType.gai_lian):
        """
        获取板块数据
        @param plate_type: 概念板块plate_type=PlateType.gai_lian，地域板块plate_type=PlateType.di_yu，行业板块plate_type=PlateType.hang_ye
        @return:
            [
                {
                    'f1': '',
                    'f2': '最新价',
                    'f3': '涨跌幅',
                    'f4': '涨跌额',
                    'f5': '',
                    'f6': '',
                    'f7': '',
                    'f8': '换手率',
                    'f9': '',
                    'f10': '',
                    'f12': '',
                    'f13': '',
                    'f14': '板块名称',
                    'f15': '',
                    'f16': '',
                    'f17': '',
                    'f18': '',
                    'f20': '总市值',
                    'f21': '',
                    'f23': '',
                    'f24': '',
                    'f25': '',
                    'f26': '',
                    'f22': '',
                    'f33': '',
                    'f11': '',
                    'f62': '',
                    'f128': '领涨股票',
                    'f136': '领涨股票涨跌幅',
                    'f115': '',
                    'f152': '',
                    'f124': '',
                    'f107': '',
                    'f104': '上涨家数',
                    'f105': '下跌家数',
                    'f140': '',
                    'f141': '',
                    'f207': '',
                    'f208': '',
                    'f209': '',
                    'f222': ''
                }
            ]
        """
        hang_ye_url = 'http://81.push2.eastmoney.com/api/qt/clist/get?'
        hang_ye_params = {
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
        gai_lian_url = 'http://30.push2.eastmoney.com/api/qt/clist/get?'
        gai_lian_params = {
            "cb": "jQuery11240752172781178722_1626791176577",
            "pn": "1",
            "pz": "10000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:90+t:3+f:!50",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222",
            "_": "1626791176680"
        }
        di_yu_url = 'http://30.push2.eastmoney.com/api/qt/clist/get?'
        di_yu_params = {
            "cb": "jQuery11240752172781178722_1626791176575",
            "pn": "1",
            "pz": "10000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:90+t:1+f:!50",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222",
            "_": "1626791176711"
        }

        if plate_type == EnumPlateType.gai_lian:
            url = gai_lian_url
            params = gai_lian_params
            name = EnumPlateType.gai_lian.value
        elif plate_type == EnumPlateType.hang_ye:
            url = hang_ye_url
            params = hang_ye_params
            name = EnumPlateType.hang_ye.value
        elif plate_type == EnumPlateType.di_yu:
            url = di_yu_url
            params = di_yu_params
            name = EnumPlateType.di_yu.value
        result = requests.get(url, params=params).content.decode('utf-8')
        result = jx_jquery_result(result)
        result = result['data']
        if result["total"] == len(result["diff"]):
            print(f'{name}数据已全部获取：{result["total"]}条')
        else:
            print(f'{name}数据获取不全：预期{result["total"]}条，实际{len(result["diff"])}条')
        dddd = [
            {
                'f1': '',
                'f2': '最新价',
                'f3': '涨跌幅',
                'f4': '涨跌额',
                'f5': '',
                'f6': '',
                'f7': '',
                'f8': '换手率',
                'f9': '',
                'f10': '',
                'f12': '',
                'f13': '',
                'f14': '板块名称',
                'f15': '',
                'f16': '',
                'f17': '',
                'f18': '',
                'f20': '总市值',
                'f21': '',
                'f23': '',
                'f24': '',
                'f25': '',
                'f26': '',
                'f22': '',
                'f33': '',
                'f11': '',
                'f62': '',
                'f128': '领涨股票',
                'f136': '领涨股票涨跌幅',
                'f115': '',
                'f152': '',
                'f124': '',
                'f107': '',
                'f104': '上涨家数',
                'f105': '下跌家数',
                'f140': '',
                'f141': '',
                'f207': '',
                'f208': '',
                'f209': '',
                'f222': ''
            }
        ]

        return result['diff']


if __name__ == '__main__':
    result = GetMicData.get_alone_data_by_sina('sh600010', '20210716', True)  # ['301027', '600010'] 301027
    # result = GetMicData.get_alone_data_by_df(['600010'])
    # print(*result, sep='\n')
    # print(*GetMicData.get_jj_by_df(['512670', '515030', '159755']), sep='\n')
    # GetMicData.get_image(pointer_type=EnumPointerType.CCI)
    # GetMacData.get_plate_data(PlateType.gai_lian)
    # print(*GetMacData.get_plate_data(PlateType.di_yu), sep='\n')
    # GetMacData.get_plate_data(PlateType.hang_ye)
