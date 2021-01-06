# 一次只能打开一个弹窗
# 导入网络数据库
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
# 添加商品弹窗
class askAddGood(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("添加商品")
        self.geometry('1000x400')
        self.Info = []
        self.infoList = []
        self.setupUI()
    
    def setupUI(self):
        # row1: menu
        menu = Frame(self)
        menu.pack(fill='x')
        content = ["商品型号", "抢购时间", "心理价位", "浮动范围"]
        for i in range(0, 4):
            Label(menu,text=content[i], font=('楷体', 12), height=2).grid(row=1, column=i, padx=70, ipadx = 20)
        # row2 - 11: goods information
        for i in range(0,10):
            self.setupUIEnterGoods()
        # row 12: confirm and cancel button
        choice = Frame(self)
        choice.pack(fill='x')
        Label(choice,text='', font=('楷体', 12), height=1).pack()
        Label(choice,text='', font=('楷体', 10), width=5, height=1).pack(side=RIGHT)
        Button(choice, text="取消", font=('楷体', 12), width=15, height=1, command=self.cancel).pack(side=RIGHT)
        Button(choice, text="确定", font=('楷体', 12), width=15, height=1, command=self.confirm).pack(side=RIGHT)
    
    def confirm(self):
        content = ['name', 'time', 'price', 'float']
        tempDic = {}
        for goods in self.Info:
            for i in range(0,4):
                if len(goods[content[i]].get()) != 0:
                    tempDic[content[i]] = goods[content[i]].get()
            if len(tempDic) == 4:
                self.infoList.append(tempDic)
            tempDic = {}
        self.destroy()
    
    def cancel(self):
        self.Info = None
        self.destroy()
    
    def setupUIEnterGoods(self):
        good = Frame(self)
        good.pack(fill='x')
        content = ['name', 'time', 'price', 'float']
        receivedInfo = dict()
        for i in range(0, 4):
            receivedInfo[content[i]] = StringVar()
            Entry(good,textvariable=receivedInfo[content[i]], font=('楷体', 12), width=19).grid(row=1, column=i, padx=26, ipadx = 20)
        self.Info.append(receivedInfo)
        Label(self, text='', font=('楷体', 2), width = 400, height=1).pack()

# 删除商品弹窗
class askDeleteGood(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("删除商品")
        # self.geometry('1000x400')
        self.Info = []
        self.infoList = []
        self.setupUI()
    
    def setupUI(self):
        # row1: menu
        menu = Frame(self)
        menu.pack(fill='x')
        Label(menu, text='请输入需要取消关注的产品', font=('楷体', 14),width = 40, height=3).pack(side=LEFT)
        # row2 - 11: goods information
        for i in range(0, 4):
            self.setupUIEnterGoods()
        # row 12: confirm and cancel button
        choice = Frame(self)
        choice.pack(fill='x')
        Label(choice,text='', font=('楷体', 12), height=1).pack()
        Label(choice,text='', font=('楷体', 10), width=5, height=1).pack(side=RIGHT)
        Button(choice, text="取消", font=('楷体', 12), width=15, height=1, command=self.cancel).pack(side=RIGHT)
        Button(choice, text="确定", font=('楷体', 12), width=15, height=1, command=self.confirm).pack(side=RIGHT)
        Label(self,text='', font=('楷体', 10), width=5, height=1).pack()
    
    def confirm(self):
        for goods in self.Info:
            if len(goods.get()) != 0:
                self.infoList.append(goods.get())
        self.destroy()
    
    def cancel(self):
        self.infoList = None
        self.Info = None
        self.destroy()
    
    def setupUIEnterGoods(self):
        good = Frame(self)
        good.pack(fill='x')
        message = StringVar()
        Entry(good,textvariable=message, font=('楷体', 12), width=19).pack()
        self.Info.append(message)
        Label(self, text='', font=('楷体', 2), width = 25, height=1).pack()

# 主窗
class APP(Tk):
    def __init__(self):
        super().__init__()
        self.title("农村淘宝抢购")
        self.geometry('1000x580')
        self.database = []
        self.Info = []
        self.setupUI()
    
    def setupUI(self):
        # welcome notes
        Label(self, text='欢迎使用淘宝秒杀~', bg='bisque', font=('楷体', 20),width = 400, height=2).pack()
        # add goods
        addG = Frame(self)
        addG.pack(fill='x')
        Label(addG, text='', font=('楷体', 14),width = 5, height=3).pack(side=LEFT)
        Label(addG, text='', font=('楷体', 12),width = 5, height=2).pack(side=RIGHT)
        Button(addG, text="一键清空", font=('楷体', 12), width=15, height=1, command=self.clearAll).pack(side=RIGHT)
        Label(addG, text='', font=('楷体', 12),width = 2, height=2).pack(side=RIGHT)
        Button(addG, text="删除商品", font=('楷体', 12), width=15, height=1, command=self.deleteGoods).pack(side=RIGHT)
        Label(addG, text='', font=('楷体', 12),width = 2, height=2).pack(side=RIGHT)
        Button(addG, text="添加商品", font=('楷体', 12), width=15, height=1, command=self.addGoods).pack(side=RIGHT)
        # show information
        self.showInfo()
        # start and exit
        Button(self, text="开始秒杀", font=('楷体', 12), width=15, height=1, command=self.startBuy).place(x=670,y=530)
        Button(self, text="退出", font=('楷体', 12), width=15, height=1, command=self.exit).place(x=830,y=530)
    def showInfo(self):
        ''' 创建一个可滚动的表格'''
        form = ttk.Treeview(self, show="headings", height=18)
        form['columns'] = ("name", "price", "idealPrice", "buyStatus")
        # 设置列宽度以及居中显示
        widthSet = [500,150,150,120]
        for i in range(0, len(form['columns'])):
            form.column(form['columns'][i], width=widthSet[i])
            form.column(form['columns'][i], anchor = "center")
        # 添加列名
        names = ["商品型号", "价格", "心理价位", "抢购状态"]
        for i in range(0,len(form['columns'])):
            form.heading(form['columns'][i], text=names[i])
        form.place(x=40, y=130)     
        # 修改字体大小
        styleH = ttk.Style()
        styleH.configure("Treeview.Heading", font=(None, 14))
        styleB = ttk.Style()
        styleB.configure("Treeview", font=(None, 14))
        # 给表格添加滚动条
        verticalBar = ttk.Scrollbar(form, orient=VERTICAL, command=form.yview)
        # 给表格添加数据
        if len(self.database) == 0:
            return
        for i in range(0, len(self.database)):
            form.insert('', 0, text='',values=(self.database[i]['name'], self.database[i]['time'],self.database[i]['price'],self.database[i]['float']))
    
    def addGoods(self):
        inputGoods = askAddGood()
        self.wait_window(inputGoods)
        if inputGoods.infoList is None or len(inputGoods.infoList) == 0: return
        # 提取所需参数存储到该class
        self.updateGoods(inputGoods.infoList)
        # 将临时参数根据需要添加到数据库
        self.addToDataBase()
        # 将本次临时参数库清空
        self.clear()
        # 更新界面
        self.showInfo()

    def deleteGoods(self):
        inputGoods = askDeleteGood()
        self.wait_window(inputGoods)
        if inputGoods.infoList is None or len(inputGoods.infoList) == 0: return
        self.updateGoods(inputGoods.infoList)
        self.deleteFromDataBase()
        self.clear()
        self.showInfo()

    def updateGoods(self, inputGoodsList):
        for good in inputGoodsList:
            self.Info.append(good)

    def addToDataBase(self):
        ''' This function will add the data to the database and compare if the data is replicated '''
        ''' If the data is replicated, give the hint '''
        (replicatedData, nonReplicatedData) = self.checkGoodExist(self.Info, self.database)
        self.database = self.database + nonReplicatedData
        if len(replicatedData) != 0:
            ''' update the database info '''
            for goods in replicatedData:
                for figure in self.database:
                    if goods['name'] in str(figure['name']):
                        figure['time'] = goods['time']
                        figure['price'] = goods['price']
                        figure['float'] = goods['float']

    def deleteFromDataBase(self):
        ''' This function will delete the goods from database in terms of the given names '''
        for goods in self.Info:
            i = 0
            while i < len(self.database):
                ''' 如果数据被删除，则下一个数据被上挪，被上挪的数据则不会被遍历导致无法完全删除 '''
                if goods in str(self.database[i]['name']):
                    self.database.remove(self.database[i])
                    i -= 1
                    if len(self.database) == 0: break
                i += 1
    def checkGoodExist(self, data, database):
        ''' given two lists of dicts and check if the data is in database '''
        ''' if the data is replicated, return a list of the replicated data'''
        existDict = []
        nonReplicatedData = []
        exist = False
        for figure in data:
            if len(database) == 0:
                return([], data)
            for monoData in database:
                if figure['name'] in str(monoData['name']):
                    exist = True
            if exist: existDict.append(figure)
            else: nonReplicatedData.append(figure)
        return (existDict, nonReplicatedData)
    
    def clear(self):
        self.Info = []
    
    def clearAll(self):
        self.database = []
        self.showInfo()
    
    def exit(self):
        self.destroy()
    def startBuy(self):
        pass

class buy():
    def __init__(self):
        pass


if __name__ == '__main__':
    app = APP()
    app.mainloop()