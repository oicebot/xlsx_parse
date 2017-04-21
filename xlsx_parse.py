#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# filename: xlsx_parse.py
# Debug on Python 3.5.2
# 2017.04.17 by Oicebot 
#
# 运行方法，用 Python IDLE 打开，按 F5 运行
#
#

from openpyxl import Workbook, load_workbook
from parse_functions import parse_sonography

table_title=['编号','姓名','年龄','住院号',
             '描述','位置','大小','形态','生长方向',
             '边缘','分布','内部回声','钙化','后方回声',
             ]

def create_rows(indata_sheet):
    global table_title
    row_objs = [] 
    
    for row in indata_sheet.rows:
    
        parsed_data = parse_sonography(row[8].value)

        for data_item in parsed_data:

            info_data = dict.fromkeys(list(table_title),'')
            info_data['编号'] = row[0].value
            info_data['姓名'] = row[1].value
            info_data['年龄'] = row[3].value
            info_data['住院号'] = row[4].value
            
            for key,item in data_item.items():
                info_data[key] = item

            row_objs.append(info_data)

    return row_objs


if __name__ == '__main__':

    indata = load_workbook('testdata.xlsx')
    #indata = load_workbook('info.xlsx')

    print('该文件中含有如下工作表：')
    sheets = []
    for sheet in indata:
        sheets.append(sheet)

    print('===========')
    SheetID = 'A'
    indata_sheet = None
    while not SheetID.isdigit():
        
        i = 0
        for sheet in sheets:
            print ("{} : {}".format(i,sheet.title))
            i += 1
        print('请输入你想要解析的工作表的编号：',end='')
        SheetID = input()

        try:
            indata_sheet = sheets[int(SheetID)]
        except Exception as errinfo :
            print('打开失败……', errinfo)
            SheetID = 'A'
        else:
            print('已打开 {}，解析中…'.format(indata_sheet.title))
            
    
    outtable= [ table_title, ]

    row_objs = create_rows(indata_sheet)
    
    index = 0
    print('Items added:')
    for i in row_objs:
        if index % 10 == 0:
            print(str(index),end='')
        else:
            print('.',end='')
        
        #print('----- {} -----'.format(index))
        index += 1
        next_row =[]
        for key in table_title:
            #print('{} : {}'.format(key,i[key]))
            next_row.append(i[key])

        outtable.append(next_row)

    wb = Workbook()
    ws = wb.active

    for row in outtable:
        ws.append(row)

    wb.save("outinfo.xlsx")

    
            

            




            
            

