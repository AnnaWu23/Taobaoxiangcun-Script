from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import requests
import re
from random import choice
from time import sleep
from mitmproxy.tools._main import mitmdump
import threading
import os
import NetDataBase
from datetime import date, timedelta, datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import platform
import json
from selenium.webdriver.support.wait import WebDriverWait
import LocalDatabase
import pickle
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
        self.geometry('1160x580')
        # info that need to be show in the table
        self.beforeComp = []
        # info of the goods in cart
        self.cartGoodInfo = []
        # info after comparing
        self.afterComp = []
        # the goods need to buy in a mintue
        self.buyList = []
        self.cookie_path = os.path.abspath(os.getcwd()) + os.sep + 'COOKIE'
        self.readCookie()
        self.setupUI()
        Proxy()

    def readCookie(self):
        try:
            f = open(self.cookie_path, 'rb')
            NetDataBase.COOKIE = pickle.load(f)
            f.close()
        except:
            messagebox.showinfo("提示","需要扫码登录之后刷新才可以显示完整信息哟")

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
        Label(addG, text='', font=('楷体', 12),width = 5, height=2).pack(side=RIGHT)
        Label(addG, text='时间格式：例如：1月6日下午1点30分填写为1-6 1:30', font=('楷体', 12),width = 50, height=2).pack(side=RIGHT)
        # show information
        self.showInfo()
        # start and exit
        Button(self, text="确认好了，开始抢购", font=('楷体', 12), width=25, height=1, command=self.secKill).place(x=250,y=530)
        Button(self, text="刷新", font=('楷体', 12), width=15, height=1, command=self.refresh).place(x=505,y=530)
        Button(self, text="登录", font=('楷体', 12), width=15, height=1, command=self.log).place(x=670,y=530)
        Button(self, text="退出", font=('楷体', 12), width=15, height=1, command=self.exit).place(x=830,y=530)
        
    
    def showInfo(self):
        ''' 创建一个可滚动的表格'''
        form = ttk.Treeview(self, show="headings", height=18)
        form['columns'] = ('brand', "name", "price", "idealPrice","time", "buyStatus")
        # 设置列宽度以及居中显示
        widthSet = [100, 400,150,150, 150,120]
        for i in range(0, len(form['columns'])):
            form.column(form['columns'][i], width=widthSet[i])
            form.column(form['columns'][i], anchor = "center")
        # 添加列名
        names = ["品牌","商品型号", "价格", "心理价位","抢购时间","抢购状态"]
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
        if len(self.afterComp) == 0:
            return
        for i in range(0, len(self.afterComp)):
            form.insert('', 0, text='',values=(self.afterComp[i]['brand'], self.afterComp[i]['name_full'], self.afterComp[i]['price_now'], self.afterComp[i]['ideal_price'], self.afterComp[i]['time'],self.afterComp[i]['buy_status']))
    
    def addGoods(self):
        inputGoods = askAddGood()
        self.wait_window(inputGoods)
        if inputGoods.infoList is None or len(inputGoods.infoList) == 0: return
        # 将临时参数根据需要添加到程序数据库
        self.addToClassDataBase(inputGoods.infoList)
        # 将本次临时参数库清空
        self.clear()

    def deleteGoods(self):
        inputGoods = askDeleteGood()
        self.wait_window(inputGoods)
        if inputGoods.infoList is None or len(inputGoods.infoList) == 0: return
        self.deleteFromClassDataBase(inputGoods.infoList)
        self.clear()
        self.showInfo()

    def addToClassDataBase(self, inputGoods):
        ''' This function will add the data to the database and compare if the data is replicated '''
        ''' If the data is replicated, give the hint '''
        for item in inputGoods:
            tempDict = {
                'brand': '等待爬取数据',
                'name_short': item['name'],
                'name_full': '等待爬取数据',
                'ID': None,
                'price_now': 0,
                'ideal_price': item['price'],
                'buy_status': '等待爬取数据',
                'time': item['time'],
                'float': item['float'],
                'price_gap': 0,
                'price_cell': 0,
                'checked': None,
            }
            self.beforeComp.append(tempDict)

    def deleteFromClassDataBase(self, inputGoods):
        ''' This function will delete the goods from database in terms of the given names '''
        for goods in inputGoods:
            i = 0
            while i < len(self.afterComp):
                ''' 如果数据被删除，则下一个数据被上挪，被上挪的数据则不会被遍历导致无法完全删除 '''
                if goods in str(self.afterComp[i]['name_full']):
                    self.afterComp.remove(self.afterComp[i])
                    i -= 1
                    if len(self.afterComp) == 0: break
                i += 1

    def checkGoodExist(self, data, database):
        ''' given two lists of dicts and check if the data is in database '''
        ''' if the data is replicated, return a list of the replicated data'''
        existDict = []
        nonReplicatedData = []
        for figure in data:
            exist = False
            if len(database) == 0:
                return([], data)
            for monoData in database:
                if figure['name_short'] in str(monoData['name_full']):
                    exist = True
            if exist: existDict.append(figure)
            else: nonReplicatedData.append(figure)
        return (existDict, nonReplicatedData)
    
    def clear(self):
        self.Info = []
    
    def clearAll(self):
        self.beforeComp = []
        self.cartGoodInfo = []
        self.afterComp = []
        self.buyList = []
        self.showInfo()

    def exit(self):
        self.destroy()

    def refresh(self):
        try:
            self.updateAfterDatabase()
            (existData,nonRepData) = self.checkGoodExist(self.beforeComp, self.afterComp)
            if len(existData) != 0:
                self.beforeComp = nonRepData
            if len(self.beforeComp) != 0:
                if len(NetDataBase.COOKIE) != 0:
                    self.cartGoodInfo = Buy().direct_requests()
                self.updateAfterDatabase()
            self.showInfo()
            self.beforeComp.clear()
        except:
            messagebox.showinfo("提示","验证码过期，请尝试重新登录")

    def log(self):
        self.cartGoodInfo = Buy().web_login()
        self.updateAfterDatabase()
        self.showInfo()
        self.beforeComp.clear()

    def updateAfterDatabase(self):
        goodsNeedInCart = []
        for good in self.beforeComp:
            for data in self.cartGoodInfo:
                if good['name_short'] in str(data['name_full']):
                    goodsNeedInCart.append({
                        'name_short': good['name_short'],
                        'name_full': data['name_full'],
                        'ID': data['ID'],
                        'brand': data['brand'],
                        'time': good['time'],
                        'price_now': float(data['price_now'])/100,
                        'ideal_price': float(good['ideal_price']),
                        'price_gap': float(data['price_now'])/100 - float(good['ideal_price']),
                        'float': float(good['float']),
                        'price_cell': float(good['float']) + float(good['ideal_price']),
                        'checked': data['checked'],
                        'buy_status': data['buy_status']
                    })
                    break
        (existData,nonRepData) = self.checkGoodExist(goodsNeedInCart, self.afterComp)
        for data in nonRepData: self.afterComp.append(data)

        for good in existData:
            for data in self.afterComp:
                if good['name_short'] in str(data['name_full']):
                    data = {
                        'name_short': data['name_short'],
                        'name_full': good['name_full'],
                        'ID': good['ID'],
                        'brand': data['brand'],
                        'time': good['time'],
                        'price_now': float(good['price_now'])/100,
                        'ideal_price': float(data['ideal_price']),
                        'price_gap': float(good['price_now'])/100 - float(data['ideal_price']),
                        'float': float(data['float']),
                        'price_cell': float(data['float']) + float(data['ideal_price']),
                        'checked': good['checked'],
                        'buy_status': good['buy_status']
                    }
                    break

    def select_item(self, buyList, startBrowser):
        if len(buyList) == 0:
            return
        for item in buyList:
                if not item['checked']:
                    label = "".join(('//*[@id="J_Item_', item['ID'], '"]/ul/li[1]/div/div/div/label'))
                    target = startBrowser.find_element_by_xpath(label) 
                    startBrowser.execute_script("arguments[0].scrollIntoView();", target)
                    sleep(0.8)
                    startBrowser.find_element_by_xpath(label).click()
    
    def secKill(self):
        startBuy = self.startBrowser()
        # 通过时间排序需要抢购物品的先后顺序
        self.afterComp = sorted(self.afterComp, key=lambda x: x['time'], reverse=False)
        time = self.find_first_time()
        # 若未到达120s, 则一直等待
        while True:
            if Time().time_less_than_120s(time) is True:
                break
        # 到达120s，刷新现在价格
        self.refreshPrice()
        # 生成需要抢购的物品列表为buyList
        self.getBuyList()
        # 选择要抢购的物品
        self.select_item(self.buyList, startBuy)
        # 若价格合理则开始抢购, 抢购结束后关闭页面
        while not Time().time_arrived(time): pass
        self.click_buy(startBuy, time)
        # 将被抢购的商品替换状态并且进行下一次抢购
        self.replaceBuyStatus()
        
    def startBrowser(self):
        startBuy = Login()
        # 1 初始化浏览器
        startBuy.init_browser()
        # 2 打开淘宝购物车
        cookie = startBuy.browser.get("https://cart.taobao.com/cart.htm?t=1609822441959")
        startBuy.browser.delete_all_cookies()
        f = open(self.cookie_path, 'rb')
        cookies = pickle.load(f)
        f.close()
        for cookie in cookies:
            startBuy.browser.add_cookie(cookie)
        startBuy.browser.get("https://cart.taobao.com/cart.htm?t=1609822441959")
        return startBuy.browser
        
    def find_first_time(self):
        for item in self.afterComp:
            if item['buy_status'] != '已抢购' and not Time().time_arrived(item['time']):
                return item['time']

    def refreshPrice(self):
        Buy().direct_requests()
        self.beforeComp = self.afterComp
        self.updateAfterDatabase()
        self.beforeComp = []
    
    def getBuyList(self):
        self.afterComp = sorted(self.afterComp, key=lambda x: x['time'], reverse=False)
        for good in self.afterComp:
            if good['time'] == self.afterComp[0]['time'] and good['price_now'] <= good['price_cell'] and good['buy_status'] != '已抢购':
                self.buyList.append(good)
    
    def click_buy(self, startBrowser, time):
        startBrowser.find_element_by_id("J_Go").click()

        while True:
            try:
                startBrowser.find_element_by_xpath('//*[@id="ctTmypB2bFulfilmentSelectPC_ctTmypB2bFulfilmentSelectPC1"]/div/div/div/span/span[1]').click()
                break
            except:
                pass

        try:
            startBrowser.find_element_by_xpath('/html/body/div[4]/ul/li[2]/div').click()
        except:
            pass

        startBrowser.find_element_by_link_text('提交订单').click()
        
    def replaceBuyStatus(self):
        if len(self.buyList) == 0:
            return
        for good in self.buyList:
            for item in self.afterComp:
                if good['name_short'] == item['name_short']:
                    item['buy_status'] = '已抢购'
        self.buyList.clear()
    
            

