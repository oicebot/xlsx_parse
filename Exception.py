# -*- coding: utf-8 -*-


class WangdachuiError(Exception):


    def __init__(self, original_data):
        self.original_data = original_data

    def __repr__(self):
        return '<' + str(self.original_data) + '>'

    def __repr__(self):
        return '<' + str(self.original_data) + '>'

if __name__ == '__main__':
    raise RuntimeError('无法运行')
