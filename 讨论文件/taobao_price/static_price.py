'''
此程序将会根据给出的一个淘宝url链接爬取该链接下商品的价格，若无则返回ERROR.
由于淘宝的反爬机制，该程序需要输入cookie!!
This program will print the price of the goods with the given URL in TaoBao,
if the goods does not exist or cannot find the price, then return ERROR.
This program need entering the cookie manually!!
时间:2021/01/04
Time: 2021/01/04
Author: Yanyun Wu   1079042305@qq.com
Version: 1.0
'''

import requests
import re

url = 'https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w4004-22707274114.3.172014eemIictQ&pvid=6d9efb1b-e0d8-46d6-ab81-d154e8822ece&pos=2&acm=03068.1003.1.702815&id=616400172998&scm=1007.12941.156882.100200300000000&skuId=4519189046027'

def getHTMLText(url):
    try:
        kv = {'cookie': "hng=CN%7Czh-CN%7CCNY%7C156; t=beb814789db2e3d1df8ab388bdfbc439; cookie2=22996317119dd747b4bd73b941ac6021; enc=kBupAcE10zeQDqEGAgeGJp9IEWtoN7t%2FJYvMY8ibYeALKqP%2BHt4XKDWIUPXUOsdUHoldwTmbeZekBAGVgyDOmQ%3D%3D; xlly_s=1; cna=lpBUGEKyMycCAYFejpyeS6qt; _m_h5_tk=488f7b4678bf64ef4b5b2228be116cab_1609754661385; _m_h5_tk_enc=bd3d15cb85b29a739c913d35b1be85d7; _tb_token_=e4b831ead5e8e; cq=ccp%3D0; pnm_cku822=098%23E1hvh9vUvbpvUpCkvvvvvjiWP2cwlji8RFcOljnEPmPWAjnHPL5Z6jYVRLcZAjrmR29CvvpvvhCv29hvCvvvvvmgvpvIMMYvSMMMvPGvvhXVvvvC4pvvByOvvUhQvvCVB9vv9BQvvhXhvvmCj49Cvv9vvhhzWt8CfO9CvvOCvhE2gnQUvpCWvCWVC30xhE%2BaRoxBlwyzhboJEcqwaBTAdX9aWqVxnqWTnjYn6Wpae1kOwxzXSfpAhC3qVUcn%2B3vwjLEc6aZtn1m6NB3rt8gJ%2Bul08QvCvvOv9hCvvvmevpvhvvCCBv%3D%3D; tk_trace=1; dnk=myluckymh; uc1=cookie14=Uoe0ZNHCONUFww%3D%3D&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie21=VFC%2FuZ9ainBZ&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&pas=0&existShop=true; uc3=vt3=F8dCuAAmefpBnn84La0%3D&id2=UU8OcxizyAH94g%3D%3D&nk2=DkmoijuG6M%2BG&lg2=UIHiLt3xD8xYTw%3D%3D; tracknick=myluckymh; lid=myluckymh; uc4=nk4=0%40DCzaWCbQZX%2Bkbip5iRFYlHh18zY%3D&id4=0%40U22Jog%2FoSUW%2F8aTxGT7EC0yxV%2BFq; _l_g_=Ug%3D%3D; unb=2762806893; lgc=myluckymh; cookie1=UU6p%2FKxprUJX4vIX2mzU0HqtOlq7KIg94n2J8nhPipY%3D; login=true; cookie17=UU8OcxizyAH94g%3D%3D; _nk_=myluckymh; sgcookie=E100NUf48U96vbxr0ZDguU3sgagWhcgBbNTkQzQcH7VerPHROniMCs5Z1ADjU6ZQARUY9wtubW3lbXjr5z%2F7mmSy6Q%3D%3D; sg=h37; csg=cbfbaf75; tfstk=cfV1BwXIThx10wX2_P_Euyxw8mG1arSI-OiT5RcIQYMGZU4svsmHa0_zK-xH9Y3C.; l=eBjBu8FRO2VSu0aLBO5CFurza77TqIRb8sPzaNbMiInca6NPwH17uNQ2ubgDkdtj_tCf5etrJmGnAdQ0j3Ud0lB6rw1REpZZ3xJO.; isg=BMXFP-LhNrbEWBIHzm-liu5r1AH_gnkUgiuxYscqSvxOXuTQj9LF5UV8bIqoHpHM",
              'user-agent': "Mozilla/5.0"}
        r = requests.get(url, headers = kv)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('ERROR in getHTMLText')
        return ""

def grabInfo(infoList, html):
    try:
        price = re.findall(r'\"price\"\:\"[\d\.]*\"', html)
        title = re.findall(r'\<title\>.*?',html)
        price = eval(price[0].split(':')[1])
        title = title[0].split('<title>')[1]
        infoList.append(title)
        infoList.append(price)
    except:
        print('ERROR in grabInfo')

def printInfo(infoList):
    typo = "{:8}\t{:40}"
    print(typo.format('商品价格', '商品名称'))
    print(typo.format(infoList[1], infoList[0]))

################# API #########################
def getPrice(infoList):
    return infoList[1]

def getName(infoList):
    return infoList[0]

################# Main #####################
def main():
    infoList = []
    html = getHTMLText(url)
    grabInfo(infoList, html)
    printInfo(infoList)

if __name__ == '__main__':
    main()