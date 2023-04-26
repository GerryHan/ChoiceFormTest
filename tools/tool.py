#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/3 12:41
# @Author  : Glory Gu
import functools


def value_check(checked_data, expect_key, default_value='', check_result=None):
    if check_result is not None:
        if isinstance(checked_data, dict):
            if expect_key not in checked_data.keys() or checked_data[expect_key] in ['请输入', '']:
                check_result.append(False)
            else:
                check_result.append(True)
            return checked_data.get(expect_key, default_value)
        elif isinstance(checked_data, list):
            if len(checked_data) > 0:
                check_result.append(True)
                return ','.join([component[expect_key] for component in checked_data])
            else:
                check_result.append(False)
                return default_value


def filter_and_sort(df, conditions, sort_by=None, ascending=None):
    _df = df.loc[conditions]
    if sort_by:
        return _df.sort_values(by=sort_by, ascending=ascending)
    else:
        return _df


def get_formatter(workbook):
    formatter = {
        'text_wrap': True,  # 是否自动换行
        'valign': 'vcenter',  # 垂直对齐方式
        'border': 1,  # 单元格边框宽度
        'font_size': 10  # 字体大小
    }
    # 定义表头样式
    header_formatter = {
        'bold': True,  # 字体加粗
        'align': 'center',  # 水平对齐方式
        'valign': 'vcenter',  # 垂直对齐方式
    }
    dict.update(header_formatter, formatter)
    header_format = workbook.add_format(header_formatter)
    # 定义行样式
    cell_format = workbook.add_format(formatter)
    merge_formatter = {
        'align': 'center',  # 水平对齐方式
    }
    dict.update(merge_formatter, formatter)
    merge_format = workbook.add_format(merge_formatter)
    return {'base_formatter': formatter, 'header_formatter': header_format, 'cell_formatter': cell_format,
            'merge_formatter': merge_format}


def retry(max_count, description):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            raise_ex = None
            for count in range(max_count):
                print("\t%s, retry %s times, %s execution" % (description, max_count, count + 1))
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    raise_ex = ex
            raise raise_ex

        return wrapper

    return decorator
