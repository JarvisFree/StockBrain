#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/29 9:44
@Author  ：维斯
@File    ：message.py
@Version ：1.0
@Function：提送消息（微信、短信等）
"""
import datetime

import requests


def send_sms(phone_number: list, message):
    """
    发送短信
    @param phone_number: 手机号
    @param message: 短信文本
    """
    key = 'd41d8cd98f00b204e980'
    username = 'UserJourney'
    url = f'http://utf8.api.smschinese.cn/?Uid={username}&Key={key}&smsMob={",".join(phone_number)}&smsText={message}'
    result = requests.get(url).text
    print(f'{phone_number}发送结果：{result}')


if __name__ == '__main__':
    phone = [
        '13678066240',
        '13208186240'
    ]
    message = f'测试短信！！√（{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}）'
    send_sms(phone, message)
