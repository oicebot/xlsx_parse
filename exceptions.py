# -*- coding: utf-8 -*-


class WangdachuiError(Exception):


    def __init__(self, original_data):
        self.original_data = original_data

    def __repr__(self):
        return '<' + str(self.original_data) + '>'

    def __str__(self):
        pass


class SheetNotFoundError(WangdachuiError):

    def __init__(self, workbook, sheet):

        self.workbook = workbook
        self.sheet = sheet

    def __repr__(self):
        pass

    def __str__(self):
        pass

if __name__ == '__main__':
    exception = WangdachuiError('无法运行')

    print(exception)
