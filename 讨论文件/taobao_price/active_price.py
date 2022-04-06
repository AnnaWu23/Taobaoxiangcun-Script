'''
此程序将会根据给出的淘宝购物车链接爬取购物车中商品的信息
由于淘宝的反爬机制，该程序需要输入cookie!!
This program will print the price of the goods with the given URL in TaoBao,
if the goods does not exist or cannot find the price, then return ERROR.
This program need entering the cookie manually!!
时间:2021/01/05
Time: 2021/01/05
Author: Yanyun Wu   1079042305@qq.com
Version: 2.0
该版本解决了促销价格抓取的问题, 通过抓取购物车的静态网页来获取商品信息
'''

import requests
import re
from random import choice

USER_AGENTS = [
"Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
"Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
"Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
"Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
"Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 ",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
]

COOKIE = [
"thw=cn; t=beb814789db2e3d1df8ab388bdfbc439; hng=CN%7Czh-CN%7CCNY%7C156; ubn=p; ucn=center; cna=lpBUGEKyMycCAYFejpyeS6qt; lgc=myluckymh; tracknick=myluckymh; enc=aFitBsUlNuNHFYeUwTH4kJhCmmEJPio5TEfpV6QZhwyTek3KytgnQgRD5paR8zf9%2FhzeK%2B9n6KQy3KRkXRYpDA%3D%3D; _m_h5_tk=87753abd2bf39bfcae841a66bbe7f2f8_1609993997182; _m_h5_tk_enc=5dc4be6a37a29b16cb68240c64083bcd; xlly_s=1; cookie2=1c86cd2aad52501e5885e876b28a1782; _tb_token_=e5fbbe3e11b4e; _samesite_flag_=true; sgcookie=E100mErbAFoIrKLVgHfSBEtXXKqy9jdYpoZKAzq4nWbfLskux9JXI%2FSbKVhgSFr1%2FNAbFa9AQJtQOym7C7sP8cqi6Q%3D%3D; unb=2762806893; uc3=id2=UU8OcxizyAH94g%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=DkmoijuG6M%2BG&vt3=F8dCuAAgSJPEBoV412I%3D; csg=b4f16bda; cookie17=UU8OcxizyAH94g%3D%3D; dnk=myluckymh; skt=4d6d4e3f155202b4; existShop=MTYwOTk4NjA4NA%3D%3D; uc4=id4=0%40U22Jog%2FoSUW%2F8aTxGT7EBY0gy67N&nk4=0%40DCzaWCbQZX%2Bkbip5iRFWLLKb0Ec%3D; _cc_=WqG3DMC9EA%3D%3D; _l_g_=Ug%3D%3D; sg=h37; _nk_=myluckymh; cookie1=UU6p%2FKxprUJX4vIX2mzU0HqtOlq7KIg94n2J8nhPipY%3D; mt=ci=58_1; uc1=existShop=true&cookie14=Uoe0ZN%2FdB6bZNg%3D%3D&cart_m=0&cookie21=VFC%2FuZ9ainBZ&pas=0&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D; isg=BDw8S_6PTzrtY3szep1nfutvDdruNeBfI8QYKRa9SCcK4dxrPkWw77JTxQGZshi3; l=eBQ0dI4rO2gFJFWDBOfanurza77OSIRYYuPzaNbMiOCPO2fB5o5PWZ8S_0Y6C3GNh6JkR3uKcXmBBeYBqQAonxvOUKaOYMkmn; tfstk=c8lNBS9CXCdZeXVXe5NVhg37ES3OwTgio6z7IxtcMq_xLPfDdiU3P6UUlud3I",
"hng=CN%7Czh-CN%7CCNY%7C156; t=beb814789db2e3d1df8ab388bdfbc439; cookie2=22996317119dd747b4bd73b941ac6021; cna=lpBUGEKyMycCAYFejpyeS6qt; tk_trace=1; login=true; xlly_s=1; _l_g_=Ug%3D%3D; cq=ccp%3D0; _m_h5_tk=b4aabed1e32cb4be0ba20cbd6477fc35_1609818212445; _m_h5_tk_enc=fe877ce455a4ac90af1ebae2b18b8ef5; _tb_token_=7eb1e85373b67; dnk=sanctifieral; uc1=cookie14=Uoe0ZN5ngw%2FAIg%3D%3D&pas=0&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&existShop=false&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie21=UIHiLt3xThH8t7YQoFNq; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&nk2=EF8fRrBtzpL5%2FPFL&id2=UUjUKIcrShjr3g%3D%3D&vt3=F8dCuAAhL%2BuF2mszE7I%3D; tracknick=sanctifieral; lid=sanctifieral; uc4=id4=0%40U2o29R1VYk9Cqx4Va4nYKpkoLQYr&nk4=0%40EoZgGPemyONAtifGlsVcZ1kilcgeCpo%3D; unb=2052084544; lgc=sanctifieral; cookie1=BqtZyKdExt%2BrDqHheeYkUbVQ5Na%2B%2FOQe5WUmJgHvUx4%3D; cookie17=UUjUKIcrShjr3g%3D%3D; _nk_=sanctifieral; sgcookie=E100rLbC8uf%2BqJ9veXrDp7fsWu5Pgdn6uSwMAOkcqZZEqbHVzSu9gi4Tto7WCM5wg5rqVMkOjpXQVRXnKo%2BGzOVLQQ%3D%3D; sg=l4d; csg=ad7d5468; enc=Pmkl%2FG4FK%2FdzfBRRFalXxT3%2BZdoD1HYnu9fIGjagvu7LEwEOszoMoiiBMC0zczMcdvWvgL8yCoZ8bQdKHITOEw%3D%3D; sm4=511102; pnm_cku822=098%23E1hvv9vUvbpvUvCkvvvvvjiWP2c91jiEPsdUljEUPmP9zjiPPFqw1jlHRL5vAjnbi9hvCvvvpZogvpvIMMYvSMMMvPGvvhXVvvvC4pvvByOvvUhQvvCVB9vv9BQvvhXhvvmCjO9CvvOCvhE2gnAIvpvUvvCCn6P%2BLkUUvpCW9Urmp30UHd8reB69kU97%2Bu0Ojo2v%2BboJe3iQBb2XrqpAhjCbFO7t%2B3mOaysEDLuTRLa9C7zOdiTAdcvrKU66%2B2e3b6KxCLIZ%2Bul68pvCvvOv9hCvvvvRvpvhvv2MMs9CvvpvvhCv; tfstk=cRV5B2Xjg3xWgKWeaz_q8fjYT4lOZ2IjoTi8P8DKqphda0a5ifAZfNy0KnAxBq1..; l=eBjBu8FRO2VSuEVoKOfwnurza77t_IRAguPzaNbMiOCPOc1e5sFRWZ8mzbYwCnGNh64kR3uKcXmBBeYBqnvpBkyca6Fy_CMmn; isg=BCMjE8RLePkkVjShvAU7FHyhsmfNGLdasLEXhFWAZQL5lEO23esXq-bGimyaNA9S",
"thw=cn; t=beb814789db2e3d1df8ab388bdfbc439; cookie2=22996317119dd747b4bd73b941ac6021; _samesite_flag_=true; hng=CN%7Czh-CN%7CCNY%7C156; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5v3ihMmIhO3UBh3wmViYjJAhiEnXGlw6XqqvYdmTNw17RYQ4bNaYjuq7UXlU8F18uN09aMe3JeG5PVgS%2BMWguhyRn00wB1VKwAOMbu%2FGpy%2BosZ3kW8zwI1PdUEVPA5%2B4yVKt%2FL9v7SeBwhhSn%2Bgsui9fY5p%2FbgNaXI0XX2sQKjVu8Zlb1vuvZF3SPych%2FAN%2BnCjTB5AIlySxieATkA8RADBXyUwFNKOUkzY3GimS3y8WBKTLPovy%2FdlrYc%3D; lLtC1_=1; xlly_s=1; oa2=42a2849599a7f58156ae542b29ec7e30; _tb_token_=7eb1e85373b67; cna=lpBUGEKyMycCAYFejpyeS6qt; unb=2052084544; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&nk2=EF8fRrBtzpL5%2FPFL&id2=UUjUKIcrShjr3g%3D%3D&vt3=F8dCuAAhL%2BuF2mszE7I%3D; csg=ad7d5468; lgc=sanctifieral; cookie17=UUjUKIcrShjr3g%3D%3D; sgcookie=E100rLbC8uf%2BqJ9veXrDp7fsWu5Pgdn6uSwMAOkcqZZEqbHVzSu9gi4Tto7WCM5wg5rqVMkOjpXQVRXnKo%2BGzOVLQQ%3D%3D; dnk=sanctifieral; skt=f3634f19fbea6a3e; existShop=MTYwOTgxMTE2Mw%3D%3D; uc4=id4=0%40U2o29R1VYk9Cqx4Va4nYKpkoLQYr&nk4=0%40EoZgGPemyONAtifGlsVcZ1kilcgeCpo%3D; tracknick=sanctifieral; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=l4d; _nk_=sanctifieral; cookie1=BqtZyKdExt%2BrDqHheeYkUbVQ5Na%2B%2FOQe5WUmJgHvUx4%3D; enc=58nwMnEPUE33f7tliNI%2FNSfKuzhxFtKfsIKD00tTJKcs%2Fe5TQSzgsprsoZL%2BmkbGpRd6rHeuMwkO2agmdfefNw%3D%3D; mt=ci=105_1; v=0; uc1=cookie14=Uoe0ZN5ngwxiig%3D%3D&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=V32FPkk%2FgihF%2FS5nr3O5; _m_h5_tk=06a9965afcb80975c8d6acb4a1fffa83_1609821209797; _m_h5_tk_enc=fa08d30bc20a7a7c2af88e32c2c85bb2; tfstk=c5EfBObS4IAX_cbw0-6rQDq8lqiAZB1SEZGYhr0tN1hM8fwfi4xEO9zuSQx-JY1..; l=eBQ0dI4rO2gFJ5-BBOfZnurza77TIIRAguPzaNbMiOCPO91WRpxFWZ8mPMTXCnGNhsMHR3uKcXmBBeYBqnqIdJfZe5DDwQDmn; isg=BGdnQgw49I1D0HBSlTTsT1zm9psx7DvO1N1TSDnUiPYUKIfqQb7UHk4qTiC2wBNG",
"thw=cn; t=beb814789db2e3d1df8ab388bdfbc439; cookie2=22996317119dd747b4bd73b941ac6021; _samesite_flag_=true; hng=CN%7Czh-CN%7CCNY%7C156; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5v3ihMmIhO3UBh3wmViYjJAhiEnXGlw6XqqvYdmTNw17RYQ4bNaYjuq7UXlU8F18uN09aMe3JeG5PVgS%2BMWguhyRn00wB1VKwAOMbu%2FGpy%2BosZ3kW8zwI1PdUEVPA5%2B4yVKt%2FL9v7SeBwhhSn%2Bgsui9fY5p%2FbgNaXI0XX2sQKjVu8Zlb1vuvZF3SPych%2FAN%2BnCjTB5AIlySxieATkA8RADBXyUwFNKOUkzY3GimS3y8WBKTLPovy%2FdlrYc%3D; lLtC1_=1; xlly_s=1; oa2=42a2849599a7f58156ae542b29ec7e30; _tb_token_=7eb1e85373b67; enc=58nwMnEPUE33f7tliNI%2FNSfKuzhxFtKfsIKD00tTJKcs%2Fe5TQSzgsprsoZL%2BmkbGpRd6rHeuMwkO2agmdfefNw%3D%3D; _m_h5_tk=06a9965afcb80975c8d6acb4a1fffa83_1609821209797; _m_h5_tk_enc=fa08d30bc20a7a7c2af88e32c2c85bb2; cna=lpBUGEKyMycCAYFejpyeS6qt; sgcookie=E100KAaZXw3xtHlGmbZuQ6Mfi%2BZ1goC3YrZoIAzpwX9Ce%2FXg%2FOYY47bqKexJJgck0bTRbytT6fqZCmAnOe5M7wrWFA%3D%3D; unb=2052084544; uc3=vt3=F8dCuAAhL%2BuCoS0OWhw%3D&nk2=EF8fRrBtzpL5%2FPFL&id2=UUjUKIcrShjr3g%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; csg=880c0131; lgc=sanctifieral; cookie17=UUjUKIcrShjr3g%3D%3D; dnk=sanctifieral; skt=1ca9f05f1a61c689; existShop=MTYwOTgxMTYzNg%3D%3D; uc4=id4=0%40U2o29R1VYk9Cqx4Va4nYKpkoKi3h&nk4=0%40EoZgGPemyONAtifGlsVcZ1kilcgZPAw%3D; tracknick=sanctifieral; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=l4d; _nk_=sanctifieral; cookie1=BqtZyKdExt%2BrDqHheeYkUbVQ5Na%2B%2FOQe5WUmJgHvUx4%3D; mt=ci=105_1; uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie14=Uoe0ZN5ngwieeA%3D%3D&cookie15=UtASsssmOIJ0bQ%3D%3D&cookie21=V32FPkk%2FgihF%2FS5nr3O5&pas=0; isg=BIqKZLu94Tb2s23J-AP5pMmJ23Asew7VQeJucxTDO11oxyqB_Aoq5RY11zsbN4Zt; l=eBQ0dI4rO2gFJkC9BOfanurza77OSIRYYuPzaNbMiOCPOb1B5I_NWZ8mPkT6C3GNh6lDR3uKcXmBBeYBqQAonxvtIosM_Ckmn; tfstk=cTdGB0AxSdWsHx6HFf16r-oqOjlRwLDNfIReTBNM4mt3IR5m9JyPh83hXhAYh",
"thw=cn; t=beb814789db2e3d1df8ab388bdfbc439; cookie2=22996317119dd747b4bd73b941ac6021; _samesite_flag_=true; hng=CN%7Czh-CN%7CCNY%7C156; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5v3ihMmIhO3UBh3wmViYjJAhiEnXGlw6XqqvYdmTNw17RYQ4bNaYjuq7UXlU8F18uN09aMe3JeG5PVgS%2BMWguhyRn00wB1VKwAOMbu%2FGpy%2BosZ3kW8zwI1PdUEVPA5%2B4yVKt%2FL9v7SeBwhhSn%2Bgsui9fY5p%2FbgNaXI0XX2sQKjVu8Zlb1vuvZF3SPych%2FAN%2BnCjTB5AIlySxieATkA8RADBXyUwFNKOUkzY3GimS3y8WBKTLPovy%2FdlrYc%3D; lLtC1_=1; ubn=p; ucn=center; xlly_s=1; oa2=42a2849599a7f58156ae542b29ec7e30; enc=58nwMnEPUE33f7tliNI%2FNSfKuzhxFtKfsIKD00tTJKcs%2Fe5TQSzgsprsoZL%2BmkbGpRd6rHeuMwkO2agmdfefNw%3D%3D; _m_h5_tk=06a9965afcb80975c8d6acb4a1fffa83_1609821209797; _m_h5_tk_enc=fa08d30bc20a7a7c2af88e32c2c85bb2; cna=lpBUGEKyMycCAYFejpyeS6qt; sgcookie=E100KAaZXw3xtHlGmbZuQ6Mfi%2BZ1goC3YrZoIAzpwX9Ce%2FXg%2FOYY47bqKexJJgck0bTRbytT6fqZCmAnOe5M7wrWFA%3D%3D; unb=2052084544; uc3=vt3=F8dCuAAhL%2BuCoS0OWhw%3D&nk2=EF8fRrBtzpL5%2FPFL&id2=UUjUKIcrShjr3g%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; csg=880c0131; lgc=sanctifieral; cookie17=UUjUKIcrShjr3g%3D%3D; dnk=sanctifieral; skt=1ca9f05f1a61c689; existShop=MTYwOTgxMTYzNg%3D%3D; uc4=id4=0%40U2o29R1VYk9Cqx4Va4nYKpkoKi3h&nk4=0%40EoZgGPemyONAtifGlsVcZ1kilcgZPAw%3D; tracknick=sanctifieral; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=l4d; _nk_=sanctifieral; cookie1=BqtZyKdExt%2BrDqHheeYkUbVQ5Na%2B%2FOQe5WUmJgHvUx4%3D; mt=ci=105_1; v=0; uc1=cookie14=Uoe0ZN5nhiwJOg%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=VT5L2FSpccLuJBreK%2BBd&existShop=false&pas=0&cookie15=UIHiLt3xD8xYTw%3D%3D; _tb_token_=e548bee88667b; isg=BA8PVos-jPUw54harXwExySenqMZNGNWvJWLQCEdwH6F8C7yKATLpn2h8ijOiDvO; l=eBQ0dI4rO2gFJZnTBO5Churza77T5IOb8sPzaNbMiInca6ih1FaMTNQ2oDJ2Rdtj_tCAaeKrJmGnARdlO3jR2xDDBYFinQnnFxJO.; tfstk=cp3PBixfeULrgzUBXzaFARFV65VRaJe3CZPaqD9kZo958eEQQsqNpSV1kSPUBEql."
]

