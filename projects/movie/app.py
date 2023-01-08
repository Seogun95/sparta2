
# 코딩 시작

#pymongo
from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient("mongodb+srv://seogun:test@cluster0.xh0ugah.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.dbsparta


#웹스크래핑
import requests
from bs4 import BeautifulSoup


#Flask
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/movie', methods=['POST'])
def test_post():
   url_receive = request.form['url_give']
   star_receive = request.form['star_give']
   comment_receive = request.form['comment_give']

   headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get(url_receive,headers=headers)
   soup = BeautifulSoup(data.text, 'html.parser')

   og_title = soup.select_one('meta[property="og:title"]')['content']
   og_image = soup.select_one('meta[property="og:image"]')['content']
   og_desc = soup.select_one('meta[property="og:description"]')['content']

   doc = {
    'url': url_receive,
    'star': star_receive,
    'comment': comment_receive,
    'title': og_title,
    'img': og_image,
    'desc': og_desc
   }
   db.movie.insert_one(doc)
   
   return jsonify({'msg':'저장완료'})

@app.route("/movie", methods=["GET"])
def test_get():
    all_movies = list(db.movie.find({}, {'_id': False}))
    return jsonify({'movie': all_movies})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)