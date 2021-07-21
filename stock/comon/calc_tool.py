#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/21 22:40
@Author  ：维斯
@File    ：calc_tool.py
@Version ：1.0
@Function：
"""


def find_asc(data_list: list, min_limit: int, *args, **kwargs):
    return __find(data_list, min_limit, 'asc', *args, **kwargs)


def find_desc(data_list: list, min_limit: int, *args, **kwargs):
    return __find(data_list, min_limit, 'desc', *args, **kwargs)


def __find(data_list: list, min_limit: int, order_type, keyword=None):
    """
    获取data列表中连续min_limit及以上 个升序的数字
    @param data_list:
        [
            '1',
            '1',
            '2',
            '3',
            '4',
            '5',
            '8',
            '3',
            '4',
            '5',
            '1',
            '1',
            '1',
            '1',
            '2',
            '1',
            '1',
            '1',
            '1',
            '1',
            '24',
            '7',
            '9',
            '17',
            '2',
            '1',
        ]
    @param min_limit: 最小限制个数
    @type 排序类型
    @keyword 字典中的目标key
    @return
        [
            ['1', '2', '3', '4', '5', '8'],
            ['3', '4', '5'],
            ['7', '9', '17']
        ]
    """
    s_list = data_list
    count = min_limit
    all_list = []
    c = 1
    while True:
        alone_list = []
        if len(s_list) > count:
            if order_type == 'asc':
                if keyword is None:
                    if all(float(s_list[i]) < float(s_list[i + 1]) for i in range(count - 1)):
                        index = count
                        wap_count = count
                        while True:
                            if index < len(s_list):
                                if float(s_list[index - 1]) < float(s_list[index]):
                                    wap_count += 1
                                    index += 1
                                else:
                                    break
                            else:
                                break
                        for j in range(wap_count):
                            alone_list.append(s_list[j])
                        all_list.append(alone_list)
                        c += 1
                        for i in range(wap_count):
                            s_list.pop(0)
                    else:
                        s_list.pop(0)
                else:
                    if all(float(s_list[i][keyword]) < float(s_list[i + 1][keyword]) for i in range(count - 1)):
                        index = count
                        wap_count = count
                        while True:
                            if index < len(s_list):
                                if float(s_list[index - 1][keyword]) < float(s_list[index][keyword]):
                                    wap_count += 1
                                    index += 1
                                else:
                                    break
                            else:
                                break
                        for j in range(wap_count):
                            alone_list.append(s_list[j])
                        all_list.append(alone_list)
                        c += 1
                        for i in range(wap_count):
                            s_list.pop(0)
                    else:
                        s_list.pop(0)
            elif order_type == 'desc':
                if keyword is None:
                    if all(float(s_list[i]) > float(s_list[i + 1]) for i in range(count - 1)):
                        index = count
                        wap_count = count
                        while True:
                            if index < len(s_list):
                                if float(s_list[index - 1]) > float(s_list[index]):
                                    wap_count += 1
                                    index += 1
                                else:
                                    break
                            else:
                                break
                        for j in range(wap_count):
                            alone_list.append(s_list[j])
                        all_list.append(alone_list)
                        c += 1
                        for i in range(wap_count):
                            s_list.pop(0)
                    else:
                        s_list.pop(0)
                else:
                    if all(float(s_list[i][keyword]) > float(s_list[i + 1][keyword]) for i in range(count - 1)):
                        index = count
                        wap_count = count
                        while True:
                            if index < len(s_list):
                                if float(s_list[index - 1][keyword]) > float(s_list[index][keyword]):
                                    wap_count += 1
                                    index += 1
                                else:
                                    break
                            else:
                                break
                        for j in range(wap_count):
                            alone_list.append(s_list[j])
                        all_list.append(alone_list)
                        c += 1
                        for i in range(wap_count):
                            s_list.pop(0)
                    else:
                        s_list.pop(0)
        else:
            break
    print(*all_list, sep='\n')
    return all_list


if __name__ == '__main__':
    data = [
        '1',
        '1',
        '2',
        '3',
        '4',
        '5',
        '8',
        '3',
        '4',
        '5',
        '3',
        '1',
        '1',
        '1',
        '2',
        '1',
        '1',
        '1',
        '1',
        '1',
        '24',
        '7',
        '9',
        '17',
        '2',
        '1',
    ]
    data_dict = [
        {'F12': '1'},
        {'F12': '1'},
        {'F12': '2'},
        {'F12': '3'},
        {'F12': '4'},
        {'F12': '5'},
        {'F12': '8'},
        {'F12': '3'},
        {'F12': '4'},
        {'F12': '5'},
        {'F12': '3'},
        {'F12': '1'},
        {'F12': '1'},
        {'F12': '1'},
        {'F12': '2'},
        {'F12': '1'},
        {'F12': '1'},
        {'F12': '1'},
        {'F12': '1'},
        {'F12': '1'},
        {'F12': '24'},
        {'F12': '7'},
        {'F12': '9'},
        {'F12': '17'},
        {'F12': '2'},
        {'F12': '1'},
    ]
    # find_asc(data_dict, 3, keyword='F12')
    find_desc(data_dict, 3, keyword='F12')
    # find_desc(data, 3)
