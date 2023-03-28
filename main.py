from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
import requests
import pandas as pd

# Udemy
def get_data_udemy():
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # """
    # find_allで検索する癖をつける
    # ➡︎findだと最初の1件のみを取得するため
    # ➡︎IDの場合はfindでOK
    # soup.find_all('p')
    # """

    n_subscriber = soup.find('p', {'class': 'subscribers'}).text
    n_subscriber = int(n_subscriber.split('：')[1])

    # 型の確認
    # type = type(n_subscriber)
    # print(type)

    n_review = soup.find('p', {'class': 'reviews'}).text
    n_review = int(n_review.split('：')[1])
    return {
        'n_subscriber': n_subscriber,
        'n_review': n_review
    }
get_data_udemy()



# いまにゅのECサイト
def get_data_ec():
    url_ec = 'https://scraping.official.ec/'
    res = requests.get(url_ec)
    soup = BeautifulSoup(res.text, 'html.parser')
    item_list = soup.find('ul', {'id': 'itemList'})

    items = item_list.find_all('li')
    """
    商品の情報を取得
    ・名前
    ・値段
    ・URL
    """
    data_ec = []
    for item in items:
        datum_ec = {}
        datum_ec['title'] = item.find('p', {'class': 'items-grid_itemTitleText_31161d6a'}).text
        price = item.find('p', {'class': 'items-grid_price_31161d6a'}).text
        datum_ec['price'] = int(price.replace('¥', '').replace(',', ''))
        datum_ec['link'] = item.find('a')['href']
        is_stock = items[0].find('p', {'class': 'items-grid_soldOut_31161d6a'}) == None
        datum_ec['is_stock'] = '在庫あり' if is_stock == True else '在庫なし'
        data_ec.append(datum_ec)
    
    df_ec = pd.DataFrame(data_ec)
    return df_ec

print(get_data_ec())


# items-grid_soldOut_31161d6a
# 在庫なし
# test = items[3].find('p', {'class': 'items-grid_soldOut_31161d6a'}) == None
# 在庫あり



# print(data_ec)


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'path/to/the/downloaded/file.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

