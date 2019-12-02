import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


url = 'https://www.dcard.tw/f'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
dcard= soup.find_all('div', re.compile('NormalPostLayout__Left.+'))
articles = []

for d in dcard:
    new=dict()
    new['title'] = d.h3.text.strip()
    new['summary'] = d.find_all('div')[1].text.strip()
    new['mark'] = re.findall("\d+",d.find_all('div')[2].text.strip())[1]
    new['response'] = re.findall(r"\d+",d.find_all('div')[2].text.strip())[0]
    new['href'] = 'https://www.dcard.tw' + d.parent.parent.parent['href']
    articles.append(new)
    
print('共 %d 篇' % (len(articles)))
for a in articles[:3]:
    print(a)

    
name=['title','summary','mark','response','href']
test=pd.DataFrame(columns=name,data=articles)
test.index = np.arange(1,len(test)+1)
test.index.names = ['article_NO.']
print(test)

test.to_csv('dcardcsv.csv',encoding='utf_8_sig')
