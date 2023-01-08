
from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://seogun:test@cluster0.xh0ugah.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

#Flask 기본 코드
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/test', methods=['POST'])
def test_post():
   some_receive = request.form['some_give']

   doc = {
    'some_receive': some_receive
   }

   db.folder.insert_one(doc)
   return jsonify({'msg':'저장완료'})

@app.route("/test", methods=["GET"])
def test_get():
    all_something = list(db.folder.find({}, {'_id': False}))
    return jsonify({'some':all_something})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)