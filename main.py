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
test = int(n_subscriber.split('：')[1])
type = type(test)

print(type)
