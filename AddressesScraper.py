#import libraries
from lxml import html
from selenium import webdriver
import pandas as pd
import time

columns = {'Address', 'EthBal', 'LrcBal','LastTXN'}
data = pd.DataFrame(columns=columns)

website = "http://etherscan.io/address/"
browser = webdriver.PhantomJS(executable_path='c:/phantomjs/bin/phantomjs.exe')


total = 0
count = 91343852333181432387730302044767688728495783936 #change from 7 to 6
#count = 0
while total < 2000000:
    adr = hex(count)
    adr = adr.replace("0x","")
    fix = ""
    while len(adr)+len(fix)<40:
        fix = fix+"0"
    
    adr = "0x"+fix+adr
    webadr = website+adr
    print(adr)
    
    browser.get(webadr)
    html_source = browser.page_source
    tree = html.fromstring(html_source)
    ammountData = tree.xpath('//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/table/tbody/tr[1]/td[2]/text()')
    balance = str(ammountData[0])
    balance = balance.replace(" ","")
    balance = balance.replace("\\","")
    balance = balance.replace("n","")
    balance = balance.replace("\n","")
    balance = balance.replace("[","")
    balance = balance.replace("]","")
    balance = balance.replace("'","")
    balance = balance.replace(",","")
    if "wei" in balance:
        balance = 0
    else:
        balance = balance.replace("Ether","")
        balance = int(balance)
    
    print(balance)
    #%%
    date = tree.xpath('//*[@id="transactions"]/div/div/table/tbody/tr[2]/td[3]/span/text()')
    
    if len(date) > 0:
        date = str(date[0])
        date = date.replace(",","")
        date = date.replace("days","")
        date = date.replace(" ","")
        date = date.replace("'","")
        date = int(date)
    else:
        date = 666
    
    #%%
    if(date <=14) and (balance>=5 and balance<=50000):
        lrcContractBalAdr = "https://etherscan.io/token/0xef68e7c694f40c8202821edf525de3782458639f?a="+adr
        browser.get(lrcContractBalAdr)
        #time.sleep(10)
        html_source = browser.page_source
        tree = html.fromstring(html_source)
        lrcBalance = tree.xpath('//td/text()')
        lrc = ""
        for i in lrcBalance:
            if("LRC" in str(i)):
                lrc = str(i)
        
                
        lrc = str(lrc)
        lrc = lrc.replace(" ","")
        lrc = lrc.replace("\\","")
        lrc = lrc.replace("n","")
        lrc = lrc.replace("[","")
        lrc = lrc.replace("]","")
        lrc = lrc.replace("'","")
        lrc = lrc.replace("LRC", "")
        lrc = lrc.replace(",", "")
        lrc = int(lrc)
        
        if (lrc >0) == False:
            
            row = pd.Series([adr, balance, lrc, date], index=['Address', 'EthBal', 'LrcBal','LastTXN'])
            data = data.append(row, ignore_index=True)
            total = total+1
            
    count = count+1








