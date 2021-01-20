
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta, date
import re
import json
import csv


# FIX ================
startPage = 1
url = "https://www.arena.co.kr/product/new.asp?gb=F"
categoryName = "footwear"
endPage = 2
# END FIX ============

endPage = endPage + 1

f = open(categoryName + '.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

wr.writerow(["id", "제목", "설명", "링크", "상태", "가격", "할인가", "재고 수량", "이미지 링크", "gtin", "mpn", "상표", "google 상품 카테고리"])
# wr.writerow([2, "박상미", True])


# CRAWL START
for page in range(startPage, endPage):
    print(url + "&page=" + str(page))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url + "&page=" + str(page), headers=headers, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    
    products = soup.find('ul', {'id': 'productList'})
    products = products.find_all('li', {'class': 'col-3'})
    for product in products:
        try:
            card = product.find('div', {'class', 'card'})
            aTag = card.find('a')
            link = aTag['href']
            link = "https://www.arena.co.kr" + link
            print(link)

            image = aTag.find_all('img')
            imageLink = "https:" + image[-1]['src']
            print(imageLink)

            items = card.find('div', {'class': 'items'})
            title = items.find('h3').get_text()
            title = title.strip()
            print(title)

            productId = items.find('div', {'class': 'item-num'}).get_text()
            print(productId)

            s = items.find('s')
            if s==None:
                sale = ""
                price = items.find('div', {'class': 'price'}).get_text()
                price = price.replace(",", "")
                price = price.replace("원", "")
                price = price.strip()
                price = price + " KRW"
                print(price)
                wr.writerow([productId, title, "", link, "새 상품", price, sale, "재고 있음", imageLink, "", "", "", ""])
            else:
                price = s.get_text()
                price = price.replace(",", "")
                price = price.replace("원", "")
                price = price.strip()
                price = price + " KRW"

                sale = items.find('div', {'class': 'price'}).get_text()
                sale = sale.replace(",", "")
                sale = sale.replace("원", "")
                sale = sale.strip()
                sale = sale + " KRW"
                print(price, sale)
                wr.writerow([productId, title, "", link, "새 상품", price, sale, "재고 있음", imageLink, "", "", "", ""])
        except Exception as e:
            print(e)
f.close()