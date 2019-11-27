import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



def Gossiping_today_pop_articles(url):
    resp=requests.get(url,cookies={'over18': '1'})
    soup=BeautifulSoup(resp.text,'html5lib')
    
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    PTT_URL = 'https://www.ptt.cc'        
    prev_url = PTT_URL+paging_div.find_all('a')[1]['href']
   

    articles = []
    divs = soup.find_all('div', 'r-ent')

    today = time.strftime("%m/%d").lstrip('0')

    
    for d in divs:
        if d.find('div', 'date').text.strip()==today:  
            push_count = 0
            push_str = d.find('div', 'nrec').text
            
            if push_str:
                try:
                    push_count = int(push_str) 
                except ValueError:
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            if d.find('a'):
                title = d.find('a').text    
                date= d.find('div', 'date').text
                author = d.find('div', 'author').text 
                href = PTT_URL+d.find('a')['href']   
                articles.append({
                    'title':title,
                    'date':date,
                    'author':author,
                    'push_count':push_count,
                    'href':href})

    return articles,prev_url



def repeat_articles(url):
    articles=[]
    
    new_articles,prev_url=Gossiping_today_pop_articles(url)
    articles += new_articles
    new_articles, new_prev_url= Gossiping_today_pop_articles(prev_url)

    while new_articles!=[]:
        articles += new_articles
        new_articles,new_prev_url=Gossiping_today_pop_articles(new_prev_url)

    else:
        return articles

    
    
    
    
    
    
url='https://www.ptt.cc/bbs/Gossiping/index.html'    
articles=repeat_articles(url)

print('今天有', len(articles), '篇文章')
print('熱門文章(> 50 推):' )    
for a in articles:
    if int(a['push_count']) > 50:
        print(a)


        
        
data=repeat_articles(url)
name=['title','date','author','push_count','href']
test=pd.DataFrame(columns=name,data=data)
test.index = np.arange(1,len(test)+1)
test.index.names = ['article_NO.']


print(test)
test.to_csv('testcsv.csv',encoding='utf_8_sig')
