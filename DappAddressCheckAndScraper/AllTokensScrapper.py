# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:32:43 2017

@author: Khera
"""

#import libraries
from lxml import html
from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup

columns = {'Address', 'Bits', 'Symbol','Name'}
data = pd.DataFrame(columns=columns)
#%%
browser = webdriver.PhantomJS(executable_path='c:/phantomjs/bin/phantomjs.exe')
website = "http://coinmarketcap.com/tokens/views/all/"

browser.get(website)
time.sleep(5)

html_source = browser.page_source
#%%
soup = BeautifulSoup(html_source, 'lxml') 
table = soup.select('tr')
 
#for i in table:
#    print(i)
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
#%%
etherlist = []
for i in range(len(s)):
    if i >0:
        j = s[i].split(" ")
        if j[4] == "Ethereum":
            etherlist.append(j)


#%%
FinalList = []
for i in etherlist:
    print(i)
    try:
        
        j = []
        website = "http://etherscan.io/token/" +i[2]
        
        browser.get(website)
        time.sleep(1)
        
        html_source = browser.page_source
        tree = html.fromstring(html_source)
        bits = tree.xpath('//*[@id="ContentPlaceHolder1_trContract"]/td[2]/a')
        adr = bits[0].text
        
        website = "http://etherscan.io/"
        webAddress = website+"readcontract?a="+adr
        browser.get(webAddress)
        
        bits = tree.xpath('//td/text()')
        decimal = ""
        for i in range(len(bits)):
            bits[i] = bits[i].lower()
            if ('decimal' in bits[i]):
                decimal = decimal + bits[i+1]
                decimal = decimal.replace(" ", "")
                decimal = decimal.lower()
        
        j.append(adr)
        j.append(int(decimal))
        j.append(i[2])
        j.append(i[3])
        row = pd.Series([j[0], j[1], j[2], j[3]], index=['Address', 'Bits', 'Symbol','Name'])
        data = data.append(row, ignore_index=True)

    except:
        pass
    
            
data.to_csv("MegaListofTokens.csv")