#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# filename: sanitize.py
#
# 运行方法，用 Python IDLE 打开，按 F5 运行
#

import argparse
from openpyxl import load_workbook

# 导入调试用工具，彩色打印，区分 print 打印 debug 打印 exception 打印

def parse_command():

    parser = argparse.ArgumentParser(
        prog="python3 sanitize.py",
        description="sanitize data",
        )
    parser.add_argument(
        '-f',
        '--file',
        default="testdata.xlsx",
        help="Excel file for sanitizing (default: testdata.xlsx)",
        )
    parser.add_argument(
        '-o',
        '--output',
        default="outinfo.xlsx",
        help="Export Excel file (default: outinfo.xlsx)",
        )
    parser.add_argument(
        '-s',
        '--sheet',
        help="Choose sheet by sheet name"
        )

    args = parser.parse_args()

    return args


def getTable(excel_file_path):
    # 使用绝对地址
    workbook = load_workbook(excel_file_path)

    tables = []

    for sheet in workbook:
        tables.append(sheet)


if __name__ == '__main__':
    args = parse_command()
    print(args)
