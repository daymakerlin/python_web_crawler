import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np  


url='https://tw.appledaily.com/hot/daily'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html5lib')
apple = soup.find('ul', 'all').find_all('li')
news = []

for a in apple:
    new=dict()
    new['number']=a.find('div', 'aht_title_num').text
    new['title']=a.find('div', 'aht_title').text
    news.append(new)

print(news)
 

test=pd.DataFrame(data=news)
test.set_index('number', inplace=True)
print(test)
test.to_csv('news.csv',encoding='utf_8_sig')
