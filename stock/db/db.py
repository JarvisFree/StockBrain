#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/25 16:21
@Author  ：维斯
@File    ：db.py
@Version ：1.0
@Function：
"""
import sqlite3

import pymysql


class DB:
    def __init__(self):
        self.con = sqlite3.connect('E:\Code\Success\StockBrain\stock\db\StockData.db')
        self.cur = self.con.cursor()

    def add_ta_check_trading(self, a, b):
        """
        @param data: [('20210725',0),(),]
        """
        sql = f'INSERT INTO check_trading VALUES({a},{b})'
        self.cur.execute(sql)
        self.con.commit()

    def select_ta_check_trading(self, date):
        sql = f'SELECT * FROM check_trading WHERE date={date}'
        self.cur.execute(sql)
        # print(self.cur.fetchall())
        return self.cur.fetchall()


if __name__ == '__main__':
    DB().select_ta_check_trading('20210724')
