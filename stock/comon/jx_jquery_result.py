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

    if str1.__find('null') != -1:
        str1 = str1.replace('null', '"null"')

    if str1.endswith(';'):
        tupe_str = eval(str1[str1.find('('):-1] + ',')  # 去掉括号前后的东西 并转换为元组
    elif str1.endswith(')'):
        tupe_str = eval(str1[str1.find('('):] + ',')  # 去掉括号前后的东西 并转换为元组
    else:
        print('没有预定的结尾符')
    return tupe_str[0]


if __name__ == '__main__':
    aa = jx_jquery_result(
        '/**/jQuery19103950574251888599_1620545412321({"result_message":"验证码校验成功","result_code":"4"});')
    print(aa)
