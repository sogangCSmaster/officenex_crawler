
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta, date
from selenium import webdriver
import json
import csv


startPage = 1
endPage = 4 # Fix this

url = "http://www.officenex.com/cate/cateItemList.do?cateId=27200005910066&rowLevel=2&listSortNo=&listType=&itemId=&brandIds=&searchBrandId=&kw=&cboCateLevel1=27200005910024&cboCateLevel2=27200005910066&currentPageNo=" # Fix this
category = "복사용지/지류/컬러(OA)용지" # Fix this


location_driver = './chromedriver/mac/chromedriver'
driver = webdriver.Chrome(location_driver)
# driver.get(url)
# driver.implicitly_wait(3)

for page in range(startPage, endPage+1):
    driver.get(url + str(page))
    driver.implicitly_wait(3)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    itemList = soup.find_all('li', {'class': 'goods_md'})
    for item in itemList:
        productName = item.find('a').text
        productName = productName.split('(')[0]
        productName = productName.strip()
        print(productName)