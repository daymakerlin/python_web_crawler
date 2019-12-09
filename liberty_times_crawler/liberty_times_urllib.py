import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np  

url='https://news.ltn.com.tw/list/breakingnews/popular'

resp = urllib.request.urlopen(url).read()
soup = BeautifulSoup(resp, 'html5lib')
liberty = soup.find('ul', 'list').find_all('li')
news=[]

for a in liberty:
    new=dict()
    new['title'] =a.find('span','title').text.strip()
    new['time'] =a.find('span','time').text.strip()
    new['href'] =a.find('a','tit')['href']
    news.append(new)

print(news)


test=pd.DataFrame(data=news)
test.index = np.arange(1,len(test)+1)
test.index.names = ['news_NO.']
print(test)
test.to_csv('news.csv',encoding='utf_8_sig')
