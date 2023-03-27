from bs4 import BeautifulSoup
import requests


# url = 'https://scraping-for-beginner.herokuapp.com/udemy'
# res = requests.get(url)
# soup = BeautifulSoup(res.text, 'html.parser')


# """
# find_allで検索する癖をつける
# ➡︎findだと最初の1件のみを取得するため
# ➡︎IDの場合はfindでOK
# soup.find_all('p')
# """

# n_subscriber = soup.find('p', {'class': 'subscribers'}).text
# n_subscriber = int(n_subscriber.split('：')[1])

# 型の確認
# type = type(n_subscriber)
# print(type)

# n_review = soup.find('p', {'class': 'reviews'}).text
# n_review = int(n_review.split('：')[1])



# いまにゅのECサイト
url_ec = 'https://scraping.official.ec/'
res = requests.get(url_ec)
soup = BeautifulSoup(res.text, 'html.parser')
item_list = soup.find('ul', {'id': 'itemList'})

items = item_list.find_all('li')
item = items[0]
"""
商品の名前と値段を取得
"""
title = item.find('p', {'class': 'items-grid_itemTitleText_31161d6a'}).text
price = item.find('p', {'class': 'items-grid_price_31161d6a'}).text
price = int(price.replace('¥', '').replace(',', ''))
link = item.find('a')['href']

# items-grid_soldOut_31161d6a
# 在庫なし
test = items[3].find('p', {'class': 'items-grid_soldOut_31161d6a'}) == None
# 在庫あり
is_stock = items[0].find('p', {'class': 'items-grid_soldOut_31161d6a'}) == None



print(is_stock)
