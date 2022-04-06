'''
此程序将会根据给出的淘宝购物车链接爬取购物车中商品的信息
This program will print the price of the goods with the given URL in TaoBao,
if the goods does not exist or cannot find the price, then return ERROR.
This program need entering the cookie manually!!
时间:2021/01/07
Time: 2021/01/07
Author: Yanyun Wu   1079042305@qq.com
Version: 3.0
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

import os

from mitmproxy.tools._main import mitmdump


cartURL = 'https://cart.taobao.com/cart.htm?t=1609822441959'
loginURL = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fcart.taobao.com%2Fcart.htm'

class Login():
    def __init__(self, account, password):
        self.browser = None
        self.account = account
        self.password = password
    
    def start(self):
        # 0 自动运行代理
        # mitmdump(args=['-s', './HttpProxy.py', '-p', '9000'])
        # 1 初始化浏览器
        self.init_browser()
        # 2 打开淘宝登录页
        self.browser.get(loginURL)
        sleep(3)
        # 3 输入用户名
        self.write_username(self.account)
        sleep(1.5)
        # 4 输入密码
        self.write_password(self.password)
        sleep(1.5)
        # 5 如果有滑块 移动滑块
        if self.lock_exist():
            self.unlock()
        # 6 点击登录按钮
        self.submit()
        # 7 登录成功，直接请求页面
        print("登录成功，跳转至目标页面")
        sleep(3.5)

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
    
    def write_username(self, username):
        try:
            username_input_element = self.browser.find_element_by_id('fm-login-id')
        except:
            username_input_element = self.browser.find_element_by_id('TPL_username_1')
        
        username_input_element.clear()
        username_input_element.send_keys(username)

    def write_password(self, password):
        try:
            password_input_element = self.browser.find_element_by_id("fm-login-password")
        except:
            password_input_element = self.browser.find_element_by_id('TPL_password_1')

        password_input_element.clear()
        password_input_element.send_keys(password)

    def lock_exist(self):
        return self.is_element_exist('#nc_1_wrapper') and self.browser.find_element_by_id(
            'nc_1_wrapper').is_displayed()
    
    def unlock(self):
        if self.is_element_exist("#nocaptcha > div > span > a"):
            self.browser.find_element_by_css_selector("#nocaptcha > div > span > a").click()

        bar_element = self.browser.find_element_by_id('nc_1_n1z')
        ActionChains(self.browser).drag_and_drop_by_offset(bar_element, 258, 0).perform()
        if self.is_element_exist("#nocaptcha > div > span > a"):
            self.unlock()
        sleep(0.5)

    def submit(self):
        try:
            self.browser.find_element_by_css_selector("#login-form > div.fm-btn > button").click()
        except:
            self.browser.find_element_by_id('J_SubmitStatic').click()

        sleep(0.5)
        if self.is_element_exist("#J_Message"):
            self.write_password(self.password)
            self.submit()
            sleep(5)

    def is_element_exist(self, selector):
        try:
            self.browser.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False

    def select_one_item(self):
        try:
            self.browser.find_element_by_id("J_CheckBox_2477218357746")
            sleep(4)
        except:
            print('item select failed')

account = 'myluckymh'
# 输入你的账号名
password = '57355@huili'
# 输入你密码
Login(account,password).start()
sleep(200)
