'''
此程序将会根据给出的商品名称爬取商品的价格，若无则返回ERROR.
由于淘宝的反爬机制，该程序需要输入cookie!!
This program will print the price of the given goods in TaoBao,
if the goods does not exist or cannot find the price, then return ERROR.
This program need entering the cookie manually!!
时间:2021/01/04
Time: 2021/01/04
Author: Yanyun Wu   1079042305@qq.com
Version: 0.0
'''
import requests
import re

''' 使用正则表达式获取相关内容的函数'''
def getHTMLText(url):
    kv = {'user-agent': 'Mozilla/5.0', 'cookie': "thw=cn; v=0; t=beb814789db2e3d1df8ab388bdfbc439; cookie2=22996317119dd747b4bd73b941ac6021; xlly_s=1; _samesite_flag_=true; hng=CN%7Czh-CN%7CCNY%7C156; cna=lpBUGEKyMycCAYFejpyeS6qt; sgcookie=E100c1VMaH7GnDmetjKgLlBobbRBYVKykioE4I3O338VgmRYCRfcPjTR29%2Fc7G3Wsx1Ack8z5V8g%2BlhusHuITCewPA%3D%3D; uc3=vt3=F8dCuAAn57z9op0vOkw%3D&nk2=EF8fRrBtzpL5%2FPFL&lg2=URm48syIIVrSKA%3D%3D&id2=UUjUKIcrShjr3g%3D%3D; csg=8cf72897; lgc=sanctifieral; dnk=sanctifieral; skt=f0422b74773d1200; existShop=MTYwOTY3NDg2OQ%3D%3D; uc4=id4=0%40U2o29R1VYk9Cqx4Va4nYJIYpHo35&nk4=0%40EoZgGPemyONAtifGlsVcZ1ksCb0UcnI%3D; tracknick=sanctifieral; _cc_=URm48syIZQ%3D%3D; enc=kBupAcE10zeQDqEGAgeGJp9IEWtoN7t%2FJYvMY8ibYeALKqP%2BHt4XKDWIUPXUOsdUHoldwTmbeZekBAGVgyDOmQ%3D%3D; mt=ci=-1_0; _m_h5_tk=c25e5e3ad8036e45c4783e0c55bab602_1609755022239; _m_h5_tk_enc=a55cf337ef465a7b1f4f17f7bb7d4fb4; alitrackid=world.taobao.com; lastalitrackid=world.taobao.com; JSESSIONID=678F6EC060CE32E3E7086F567FC455A5; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=false&pas=0&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie14=Uoe0ZNHDD5Lulw%3D%3D; isg=BFlZdbtMYjpjcz78V47a2T6MaEUz5k2YdsedJnsO3ADygngUwzarafWagE70OuXQ; l=eBQ0dI4rO2gFJZpEBOfwourza77tSIRfguPzaNbMiOCP9Kfp5DHPWZ8qzzL9CnGNnsMvR3uKcXmBBfTLey4eixv9-eTCgsDK3dLh.; tfstk=cJJPBMcbyYHrHRWI6T6UOOCJNY6RZeQh5-SNZBiMm4oneG5li5zdmGwA0M7tn_f..; _tb_token_=e4b831ead5e8e"}
    try:
        r = requests.get(url, headers = kv)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'ERROR in getHTMLText'

'''对每一个获得的页面进行解析'''
def parsePage(ilt, html):
    try:
        '''get price'''
        plt = re.findall(r'\"view_price\"\:"[\d\.]*\"',html)
        '''获取名字'''
        tlt = re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print("")

'''相关信息打印到屏幕上'''
def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号",'价格', '商品名称'))
    count = 0
    for g in ilt:
        count += 1
        print(tplt.format(count, g[0], g[1]))

def main():
    goods = '女鞋'
    depth = 2
    start_url = 'https://s.taobao.com/search?q=' + goods
    '''输出结果'''
    infoList = []
    '''开始爬取'''
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44*i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)

main()