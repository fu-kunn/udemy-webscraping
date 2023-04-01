from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
import datetime
import altair as alt
import streamlit as st

import os
from dotenv import load_dotenv
load_dotenv('.env')

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

# get_data_ec()


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
    'service_account.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

SP_SHEET_KEY = os.environ.get('SP_KEY')
sh = gc.open_by_key(SP_SHEET_KEY)
SP_SHEET = 'db'
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

data_udemy = get_data_udemy()
today = datetime.date.today().strftime('%Y/%m/%d')
data_udemy['date'] = today
# エラー発生
df = df.append(data_udemy, ignore_index=True)
# スプシ書き込む場所を指定（1行１列目から）
# set_with_dataframe(worksheet, df, row=1, col=1)



data = worksheet.get_all_values()
df_udmey = pd.DataFrame(data[1:], columns=data[0])

# Layered chart with Dual-Axisからのコピー
base = alt.Chart(df_udmey).encode(
    alt.X('date:T', axis=alt.Axis(title=None))
)

line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
    alt.Y('n_subscriber',
          axis=alt.Axis(title='受講生数', titleColor='#57A44C'))
)

line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
    alt.Y('n_review',
          axis=alt.Axis(title='レビュー数', titleColor='#5276A7'))
)

chart = alt.layer(line1, line2).resolve_scale(
    y = 'independent'
)

df_udmey = df_udmey.astype({
    'n_subscriber': int,
    'n_review': int
})

# st.altair_chart(chart, use_container_width=True)
# st.write('aaaaa')
print(df_udmey.dtypes)
# print(df_udmey['n_subscriber'].min() - 10)