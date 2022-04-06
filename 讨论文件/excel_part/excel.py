import os
import xlrd
import xlwt
class Excel():
    def __init__(self):
        self.excel_path = os.path.abspath(os.getcwd()) + os.sep + '抢购信息.xlsx'

    def readTable(self):
        data = xlrd.open_workbook(self.excel_path)
        table = data.sheet_by_name('1')
        rows = table.nrows
        cols = table.ncols
        info = list()
        for rowNum in range(3,rows):
            rowValue = table.row_values(rowNum)
            tempInfo = {
                'brand': '等待爬取数据',
                'name_short': rowValue[0],
                'name_full': '等待爬取数据',
                'id': '等待爬取数据',
                'price_now': '等待爬取数据',
                'ideal_price': rowValue[1],
                'buy_status': '等待爬取数据',
                'time': rowValue[2],
                'price_gap': '等待爬取数据',
            }
            info.append(tempInfo)
        return info

print(Excel().readTable())