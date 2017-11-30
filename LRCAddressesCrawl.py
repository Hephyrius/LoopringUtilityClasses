# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 11:57:48 2017

@author: Khera
"""

from lxml import html
from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup

website = "https://etherscan.io/token/generic-tokenholders2?a=0xEF68e7C694F40c8202821eDF525dE3782458639f&p="
browser = webdriver.PhantomJS(executable_path='c:/phantomjs/bin/phantomjs.exe')

columns = {'LrcAddress'}
data = pd.DataFrame(columns=columns)

page = 1

while page<=302:
    print(str(page))
    crawlSite = website + str(page)
    browser.get(crawlSite)
    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml') 
    table = soup.select('a')
    
    s = []
    for i in table:
        m = ""
        for j in i.strings:
            k = str(j)
            k = k.replace(" ", "")
            k = k.replace("\n", ".")
            m = m+k
        m = m.split('.')
        l = ""
        for j in m:
            if len(j) > 0:
                l = l + " " + j
        print(l)
        s.append(l)
    
    addresses = []
    for i in s:
        i=i.replace(" ","")
        if len(i) ==42 and "0x" in i and i != "0xEF68e7C694F40c8202821eDF525dE3782458639f":
            if (i in addresses) == False:
                addresses.append(i)
    
    for adr in addresses:
        row = pd.Series([adr], index=['LrcAddress'])
        data = data.append(row, ignore_index=True)
    
    data = data.drop_duplicates(subset = 'LrcAddress', keep='first')
    data.to_csv("lrcHoldersAddresses.csv", index=False)
    page = page + 1
                