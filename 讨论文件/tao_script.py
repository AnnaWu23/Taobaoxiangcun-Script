from tkinter import *
import tkinter.font as tkFont
from selenium import webdriver
import datetime
import time
# 待实现功能：
# 1. 根据订单金额对比付款
# 2. 刷新单价付款

class Gui(object):

    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        #界面参数
        self.init_window_name.title("淘宝秒杀")                                  #窗口名
        self.init_window_name.geometry('250x100')                               #窗口大小和初始出现位置
        self.init_window_name["bg"] = "bisque"                                  #窗口背景色
        #self.init_window_name.attributes("-alpha",0.9)                         #虚化，值越小虚化程度越高
        #self.init_window_name.iconbitmap("tb.ico")
        #标签
        self.label1=Label(self.init_window_name, text="请输入秒杀时间",bg='bisque',font=('隶书',13))
        self.label1.pack()
        #self.label2=Label(self.init_window_name, text="提示(●'◡'●)",bg='bisque',font=('隶书',12))
        #self.label2.place(relx=0.35,rely=0.2)
        #文本框
        self.text1=Text(self.init_window_name, width=20, height=1)
        self.text1.place(relx=0.21,rely= 0.3)
        self.text1.insert(1.0,'2020-11-02 00:00:00')                            #时间格式
        #self.text2=Text(self.init_window_name, width=60, height=20)
        #self.text2.place(relx=0.1,rely=0.25)
        #按钮
        self.button1=Button(self.init_window_name, text="开始", bg="Cornsilk", width=8,height=1,command=self.run)
        self.button1.place(relx=0.35,rely= 0.58)

    def run(self):
        """运行函数"""
        self.login()
        self.picking(0)
        times=self.text1.get(1.0,END)
        self.buy(times)
    
    def login(self):
            # 打开Chrome浏览器
            self.browser = webdriver.Chrome()
            # 打开淘宝首页，通过扫码登录
            self.browser.get("https://www.taobao.com")
            time.sleep(10)
            if self.browser.find_element_by_link_text("扫一扫登录"):
                self.browser.find_element_by_link_text("亲，请登录").click()
                time.sleep(10)


    def picking(self,method):
        # 打开购物车列表页面
        self.browser.get("https://cart.taobao.com/cart.htm")
        time.sleep(3)

        # 是否全选购物车
        #if method == 0:
        if True:
            while True:
                if self.browser.find_element_by_id("J_SelectAll1"):
                    self.browser.find_element_by_id("J_SelectAll1").click()
                    break
                else:
                    time.sleep(5)


    def buy(self,times):     #参数times为时间 格式为 2020-08-05 23:00:00
        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # 对比时间，时间到的话就点击结算
            if now > times:
                # 点击结算按钮
                while True:
                    try:
                        if self.browser.find_element_by_link_text("结 算"):
                            self.browser.find_element_by_link_text("结 算").click()
                            break
                    except:
                        pass
                # 点击提交订单按钮
                while True:
                    try:
                        if self.browser.find_element_by_link_text('提交订单'):
                            self.browser.find_element_by_link_text('提交订单').click()    
                    except:
                        pass
                time.sleep(0.01)

def gui_start():
    """运行函数"""
    init_window = Tk()              #实例化出一个父窗口
    mainpage=Gui(init_window)       # 设置根窗口默认属性
    mainpage.set_init_window()
    init_window.mainloop()          #父窗口进入事件循环


gui_start()