class Buy():
    def __init__(self):
        self.infoList = []
        self.url = 'https://cart.taobao.com/cart.htm?t=1609822441959'
        self.cookie_path = os.path.abspath(os.getcwd()) + os.sep + 'COOKIE'
    
    def readCookie(self):
        try:
            f = open(self.cookie_path, 'rb')
            NetDataBase.COOKIE = pickle.load(f)
            f.close()
        except:
            pass

    def web_login(self):
        log = Login()
        log.start()
        self.readCookie()
        html = self.getHTMLText()
        self.grabInfo(html)
        return(self.infoList)

    def direct_requests(self):
        self.readCookie()
        html = self.getHTMLText()
        self.grabInfo(html)
        return(self.infoList)

    def getHTMLText(self):
        for i in range(5):
            try:
                session = requests.Session()
                self.addCookie(session)
                head = {"user-agent": self.getUserAgent()}
                r = session.get(self.url, headers = head, timeout=30)
                r.raise_for_status
                r.encoding = r.apparent_encoding
                if not self.checkBeenScraped(r.text):
                    return r.text
                else:
                    print("被反爬，请更新cookie")
            except:
                sleep(5)
        print('ERROR in getHTMLText')

    def grabInfo(self, html):
        try:
            pl = re.findall(r'\"price\"\:\{\"actual\"\:.*?\"oriPromo', html)
            tl = re.findall(r'\"skuId\".*?\"\,\"toBuy\"',html)
            idl = re.findall(r'\}\,\"cartId\".*?\,\"createTime\"',html)
            priceList = []
            titleList = []
            idList = []
            checkedList = []
            for item in pl:
                price = item.split('"now":')[1]
                price = price.split(',"oriPromo')[0]
                priceList.append(price)
            for item in tl:
                title = item.split('"title":"')[1]
                title = title.split('","toBuy"')[0]
                titleList.append(title)
            for item in idl:
                idAndChecked = item.split('","')
                id = idAndChecked[0]
                checked = idAndChecked[1]
                id = id.split('"cartId":"')[1]
                if 'false' in str(checked):
                    checked = False
                elif 'true' in str(checked):
                    checked = True
                else:
                    checked = None
                idList.append(id)
                checkedList.append(checked)
            if len(priceList) != len(titleList) and len(titleList) != len(idList) and len(idList) != len(checkedList):
                print('Unbalanced List')
                return
            self.storeData(priceList, titleList, idList, checkedList)
        except:
            print('ERROR in grabInfo')
            return ""

    def getCookie(self, num):
        if num < len(NetDataBase.COOKIE): return NetDataBase.COOKIE[num]
        return None
    
    def getUserAgent(self):
        return choice(NetDataBase.USER_AGENTS)
    
    def storeData(self, priceList, titleList, idList, checkedList):
        for i in range(0, len(priceList)):
            tempDict = {"name_full": titleList[i],
                        "brand":  self.checkBrand(titleList[i]),
                        "ID": idList[i],
                        "price_now": priceList[i],
                        "checked": checkedList[i],
                        "buy_status": None,
                        }
            self.infoList.append(tempDict)
    
    def checkBrand(self, title):
        for goods in NetDataBase.BRAND:
            for goodName in goods['names']:
                if goodName in str(title):
                    return goods['outputName']
        return ""

    def checkBeenScraped(self, html):
        try:
            loginPage = re.findall(r'\"登录页面\"改进建议', html)
            if len(loginPage) != 0:
                return True
            else: False
        except:
            print('ERROR in checkBeenScraped')
            return False
    
    def addCookie(self,session):
        jar = requests.cookies.RequestsCookieJar()
        for cookie in NetDataBase.COOKIE:
            jar.set(cookie['name'], cookie['value'])
        session.cookies = jar
        

