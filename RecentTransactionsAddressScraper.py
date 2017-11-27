#import libraries
from lxml import html
from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup


columns = {'Address', 'EthBal', 'LrcBal'}
data = pd.DataFrame(columns=columns)

website = "http://etherscan.io/address/"
browser = webdriver.PhantomJS(executable_path='c:/phantomjs/bin/phantomjs.exe')

page = 1
total = 0

while page<100000:
    
    txnWebsite = "https://etherscan.io/txs?p=" + str(page)
    browser.get(txnWebsite)
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
        if len(i) ==42 and "0x" in i:
            addresses.append(i)
    
    for adr in addresses:
        
        webadr = website+adr
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
    #    #%%
    #    date = tree.xpath('//*[@id="transactions"]/div/div/table/tbody/tr[2]/td[3]/span/text()')
    #    
    #    if len(date) > 0:
    #        date = str(date[0])
    #        date = date.replace(",","")
    #        date = date.replace("days","")
    #        date = date.replace(" ","")
    #        date = date.replace("'","")
    #        date = int(date)
    #    else:
    #        date = 666
        
        #%%
        if (balance>=5 and balance<=50000):
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
                if adr not in data.Address:
                    row = pd.Series([adr, balance, lrc], index=['Address', 'EthBal', 'LrcBal'])
                    data = data.append(row, ignore_index=True)
                    total = total+1
                    print("Addresses Found" + str(total))

    page = page+5






