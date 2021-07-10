#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2019-10-23 22:27
@Author  ：维斯
@File    ：GetStockDataServer.py
@Version ：1.0
@Function：获取股票数据服务
"""

import requests
import json
import ast
import demjson
import datetime

"""
从新浪获取的数据
"""


class GetStockDataServer:
    stock_count_get3 = 0
    stock_id_get3 = ""

    @staticmethod
    def get1_stock_all_data_by_id(stock_id):
        """
        功能1：获取指定股票所有信息
        :return:返回此股票所有数据（列表）
        """
        url = "http://hq.sinajs.cn/list=" + stock_id
        result = requests.get(url).text
        # print(result)

        # 截取引号中的字符串 放入一个列表中
        result = result[result.find('="') + 2:-3]
        # print(result)
        result_list = result.split(",")
        print(result_list)
        return result_list

    @staticmethod
    def get2_stock_all_data_by_id_and_date(stock_id, date):
        """
        功能2：获取指定股票指定交易日的所有信息
        :param stock_id: 股票代码
        :param date: 指定日期（格式：yyyymmdd）
        :return: 返回此股票指定交易日的所有数据（开盘价、收盘价、最高价、最低价、涨跌额、涨跌幅、换手率(待定)、成交量、成交金额、总市值、流通市值(待定)）
        """
        # 判断传入的代码是否是字母加数字（如 sz002415）
        if stock_id.isalnum():
            stock_id = stock_id[2:]
        # 如果股票代码首位是0或者3则需添加一个1，反之则需添加一个0
        if stock_id[0] == "0" or stock_id[0] == "3":
            stock_id = "1" + stock_id
        else:
            stock_id = "0" + stock_id
        url = "http://quotes.money.163.com/service/chddata.html?" \
              "code=" + stock_id + "&start=" + date + "&end=" + \
              date + "&fields=TOPEN;TCLOSE;HIGH;LOW;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        result = requests.get(url)
        # print(result.url)
        result = result.text.split("\r\n")[1].split(",")[3:]
        print("[get2_stock_all_data_by_id_and_date] {}股票在 {} 的所有数据为：{}".format(stock_id[1:], date, result))
        return result

    def get3_stock_close_price_by_id_and_date(self, stock_id, date):
        """
        功能3：获取指定股票指定交易日的收盘价
        :param date: 指定日期
        :return: 返回此股票指定日期的收盘价格
        """
        # step1：用于计算股票查询的个数（如果连续查询的是相同的股票id 则不计数 反之计数+1）
        if stock_id != self.stock_id_get3:
            self.stock_count_get3 += 1
        self.stock_id_get3 = stock_id

        # step2：查询
        result = self.get2_stock_all_data_by_id_and_date(stock_id, date)
        print(result)
        # 没有数据
        if len(result) == 0:
            print("[WARNING][get3_stock_close_price_by_id_and_date] 第 {} 支股票 {}，在{}的收盘价为：{}".format(self.stock_count_get3,
                                                                                                  stock_id,
                                                                                                  date, result))
        # 有数据
        else:
            result = result[1]
            print("[get3_stock_close_price_by_id_and_date] 第 {} 支股票 {}，在{}的收盘价为：{}".format(self.stock_count_get3,
                                                                                           stock_id,
                                                                                           date, result))
        return result

    def get4_all_stock_id_by_type(self):
        """
        功能4：获取指定类型的所有股票代码
        :return: 返回指定类型的所有股票信息（symbol、code、name） 是一个数组json格式的list列表
        """
        page = 1
        stocks = []
        while True:
            url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?" \
                  "page={}&num=100&sort=symbol&asc=1&node={}&symbol=&_s_r_a=init".format(page, self)
            result = requests.get(url).text
            # print("请求结果：{}".format(result))
            result = demjson.decode(result)

            # 请求完所有的数据后 则退出循环
            # print(result)
            if result is None or len(result) == 0:
                break

            # 循环找出所有股票的代码及名称
            i = 0
            while i < len(result):
                stocks.append({"symbol": result[i]["symbol"], "code": result[i]["code"], "name": result[i]["name"]})
                i = i + 1
            print("当前第{}页，总共已获取{}支股票".format(page, len(stocks)))
            # print(stocks)
            page = page + 1
        print("{}类型的所有股票代码及名称汇总：{}".format(self, stocks))
        print("{}类型的股票总共有{}支".format(self, len(stocks)))
        return stocks

    def get5_all_stock_id_by_concept_in_block(self):
        """
        功能5：获取沪深股市中热门概念为区块链的所有股票
        :return:返回沪深股市中所有为区块链概念的股票（symbol、code、name） 是一个数组json格式的list列表
        """
        page = 1
        stocks = []
        while True:
            url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?" \
                  "page={}&num=100&sort=symbol&asc=1&node=chgn_700231&symbol=&_s_r_a=init".format(page)
            result = requests.get(url).text
            result = demjson.decode(result)
            # 请求完所有的数据后 则退出循环
            if result is None:
                break
            # print(result)
            i = 0
            while i < len(result):
                stocks.append({"symbol": result[i]["symbol"], "code": result[i]["code"], "name": result[i]["name"]})
                i = i + 1
            # print("第{}页有{}支股票".format(page, len(stocks)))
            # print(stocks)
            page = page + 1

        print("沪深股市中所有为区块链概念的股票代码及名称汇总：{}".format(stocks))
        print("沪深股市中所有为区块链概念的股票总共有{}支".format(len(stocks)))
        return stocks

    def get6_close_by_id_and_date(self, stock_id_list, stock_name_list, date_list):
        """
        功能6：获取指定股票在指定日期的收盘价
        :param stock_id_list: 股票列表
        :param date_list: 日期列表
        :return: 返回一个列表（列表中每个元素为一个字典 每个字典包含股票代码、名称、日期(日期对应的值为收盘价)）
        """
        close_price = []
        # 循环每一支股票
        stock_count = len(stock_id_list)
        count_by_stock = 0
        while count_by_stock < stock_count:
            # 循环每一个日期
            date_conut = len(date_list)
            count_by_date = 0
            dict_date = {}
            while count_by_date < date_conut:
                # 获取指定股票在指定日期的收盘价
                close = self.get3_stock_close_price_by_id_and_date(stock_id_list[count_by_stock],
                                                                   date_list[count_by_date])
                # 拼装信息
                # dict_date.update(date_list[count_by_date], close)
                dict_date[date_list[count_by_date]] = close
                count_by_date = count_by_date + 1
            dict_all = {
                "symbol": stock_id_list[count_by_stock],
                "name": stock_name_list[count_by_stock],
                "data": dict_date
            }
            close_price.append(dict_all)
            count_by_stock = count_by_stock + 1
        print("[get6_close_by_id_and_date] 收盘价：{}".format(close_price))
        return close_price


"""
从东方财富获取的数据（比较全面）
"""


class GetStockDataByDongFang:
    def get_all_a_stock(self):
        """
        获取沪深A股所有股票
        """
        quer = 'jQuery112408461723792185412_1611118385420'
        url = 'http://53.push2.eastmoney.com/api/qt/clist/get?' \
              'cb=' + quer + '&' \
                             'pn=1&' \
                             'pz=20&' \
                             'po=1&' \
                             'np=1&' \
                             'ut=bd1d9ddb04089700cf9c27f6f7426281&' \
                             'fltt=2&' \
                             'invt=2&' \
                             'fid=f3&' \
                             'fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&' \
                             'fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&' \
                             '_=1611118385503'  # 13位时间戳
        result = requests.get(url=url).text
        result = result[len(quer) + 1:-2]  # 转换接口返回数据的格式（转为json字符串）
        result = json.loads(result)
        count = result['data']['total']
        print(json.dumps(result))
        print('沪深A股所有股票数：', count)

    def get_lhb(self):
        # 界面地址：http://data.eastmoney.com/stock/tradedetail.html
        startDate = '2021-02-04'
        endDate = '2021-02-04'
        re = 'var data_tab_1'
        url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=300,page=1,sortRule=-1,sortType=,startDate={},endDate={},gpfw=0,js={}.html?rt=26874257'.format(
            startDate, endDate, re)
        result = requests.get(url=url).text
        result = result[len(re) + 1:]  # 转换接口返回数据的格式（转为json字符串）
        result = json.loads(result)
        result_data = result['data']
        count = len(result_data)
        #
        # SCode:股票代码
        # SName：股票名称
        # ClosePrice：收盘价
        # Chgradio：涨跌幅
        # Dchratio：换手率
        # Ctypedes：上榜原因
        #
        true_data = []
        for i in result_data:
            # 条件1 上涨
            # 条件2 收盘价 <= 15
            if float(i['Chgradio']) >= 0 and float(i['ClosePrice']) <= 15:
                td = {
                    'SCode': i['SCode'],
                    'SName': i['SName'],
                    'ClosePrice': i['ClosePrice'],
                    'Chgradio': i['Chgradio'],
                    'Dchratio': i['Dchratio'],
                    'Ctypedes': i['Ctypedes']

                }
                true_data.append(td)
        # print(json.dumps(result))
        print(*true_data, sep='\n')
        print('龙虎榜个数：{}  已筛选出{}只符合条件的'.format(count, len(true_data)))


# 新浪数据
if __name__ == "__main__":
    times1 = datetime.datetime.now()
    get_stock_data = GetStockDataServer()

    get_stock_data.get6_close_by_id_and_date(['sh600010'], ['包钢股份'], ['20210706', '20210707', '20210708', '20210709'])

    times2 = datetime.datetime.now()
    times = times2 - times1
    print("运行此程序总耗时：{}".format(times))

# 东方财富数据
# if __name__ == '__main__':
#     # GetStockDataByDongFang().get_all_a_stock()
#     GetStockDataByDongFang().get_lhb()
