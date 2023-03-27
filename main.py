from bs4 import BeautifulSoup
import requests


url = 'https://scraping-for-beginner.herokuapp.com/udemy'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# """
# find_allで検索する癖をつける
# ➡︎findだと最初の1件のみを取得するため
# soup.find_all('p')
# """

n_subscriber = soup.find('p', {'class': 'subscribers'}).text
n_subscriber = int(n_subscriber.split('：')[1])

# 型の確認
# type = type(n_subscriber)
# print(type)

n_review = soup.find('p', {'class': 'reviews'}).text
n_review = int(n_review.split('：')[1])


print(n_review)
