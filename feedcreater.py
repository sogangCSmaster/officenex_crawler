
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta, date
import re
import json
import csv



# FIX ================
startPage = 1
url = "https://www.officenex.com/cate/cateItemList.do?cateId=200004228227200008518999&rowLevel=1"
categoryName = "주문제작"
endPage = 15
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
        print(imageLink)
        
        response2 = requests.get(link, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'})
        html2 = response2.text
        soup2 = BeautifulSoup(html2, 'lxml')
        title = soup2.find('p', {'class': 'prd-title'}).get_text()
        title = title.strip()
        print(title)

        productId = soup2.find_all('div', {'class': 'prd-info'})[1]
        productId = productId.find('dd').get_text()
        productId = productId.strip()
        print(productId)
        
        # //*[@id="subContents"]/div[2]/div/div[1]/div/div[1]/div[2]/p
        

        price = soup2.find('input', {'id': 'sobiPrice'})
        price = price['value'].split('.')[0] + ' KRW'
        print(price)

        sale = soup2.find('strong', {'class': 'price red'}).get_text()
        sale = sale.strip()
        sale = sale.replace(',', '') + ' KRW'
        print(sale)

        if not '품절' in title:
            wr.writerow([productId, title, "", link, "새 상품", price, sale, "재고 있음", imageLink, "", "", "", ""])
        

f.close()