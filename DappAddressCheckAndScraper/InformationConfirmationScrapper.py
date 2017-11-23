# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 2017
@author: Harnick Khera
"""

#script iterates over a list of ethereum based adresses and 
#then uses etherscanner in order to extract the relevant values
#
#easiest way to execute script is to install anaconda as 
#it comes with most required libraries
#but command will need to be run : pip install selenium
#
#PhantomJS driver will need to be installed.
#http://phantomjs.org/

#import libraries
from lxml import html
from selenium import webdriver
import pandas as pd
import time

#web related data
addresses=pd.read_csv("data/tokens.txt",delimiter=",")
#website = "http://etherscan.io/address/"
website = "http://etherscan.io/"
browser = webdriver.PhantomJS(executable_path='c:/phantomjs/bin/phantomjs.exe')

#prepare the data table for storage
columns = {'Address', 'Decimal', 'Symbol','Name', 'Correct'}

#%%
data = pd.DataFrame(columns=columns)


for rownumber, row in addresses.iterrows():
    
    print(rownumber)
    ads = row.values
    adds = ads[0]
    address = "" + adds
    webAddress = website+"readcontract?a="+address
    browser.get(webAddress)
    time.sleep(10)
    
    html_source = browser.page_source
    
    tree = html.fromstring(html_source)
    l = ""
    bits = tree.xpath('//td/text()')
    name = ""
    symbol = ""
    decimal = ""
    for i in range(len(bits)):
        
        bits[i] = bits[i].lower()
        
        if('name' in bits[i]):
            name = name+bits[i+1]
            name =name.replace(" ", "")
            name = name.lower()
        elif ('symbol' in bits[i]):
            symbol = symbol + bits[i+1] 
            symbol = symbol.replace(" ", "")
            symbol = symbol.lower()
        elif ('decimal' in bits[i]):
            decimal = decimal + bits[i+1]
            decimal = decimal.replace(" ", "")
            decimal = decimal.lower()
            
    print(address)
    print(decimal)
    decimal = int(decimal)
    print(name)
    print(symbol)
    
    cor = 0
    if(address == ads[0] and decimal == ads[1] and symbol == ads[2] and ads[3] in name):
        print(""+str(rownumber) +" correct")
        cor = 1
    else:
        print(""+str(rownumber) +" INCORRECT!!!")
    
    row = pd.Series([address, decimal, symbol, name, cor], index=['Address', 'Decimal', 'Symbol', 'Name', 'Correct'])
    
    data = data.append(row, ignore_index=True)

data.to_csv("Data/output.csv")