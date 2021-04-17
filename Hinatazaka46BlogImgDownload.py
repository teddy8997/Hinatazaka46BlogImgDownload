#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import time
import re
import warnings
import urllib.request
import csv
import schedule
import time
import threading
import os
import io
import sys
warnings.filterwarnings("ignore")

def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

i = 0
def downloadImg(content_list, name):
    global i
    saveDir = "./" + name +"/"
    if not os.path.isdir(saveDir):
        os.mkdir(saveDir)
    for content in content_list:
        img_list = content.findAll('img')
        for img in img_list:
            src = img['src']
            if src != '':
                tmp = requests.get(src)
                with open(saveDir+ str(i) + '.jpg', 'wb') as f:
                    f.write(tmp.content)
                print(src)
                print(i)
                i += 1
    return "OK"

def getNextURL(req_bs):
    isPrev = req_bs.find(class_= "c-pager__item--count c-pager__item--prev")
    hasNext = req_bs.find(class_= "c-pager__item--count c-pager__item--next")
    if isPrev == None or hasNext != None:
        n = req_bs.find(class_= "p-pager p-pager--count").findAll('a')
        next_href = n[len(n) - 1].get('href')
        return "https://www.hinatazaka46.com" + next_href
    elif hasNext == None: #到最後一頁時返回沒有下一頁，也就是下載完成
        return "finish"
    return "not err"




member = {"潮紗理菜": 2, "影山優佳": 4, "加藤史帆": 5, "齊藤京子": 6, "佐々木久美": 7, "佐々木美玲": 8, "高瀬愛奈": 9, "高本彩花": 10
          , "東村芽依": 11, "金村美玖": 12, "河田陽菜": 13, "小坂菜緒": 14, "富田鈴花": 15, "丹生明里": 16, "濱岸ひより": 17, "松田好花": 18
          , "宮田愛萌": 19, "渡邉美穂": 20, "上村ひなの": 21, "髙橋未来虹": 22, "森本茉莉": 23, "山口陽世": 24}


name = input('請輸入要下載的成員(一次輸入一個成員)：')
url = "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=" + str(member[name]);
html = get_html(url)
req_bs = bs(html)
content_list = req_bs.findAll(class_ = "c-blog-article__text")
flag = downloadImg(content_list, name)
next_url = getNextURL(req_bs)
hasNext = req_bs.find(class_= "c-pager__item--count c-pager__item--next")

while (hasNext != None):
    html = get_html(next_url)
    req_bs = bs(html)
    content_list = req_bs.findAll(class_ = "c-blog-article__text")
    flag = downloadImg(content_list, name)
    next_url = getNextURL(req_bs)
    hasNext = req_bs.find(class_= "c-pager__item--count c-pager__item--next")
    if next_url == "finish":
        print("All download complete!!")
    time.sleep(10)
