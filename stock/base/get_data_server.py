#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/17 18:24
@Author  ：维斯
@File    ：get_data_server.py
@Version ：1.0
@Function：股票数据获取服务（以后以这个为准了）
"""
import datetime
import json
import time
from enum import Enum

import requests
from stock.comon.decorator import elapsed_time
from stock.comon.jx_jquery_result import jx_jquery_result
from stock.comon.stock_tool import get_last_day, is_trading, is_trading_by_db


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

    @staticmethod
    def continue_up(stock_id, count: int, start_date: str, check_type: int):
        """
        获取指定股票N个交易日内持续上升的数据
                第一种：可以通过 T+1的最高价 > T+0的开盘价来计算 或者
                第二种：可以通过 T+1的最高价 > T+0的最低价来计算
        @param stock_id: 'sh600010'
        @param count: N个交易日（不含开始日期 依次往前算）
        @param start_date: 'yyyymmdd'，开始计算的日期
        @param check_type:
            1:第一种情况
            2:第二种情况
            1008601:两种情况都满足
            1008602:两种情况满足任意一个
        @return: 上升：股票数据，非上升：None
        """
        result_list = []
        while True:
            if is_trading_by_db(start_date):
                break
            else:
                start_date = get_last_day(start_date)

        for i in range(count):
            result_list.append(GetMicData.get_alone_data_by_sina(stock_id, start_date))
            start_date = get_last_day(start_date)
        # 判断是否是持续上升
        check_data = []
        # 第一种：后一天最高价 > 前一天开盘价
        if all(float(result_list[i]['F5_HIGH']) > float(result_list[i + 1]['F6_LOW']) for i in range(count - 1)):
            check_data.append(True)
        else:
            check_data.append(False)
        # 第二种：后一天最高价 > 前一天最低价
        if all(float(result_list[i]['F5_HIGH']) > float(result_list[i + 1]['F3_OPEN']) for i in range(count - 1)):
            check_data.append(True)
        else:
            check_data.append(False)

        if check_type == 1:
            if not check_data[int(check_type) - 1]: return None
        if check_type == 2:
            if not check_data[int(check_type) - 1]: return None
        if check_type == 1008601:  # 两种情况都满足
            if not all(i for i in check_data): return None
        if check_type == 1008602:  # 两种情况满足任意一个
            if not any(i for i in check_data): return None
        return result_list


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


class MonitorData:
    """
    数据监测
    """

    @staticmethod
    def monitor_price(stock_id):
        """
        实时监测个股当前价格
        @param stock_id: sh600010
        @return ['2021-07-29 11:19:29', '2.65']
        """
        if stock_id.startswith('sh'):
            stock_id = '1.' + stock_id.split('sh')[1]
        elif stock_id.startswith('sz'):
            stock_id = '0.' + stock_id.split('sz')[1]  # TODO:是不是0.开头的 待验证

        url = 'http://push2.eastmoney.com/api/qt/stock/details/get?'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "qgqp_b_id=a40cb88318829a05d29c3a8f50f9ec5a; cowCookie=true; intellpositionL=1186.4px; cowminicookie=true; intellpositionT=1674.5px; st_si=57885261691163; st_asi=delete; HAList=a-sh-600010-%u5305%u94A2%u80A1%u4EFD; em_hq_fls=js; st_pvi=23952558447054; st_sp=2021-07-27%2012%3A41%3A01; st_inirUrl=http%3A%2F%2Fquote.eastmoney.com%2Fcenter%2F; st_sn=6; st_psi=20210729103812783-113200301201-5894193723",
            "Host": "push2.eastmoney.com",
            "Pragma": "no-cache",
            "Referer": "http://quote.eastmoney.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        params = {
            "_": int(time.time() * 1000),
            "cb": f"jQuery112403702002849848167_{int(time.time() * 1000)}",
            "fields1": "f1,f2,f3,f4",
            "fields2": "f51,f52,f53,f54,f55",
            "pos": "-11",
            "secid": stock_id,
            "ut": "fa5fd1943c7b386f172d6893dbfba10b"
        }
        result = requests.get(url, headers=headers, params=params).text
        result = jx_jquery_result(result)
        result = result['data']['details']
        result = result[len(result) - 1].split(',')
        result_price = [
            datetime.datetime.now().strftime('%Y-%m-%d ') + result[0],
            result[1]
        ]
        print(result_price)
        return result_price


# if __name__ == '__main__':
#     for i in range(10):
#         MonitorData.monitor_price('sh600010')
#         time.sleep(5)

if __name__ == '__main__':
    url = 'https://bizapi.csdn.net/mp/live-message/v1.0/message/send'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "authority": "bizapi.csdn.net",
        "cache-control": "no-cache",
        "content-length": "144",
        "content-type": "application/json",
        "cookie": "uuid_tt_dd=10_19720473180-1627373583585-596830; ssxmod_itna=eqAx0DyDgiDtyDBPrtD9Dmxxfxw6DuCEneh2e=D0y0FeGzDAxn40iDtP=M778G62iqef443aiqjQ0maba=9iWONQrDCPGnDBKYLpDen=D5xGoDPxDeDADYE6DAqiOD7qDdEsNv/8DbxYpnDA3Di4D+bkQDmqG0DDU7R4G2D7UnQQdPpTbBD20xKY=DjwbD/8wb=Y=5=Paq0uiNx1K=D0PQQA9x7f9KYhGVWOQDzk7DtwtgRkdoLp=ZfMNTYiPQYY+f3xmf5DhsYExhIDWq9YfNiY4rjixiQDebCr+zI5DA9a+L5iD===; ssxmod_itna2=eqAx0DyDgiDtyDBPrtD9Dmxxfxw6DuCEneh2DnKS0FYDsqKK7DL7OQiyn77xTvMRNqDrBfK2xKupCo6m=KbqqYEjjb0abGkm+2GcAQvSkQIxzr5mLyAkZ76M9LI1IjluE96xzlK0Dnb=DUxieCwdD44=DfDkeRAwPmYxr/7pD8hhot7=32owP3mGQSErDIw+Pp7fzSqfQKmrerSv0FMLqUBvnUMEEKmNnFoXpUS6UR3w/fajDojuPqLnR9lniNZXrNLu7YHyUgjPX8K7nKeaFvuKa1t=5ACbsN=Y75W4fkqggh2qgqbFCyPGqGiG=ArZiDNBmvmWWiP29cL3e2tap7KGUBw80xX4mecLfmAS4mY9LneYTe3sI3c22FmoxacI92Kw6FuAjE9Y+K+5465=9iBGPCeBl4+4W9nt3d=8/U+DLR6R2HlgDm8LFpDy5r6D3D07kDxqYE2i5v738YAw6jgAxAcqKQefhY=GqxaxcGDk7D=i=UZUkYXTODqDDLxD2QGDD===; UserName=qq_36179095; UserInfo=f917fb152cb14c6d8fc68b6d1dec8518; UserToken=f917fb152cb14c6d8fc68b6d1dec8518; UserNick=%E6%B7%A1%E6%80%80; AU=1FF; UN=qq_36179095; BT=1627522752497; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22qq_36179095%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_19720473180-1627373583585-596830!5744*1*qq_36179095; __gads=ID=09bc964720a52d60-22db345b96ca0064:T=1627642972:RT=1627642972:S=ALNI_MbvNhbZ0-K7nxGeGq_azRIiMroXPg; c_first_ref=www.baidu.com; c_first_page=https%3A//www.csdn.net/; c_segment=14; c_page_id=default; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1627642947,1627642971,1627645793,1627708346; dc_sid=5496098cd0be538a7d0e5b4f6d66f031; log_Id_click=15; log_Id_view=81; c_ref=https%3A//live.csdn.net/%3Fspm%3D1000.2115.3001.4124; c_pref=https%3A//www.csdn.net/; dc_tos=qx3ftl; log_Id_pv=32; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1627708378; dc_session_id=10_1627710584016.410564",
        "method": "POST",
        "origin": "https://live.csdn.net",
        "path": "/mp/live-message/v1.0/message/send",
        "pragma": "no-cache",
        "referer": "https://live.csdn.net/room/harmonycommunity/cnBKxjag",
        "scheme": "https",
        "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "x-app-id": "CSDN-LIVE-PC",
        "x-ca-key": "203801083",
        "x-ca-nonce": "eb287b9a-bf62-461e-88d8-827f4d2a72cb",
        "x-ca-signature": "PWoafVZJ0cJtXdulg2OkAMcvEIXaKL2cmFpA7w6ggT8=",
        "x-ca-signature-headers": "x-ca-key,x-ca-nonce",
        "x-device-id": "10_19720473180-1627373583585-596830"
    }

    params = {"username": "qq_36179095", "liveId": "cnBKxjag", "message": "HarmonyOS 有奖征文大赛aaaaaaaaaaaaaaaaaaaa",
              "anchorId": "harmonycommunity", "image": "", "platform": "pc"}
    print(requests.post(url, params=params).text)
