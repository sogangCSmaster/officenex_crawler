
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta, date
import re
import json
from selenium import webdriver

startPage = 1

# FIX ================
endPage = 1
url = "http://www.officenex.com/cate/cateItemList.do?cateId=27200005910675&rowLevel=2"
categoryName = "PP화일"
# END FIX ============

# DRIVER PATH
driverPath = './chromedriver/mac/chromedriver'
driver = webdriver.Chrome(driverPath)

# Product Name List
productNameList = []

# CRAWL START
for page in range(startPage, endPage+1):
    driver.get(url + "&currentPageNo=" + str(page))
    driver.implicitly_wait(3)
    response = driver.page_source
    soup = BeautifulSoup(response, "html.parser")

    itemList = soup.find_all('li', {'class': 'goods_md'})
    for item in itemList:
        productName = item.find('a').text
        productName = productName.split('(')[0]
        productName = productName.strip()
        if productName not in productNameList:
            productNameList.append(productName)

driver.quit()
with open(categoryName + ".txt", "w") as txt_file:
    for line in productNameList:
        txt_file.write(line + "\n")