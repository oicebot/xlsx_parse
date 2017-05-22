#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# filename: sanitize.py
#
# 运行方法，用 Python IDLE 打开，按 F5 运行
#

import argparse
from openpyxl import load_workbook
import os

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


def get_sheets(excel_file_path):

    base_path = os.path.dirname(
        os.path.abspath(__file__)
    )

    file_path = os.path.join(base_path, excel_file_path)

    workbook = load_workbook(file_path)

    sheets = []

    for sheet in workbook:
        sheets.append(sheet)

    return sheets


def list_all_sheets(sheets):

    sheet_ids = []

    for index, item in enumerate(sheets):
        print(index, ':', item.title)
        sheet_ids.append(index)

    return sheet_ids


def load_sheet_from_input(sheets):

    selected_sheet = None

    while True:
        sheet_ids = list_all_sheets(sheets)

        user_selection = input('请输入你想要解析的工作表的编号：')

        if not user_selection.isdigit():
            print('请输入对应的数字')
            continue

        sheet_id = int(user_selection)

        if sheet_id not in sheet_ids:
            print('您输入的 ID 不存在，')
            continue

        selected_sheet = sheets[sheet_id]
        print('')
        break


    print('已打开表："', selected_sheet.title, '",解析中…')
    return selected_sheet


def save_workbook(cleaned_data):

    pass

if __name__ == '__main__':
    args = parse_command()
    print(args)
    sheets = get_sheets(args.file)



    load_sheet_from_input(sheets)
