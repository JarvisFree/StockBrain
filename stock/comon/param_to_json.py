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
import time


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
        if item.__find('=') != -1:
            item_result = item.split('=')
            result_dict.update({item_result[0]: item_result[1]})
        else:
            result_dict.update({'': item})
    # 转换为json格式
    print(json.dumps(result_dict, indent=4, ensure_ascii=False))
    return json.dumps(result_dict, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    str1 = 'cb=jQuery11240752172781178722_1626791176575&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:1+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222&_=1626791176711'
    params_to_json(str_params=str1)
    print(time.time() * 1000)

    ss = 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222'
    s_list = ss.split(',')
    dict_s = {}
    for i in s_list:
        dict_s.update({i: ''})
    print(dict_s)