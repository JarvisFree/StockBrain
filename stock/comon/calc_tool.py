#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    ：2021/7/21 22:40
@Author  ：维斯
@File    ：calc_tool.py
@Version ：1.0
@Function：
"""


def find_asc(data: list, min_limit: int, type='asc'):
    """
    获取data列表中连续min_limit及以上 个升序的数字
    @param data:
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
    @return
        [
            ['1', '2', '3', '4', '5', '8'],
            ['3', '4', '5'],
            ['7', '9', '17']
        ]
    """
    s_list = data
    count = min_limit
    all_list = []
    c = 1
    while True:
        alone_list = []
        if len(s_list) > count:
            if type == 'asc':
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
            elif type == 'desc':
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
    find_asc(data, 3)