class Login():
    def __init__(self):
        self.browser = None
        self.loginURL = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fcart.taobao.com%2Fcart.htm'
        self.cookie_path = os.path.abspath(os.getcwd()) + os.sep + 'COOKIE'
    def start(self):
        # 1 初始化浏览器
        self.init_browser()
        # 2 打开淘宝登录页
        self.browser.get(self.loginURL)
        while True:
            try:
                self.browser.find_element_by_id("J_SelectAllCbx1")
                break
            except:
                pass
        # get cookie
        cookie = self.browser.get_cookies()
        f = open(self.cookie_path, 'wb')
        f.write(pickle.dumps(cookie))
        f.close()
        # quit
        self.browser.close()
        return

    def init_browser(self):
        # 返回当前进程的工作目录
        self.downloadPath = os.getcwd()
        # 检索当前目录下的chromeDriver
        CHROME_DRIVER = os.path.abspath(os.path.dirname(os.getcwd())) + os.sep + 'chromedriver' + os.sep
        if platform.system() == 'Windows':
            CHROME_DRIVER = os.getcwd() + os.sep + 'chromedriver.exe'
        if platform.system() == 'Linux':
            CHROME_DRIVER = os.getcwd() + os.sep + 'chromedriver'
        """
        初始化selenium浏览器
        :return:
        """
        options = Options()
        # options.add_argument("--headless")
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # 1是加载图片，2是不加载图片
        prefs = {"profile.managed_default_content_settings.images": 1, 'download.default_directory': self.downloadPath}
        options.add_experimental_option("prefs", prefs)
        # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation']) 
        # 代理地址
        options.add_argument('--proxy-server=http://127.0.0.1:9000')
        # 禁止显示导航栏
        options.add_argument('disable-infobars')
        # 初始化窗口最大
        options.add_argument('--start-maximized')
        # ？？
        options.add_argument('--no-sandbox')
        # # 保持窗口不要退出
        # options.add_experimental_option("detach", True)

        # 启动浏览器
        self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)
        self.browser.implicitly_wait(1)


class Proxy():
    def __init__(self):
        thread = threading.Thread(target =  self.start)
        # thread.setDaemon(True)
        thread.start()

    def start(self):
        os.system("mitmdump -s HttpProxy.py -p 9000")

class Time():
    def __init__(self):
        pass
    def get_time(self):
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M')

    def time_arrived(self, time):
        self.time_gap(time)
        if self.gap <= 0:
            return True
        return False
    
    def time_less_than_120s(self, time):
        self.time_gap(time)
        if self.gap <= 120:
            return True
        return False
    def time_gap(self, time):
        now_year=datetime.now().strftime('%Y-')
        time = str(now_year) + time
        time = datetime.strptime(time,'%Y-%m-%d %H:%M')
        self.gap = (time - datetime.now()).seconds

def isElementExist(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
        return True
    except:
        print('ERROR CANNOT FIND ELEMENT %s'%xpath)
        return False

app = APP()
app.mainloop()