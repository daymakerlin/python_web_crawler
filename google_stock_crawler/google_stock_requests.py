import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np  

def google_stock(stid):
    url = 'https://www.google.com/search?q='
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/66.0.3359.181 Safari/537.36'}
    
    resp = requests.get(url+stid, headers=headers)
    soup = BeautifulSoup(resp.text, 'html5lib')
    section = soup.find_all('g-card-section')

    data=[]
    stock = dict()

    stock['name'] = soup.find('div','oPhL2e').text
    stock['current_price'] = section[1].find('span').text
    stock['time'] = section[1].find_all('div')[4].find('span').text
    stock['current_change'] =section[1].find_all('div')[4].find_all('span')[3].text

    for a in section[3].find_all('tr'):
        key=a.find_all('td')[0].text
        value=a.find_all('td')[1].text
        stock[key] = value

    data.append(stock)    
    return data




def repeat_google_stock(idlist):
    data2=[]

    for i in idlist:
        data=google_stock(i)
        data2 += data
        
    return data2



idlist=['TPE:2330','NASDAQ:GOOG','NYSE:T']
data=repeat_google_stock(idlist)




name=['name','市值','current_price','time','current_change',
      '上次收盤價','開盤','最高','最低','本益比','殖利率',
      '52 週高點','52 週低點']
test=pd.DataFrame(columns=name,data=data)
test.index = np.arange(1,len(test)+1)
test.index.names = ['stock_NO.']
    
print(test)
test.to_csv('stock.csv',encoding='utf_8_sig')
