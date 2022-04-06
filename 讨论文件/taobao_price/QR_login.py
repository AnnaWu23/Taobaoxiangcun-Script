'''
此程序将会根据给出的淘宝购物车链接爬取购物车中商品的信息
This program will print the price of the goods with the given URL in TaoBao,
if the goods does not exist or cannot find the price, then return ERROR.
This program need entering the cookie manually!!
时间:2021/01/07
Time: 2021/01/07
Author: Yanyun Wu   1079042305@qq.com
Version: 3.0.1
该版本解决了cookie的获取问题，可以自动输入账号密码登录
本次没有采用requests库实现，而是使用selenium驱动chromeDriver模拟登陆
'''
from time import sleep
from datetime import date, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import platform

import threading
import os

from mitmproxy.tools._main import mitmdump


cartURL = 'https://cart.taobao.com/cart.htm?t=1609822441959'
loginURL = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fcart.taobao.com%2Fcart.htm'

class Login():
    def __init__(self):
        self.browser = None
        # 0 多线程自动运行代理
        Proxy()
        self.start()
        
        
    def start(self):
        # 1 初始化浏览器
        self.init_browser()
        # 2 打开淘宝登录页
        self.browser.get(loginURL)
        sleep(20)
        # 等待扫码完成后登录
        self.check_for_login_status()

        # select_one_item()
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

        # 启动浏览器
        self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)
        self.browser.implicitly_wait(3)

    def check_for_login_status(self):
        self.browser.find_element_by_xpath('//*[@id="J_SelectAll1"]/div/label').click()


class Proxy():
    def __init__(self):
        thread = threading.Thread(target=self.start)
        thread.setDaemon(True)
        thread.start()
    def start(self):
        os.system("mitmdump -s HttpProxy.py -p 9000")

Login()
