from bs4 import BeautifulSoup
import requests


url = 'https://scraping-for-beginner.herokuapp.com/udemy'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
print(soup)