#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/17 22:56
@Author  ：维斯
@File    ：decorator.py
@Version ：1.0
@Function：装饰器工具
"""
import time


def elapsed_time(name='', is_print=True):
    """
    耗时计算
    @param name:
    @param is_print:
    @return:
    """

    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            s_time = time.time()
            result = func(*args, **kwargs)
            hao_shi = int(time.time() - s_time)
            h = str(int(hao_shi / 3600))
            m = str(int(hao_shi % 3600 / 60))
            s = str(int(hao_shi % 3600 % 60))
            if is_print:
                print(f'[{func.__name__}] {name} 耗时： {h.zfill(2)}:{m.zfill(2)}:{s.zfill(2)}')
            return result

        return inner_wrapper

    return wrapper


