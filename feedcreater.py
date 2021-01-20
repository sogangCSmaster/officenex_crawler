
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta, date
import re
import json
import csv



# FIX ================
startPage = 1
url = "https://www.officenex.com/cate/cateItemList.do?cateId=27200005910203&rowLevel=1"
categoryName = "일반사무용품"
endPage = 52
# END FIX ============

endPage = endPage + 1

f = open(categoryName + '.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

wr.writerow(["id", "제목", "설명", "링크", "상태", "가격", "할인가", "재고 수량", "이미지 링크", "gtin", "mpn", "상표", "google 상품 카테고리"])
# wr.writerow([2, "박상미", True])


# CRAWL START
for page in range(startPage, endPage):
    response = requests.get(url + "&currentPageNo=" + str(page))
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    
    goodsBox = soup.find('ul', {'class': 'goodsBox'})
    goods_contents = goodsBox.find_all('ul', {'class', 'goods_content'})

    for goods_content in goods_contents:
        img = goods_content.find('img')
        goods_img = goods_content.find('li', {'class': 'goods_img'})
        aTag = goods_img.find('a')
        
        link = "https://www.officenex.com"+aTag['href']
        imageLink = img['src']
        
        response2 = requests.get(link)
        html2 = response2.text
        soup2 = BeautifulSoup(html2, "html.parser")
        title = soup2.find('div', {'class': 'goods_title'}).get_text()
        title = title.strip()
        print(title)

        productId = soup2.find('dd', {'class': 'color_517'}).get_text()
        productId = productId.strip()
        print(productId)

        price = soup2.find('span', {'class': 'size_15'}).get_text()
        price = price.strip()
        price = price.replace(',', '') + ' KRW'

        sale = soup2.find('span', {'class': 'size_20'}).get_text()
        sale = sale.strip()
        sale = sale.replace(',', '') + ' KRW'
        print(price)
        print(sale)

        if not '품절' in title:
            wr.writerow([productId, title, "", link, "새 상품", price, sale, "재고 있음", imageLink, "", "", "", ""])
        

f.close()