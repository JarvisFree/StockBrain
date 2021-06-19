#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/5/18 14:39
@Author  ：维斯
@File    ：param_to_json.py
@Version ：1.0
@Function：参数转JSON
"""

import json


def params_to_json(str_params):
    """
    从浏览器中复制的GET、POST请求中的参数 转换为字典
    备注1：
    :param str_params: 从浏览器中复制的GET、POST请求中的参数（view source模式下复制的）如：
                login_site=E&module=login&rand=code&15959
    :return 格式化的JSON字符串 如：
                {
                    "login_site": "E",
                    "module": "login",
                    "rand": "code",
                    "": "15959"
                }
    """
    result_list = str_params.split('&')
    result_dict = {}
    for item in result_list:
        # 是否有”=“符号
        if item.find('=') != -1:
            item_result = item.split('=')
            result_dict.update({item_result[0]: item_result[1]})
        else:
            result_dict.update({'': item})
    # 转换为json格式
    print(json.dumps(result_dict, indent=4, ensure_ascii=False))
    return json.dumps(result_dict, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    str1 = 'login_site=E&module=login&rand=code&15959'
    params_to_json(str_params=str1)
