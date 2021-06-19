#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/18 15:39
@Author  ：维斯
@File    ：jx_jquery_result.py
@Version ：1.0
@Function：jQuery对象转字典
"""


def jx_jquery_result(str1):
    """
    解析接口返回的jQuery对象为字典
    如：
    str1:   /**/jQuery19103950574251888599_1620545412321({"result_message":"验证码校验成功","result_code":"4"});
    转换后:  {'result_message': '验证码校验成功', 'result_code': '4'}

    :param str1:
    :return: 字典
    """
    tupe_str = eval(str1[str1.find('('):-1] + ',')
    # print(tupe_str[0])
    return tupe_str[0]
