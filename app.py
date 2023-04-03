from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import altair as alt
import streamlit as st

import os
from dotenv import load_dotenv
load_dotenv('.env')


def get_data_ec():
    url_ec = 'https://scraping.official.ec/'
    res = requests.get(url_ec)
    soup = BeautifulSoup(res.text, 'html.parser')
    item_list = soup.find('ul', {'id': 'itemList'})
    items = item_list.find_all('li')

    # """
    # 商品の情報を取得
    # ・名前
    # ・値段
    # ・URL
    # クラス名が変わっていた？？？→商品情報がループで取得できなくなっていた
    # """
    data_ec = []
    for item in items:
        datum_ec = {}
        # datum_ec['title'] = item.find('p', {'class': 'items-grid_itemTitleText_31161d6a'}).text
        datum_ec['title'] = item.find('p', {'class': 'items-grid_itemTitleText_041c488c'}).text
        # price = item.find('p', {'class': 'items-grid_price_31161d6a'}).text
        price = item.find('p', {'class': 'items-grid_price_041c488c'}).text
        datum_ec['price'] = int(price.replace('¥', '').replace(',', ''))
        datum_ec['link'] = item.find('a')['href']
        # is_stock = items[0].find('p', {'class': 'items-grid_soldOut_31161d6a'}) == None
        is_stock = items[0].find('p', {'class': 'items-grid_soldOut_041c488c'}) == None
        datum_ec['is_stock'] = '在庫あり' if is_stock == True else '在庫なし'
        data_ec.append(datum_ec)
    
    df_ec = pd.DataFrame(data_ec)
    return df_ec


def get_worksheet():
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
    return worksheet


def get_chart():
    worksheet = get_worksheet()
    data = worksheet.get_all_values()
    df_udmey = pd.DataFrame(data[1:], columns=data[0])
    # 型変換
    df_udmey = df_udmey.astype({
        'n_subscriber': int,
        'n_review': int
    })
    # 最小値・最大値
    ymin1 = df_udmey['n_subscriber'].min() - 10
    ymax1 = df_udmey['n_subscriber'].max() + 10
    ymin2 = df_udmey['n_review'].min() - 100
    ymax2 = df_udmey['n_review'].max() + 100

    # Layered chart with Dual-Axisからのコピー
    base = alt.Chart(df_udmey).encode(
        alt.X('date:T', axis=alt.Axis(title=None))
    )

    line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
        alt.Y('n_subscriber',
            axis=alt.Axis(title='受講生数', titleColor='#57A44C'),
            scale=alt.Scale(domain=[ymin1, ymax1])
            )
    )

    line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
        alt.Y('n_review',
            axis=alt.Axis(title='レビュー数', titleColor='#5276A7'),
            scale=alt.Scale(domain=[ymin2, ymax2])
            )
    )

    chart = alt.layer(line1, line2).resolve_scale(
        y = 'independent'
    )
    return chart

data_ec = get_data_ec()
chart = get_chart()

st.title("Webスクレイピング活用アプリ")

st.write('## Udemy情報')
st.altair_chart(chart, use_container_width=True)

st.write('## EC在庫情報', data_ec)