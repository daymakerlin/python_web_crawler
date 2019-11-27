import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#爬一頁資料
url='https://movies.yahoo.com.tw/movie_thisweek.html'

def yahoo_newmovie(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html5lib')
    rows = soup.find_all('div', 'release_info_text')
    movies = []
    for row in rows:
        movie = dict()
        movie['ch_name'] = row.find('div', 'release_movie_name').a.text.strip()
        movie['eng_name'] = row.find('div', 'release_movie_name').find('div', 'en').a.text.strip()
        pattern = '\d+-\d+-\d+'
        match = re.search(pattern,row.find('div', 'release_movie_time').text)
        movie['release_date'] = match.group(0)
        movie['expectation'] = row.find('div', 'leveltext').span.text.strip()
        movie['url'] = row.find('div', 'release_movie_name').a['href']
        movie['movie_id'] =movie['url'].split('.html')[0].split('-')[-1]
        movie['poster_url'] = row.parent.find_previous_sibling('div', 'release_foto').a.img['src']
        movie['intro'] = row.find('div', 'release_text').text.replace('\n', '').strip()
        trailer_a = row.find_next_sibling('div', 'release_btn color_btnbox').find_all('a')[1]
        movie['trailer_url'] = trailer_a['href'] if 'href' in trailer_a.attrs.keys() else ''
        movies.append(movie)
    return movies


data=yahoo_newmovie(url)
name=['ch_name','eng_name','release_date','expectation','url','movie_id','poster_url','intro','trailer_url']
test=pd.DataFrame(columns=name,data=data)
test.index = np.arange(1,len(test)+1)
test.index.names = ['movie_NO.']

print('本周新片', len(data), '部電影')
print('期待值> 90% :' )
n='90%'
for a in data:
    if a['expectation'] > n :
        print(a['ch_name'],a['expectation'])
        

print('本周新片:',test)
test.to_csv('newmovie.csv',encoding='utf_8_sig')

#爬兩頁的資料
##用上映中的電影網址做範例
url='https://movies.yahoo.com.tw/movie_intheaters.html'     

movies=[]
movie=yahoo_newmovie(url)
movies += movie
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html5lib')

if soup.find('li', 'nexttxt').a['href']:
    nextpage = soup.find('li', 'nexttxt').a['href']
    new_movie=yahoo_newmovie(nextpage)
    movies += new_movie
        
        


data=movies
name=['ch_name','eng_name','release_date','expectation','url','movie_id','poster_url','intro','trailer_url']
test=pd.DataFrame(columns=name,data=data)
test.index = np.arange(1,len(test)+1)
test.index.names = ['movie_NO.']

print('本周新片', len(data), '部電影')

print('期待值> 90% :' )
n='90%'
for a in data:
    if a['expectation'] > n :
        print(a['ch_name'],a['expectation'])
        
print('本周新片:',test)

test.to_csv('newmovie.csv',encoding='utf_8_sig')
