import urllib.request
from bs4 import BeautifulSoup

url='https://movies.yahoo.com.tw/movie_intheaters.html'

def yahoo_movie(url):
    resp = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(resp, 'html5lib')
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

def repeat_yahoo_movie(url):
    movies=[]
    movie=yahoo_movie(url)
    movies += movie
    resp = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(resp, 'html5lib')
    
    if soup.find('li', 'nexttxt').a['href']:
        nextpage = soup.find('li', 'nexttxt').a['href']
    else:
        nextpage = []

    while nextpage!=[]:
        new_movie=yahoo_movie(nextpage)
        movies += new_movie
        resp = urllib.request.urlopen(nextpage).read()
        soup = BeautifulSoup(resp, 'html5lib')
        if soup.find('li', 'nexttxt').a:
            nextpage = soup.find('li', 'nexttxt').a['href']
        else:
            nextpage = []
            
    return movies

import pandas as pd
import numpy as np

data=repeat_yahoo_movie(url)
name=['ch_name','eng_name','release_date','expectation','url','movie_id','poster_url','intro','trailer_url']
test=pd.DataFrame(columns=name,data=data)
test.index = np.arange(1,len(test)+1)
test.index.names = ['movie_NO.']

print('目前上映', len(data), '部電影')

print('期待值> 90% :' )
n='90%'
for a in data:
    if a['expectation'] > n :
        print(a['ch_name'],a['expectation'])
        
print('上映中的電影:',test)

test.to_csv('newmovie.csv',encoding='utf_8_sig')
