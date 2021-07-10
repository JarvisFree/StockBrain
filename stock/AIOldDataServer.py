#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2019-10-23 22:30
@Author  ：维斯
@File    ：__init__.py
@Version ：1.0
@Function：股票历史数据分析服务
"""

import csv

import tushare
import datetime

from stock import StockParams
from stock.GetStockDataServer import GetStockDataServer


class AIOldDataServer:
    get_stock_data = GetStockDataServer()

    @staticmethod
    def ai_trading_day(self):
        """
        功能1：判断自然日是否是交易日（YES：返回此自然日；NO：从此自然日依次往前推至交易日 并返回）
        缺点：要计算10秒左右才出结果
        :return:
        """
        date_str = "{}-{}-{}".format(self[0:4], self[4:6], self[6:8])
        y, m, d = date_str.split("-")
        my_date = datetime.date(int(y), int(m), int(d))

        # 判断日期是否是交易日
        while True:
            if tushare.is_holiday(datetime.date.strftime(my_date, "%Y-%m-%d")):
                # 不是交易日 则此日期减一天 再次循环判断
                my_date = my_date + datetime.timedelta(days=-1)
            else:
                # 是交易日
                break
        print("离{}最近的一个历史交易日为：{}".format(date_str, my_date))
        return my_date

    def ai_get_close_data_by_id_and_date_write_csv(self):
        """
        功能3：获取区块链所有股票在24、25的收盘价并写入csv文件
        :return:
        """
        # step1：获取所有区块链股票信息（symbol、code、name）
        stock_list = self.get_stock_data.get5_all_stock_id_by_concept_in_block()
        stock_id_list = []
        stock_name_list = []
        count_stock = 0
        while count_stock < len(stock_list):
            stock_id_list.append(stock_list[count_stock]["symbol"])
            stock_name_list.append(stock_list[count_stock]["name"])
            count_stock = count_stock + 1

        # step2：查询日期
        date_str = StockParams.Params.param1_search_date
        search_list = date_str.split(",")
        print("[ai_get_close_data_by_id_and_date_write_csv] 查询日期列表：{}".format(search_list))

        # step3：循环查询
        result_list = self.get_stock_data.get6_close_by_id_and_date(stock_id_list, stock_name_list, search_list)

        # step4：将查询结果写入csv文件中
        print("999999999999999999999999999999999999999999999999999999999999999999")
        count_result = 0
        csv_heard = ["股票代码", "股票名称"]
        csv_rows = []

        # step4.1：csv文件头 csv_heard
        count_date = 0
        # 把要查询的所有日期添加到csv文件的头中
        while count_date < len(search_list):
            csv_heard.append(search_list[count_date])
            count_date += 1

        # step4.2：csv内容数据 rows
        count_stock = 0
        while count_result < len(result_list):
            # 根据日期个数动态获取对应日期的数据
            list_tup = []
            count_rows = 0
            list_tup.append(result_list[count_stock]["symbol"])
            list_tup.append(result_list[count_stock]["name"])
            while count_rows < len(search_list):
                list_tup.append(result_list[count_stock]["date"][search_list[count_rows]])
                count_rows += 1
            # 把一行的列表转换为元组
            tup = tuple(list_tup)
            csv_rows.append(tup)
            count_result += 1
            count_stock += 1

        # step5：数据开始写入csv
        with open("20191101.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(csv_heard)
            w.writerows(csv_rows)

        print(result_list)
        print("999999999999999999999999999999999999999999999999999999999999999999")


if __name__ == "__main__":
    time_start = datetime.datetime.now()
    ai_old_data = AIOldDataServer()

    # ai_old_data.ai_trading_day("20191007")

    AIOldDataServer.ai_trading_day("20210710")

    # ai_old_data.ai_get_close_data_by_id_and_date_write_csv()

    time_end = datetime.datetime.now()
    print("运行此程序共耗时：{}".format(time_end - time_start))
