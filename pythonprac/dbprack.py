from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://seogun:test@cluster0.xh0ugah.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20210829',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

#old_content > table > tbody > tr:nth-child(2) > td.title > div > a
#공통된 부분은 movies로 한 번에 가져온다.
movies = soup.select('#old_content > table > tbody > tr')


#movies안에 있는 태그들을 모두 찾기 위해 반복문을 사용한다.
for movie in movies:
    a_tage = movie.select_one('td.title > div > a')
    if a_tage is not None:
        title = a_tage.text
        star = movie.select_one('td.point').text
        rank = movie.select_one('td:nth-child(1) > img')['alt']

        doc = {
            'title': title,
            'star': star,
            'rank': rank,
        }

        db.movies.insert_one(doc)