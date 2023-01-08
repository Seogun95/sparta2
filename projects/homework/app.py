from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient("mongodb+srv://seogun:test@cluster0.xh0ugah.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.dbsparta

#Flask 기본 코드
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/homework', methods=['POST'])
def test_post():
   name_receive = request.form['name_give']
   comment_receive = request.form['comment_give']

   doc = {
    'name': name_receive,
    'comment': comment_receive
   }

   db.homework.insert_one(doc)
   
   return jsonify({'msg':'저장완료'})

@app.route("/homework", methods=["GET"])
def test_get():
    all_comments = list(db.homework.find({}, {'_id': False}))
    return jsonify({'comments': all_comments})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)