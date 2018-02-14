import requests
from bs4 import BeautifulSoup
from decimal import *

page = requests.get('http://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=USD')
soup = BeautifulSoup(page.content, 'html.parser')
todayrate = soup.find_all(class_="uccResultAmount")[0].get_text()
q = Decimal(todayrate)