url = 'https://cart.taobao.com/cart.htm?t=1609822441959'

################# Main #####################
def main():
    infoList = []
    html = getHTMLText(url)
    grabInfo(infoList, html)
    printInfo(infoList)

################### HELPER FUNCTION #######################
'''
通过给出的url抓取网页源代码
'''
def getHTMLText(url):
    # 如果农村淘宝，getCookie = 0, 如果天猫或淘宝，getCookie = 1
    head = {'cookie': getCookie(0), 'user-agent': getRandUA()}
    try:
        r = requests.get(url, headers = head, timeout=30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('ERROR in getHTMLText')
        return ""

# 解析购物车中物品名称以及价格
'''
解析静态网页源代码
'''
def grabInfo(infoList, html):
    try:
        pl = re.findall(r'\"price\"\:\{\"actual\"\:.*?\"oriPromo', html)
        tl = re.findall(r'\"skuId\".*?\"\,\"toBuy\"',html)
        priceList = []
        titleList = []
        for item in pl:
            price = item.split('"now":')[1]
            price = price.split(',"oriPromo')[0]
            priceList.append(price)
        for item in tl:
            title = item.split('"title":"')[1]
            title = title.split('","toBuy"')[0]
            titleList.append(title)
        if len(priceList) != len(titleList):
            print('Unbalanced List')
            return
        infoList.append(priceList)
        infoList.append(titleList)
    except:
        print('ERROR in grabInfo')

'''
打印商品信息
'''
def printInfo(infoList):
    typo = "{:3}\t{:8}\t{:40}"
    try:
        print(typo.format('序号', '商品价格', '商品名称'))
        for i in range(0, len(infoList[0])):
            print(typo.format(i+1, infoList[0][i], infoList[1][i]))
    except:
        print("ERROR in printInfo")

'''
随机选择一个user-agent
'''
def getRandUA():
    return choice(USER_AGENTS)

'''
根据不同的平台选择cookie，如果是农村淘宝则为0，如果是天猫则为1，如果是淘宝则为2，登录cookie为3
'''
def getCookie(num):
    return COOKIE[num]

################# API #########################
def getPrice(infoList):
    return infoList[1]

def getName(infoList):
    return infoList[0]

if __name__ == '__main__':
    main()