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

@app.route('/bucket', methods=['POST'])
def bucket_post():
   bucket_receive = request.form['bucket_give']
   count = list(db.bucket.find({},{'_id':False}))
   num = len(count) + 1

   doc = {
    'num': num,
    'bucket': bucket_receive,
    'done': 0
   }

   db.bucket.insert_one(doc)
   
   return jsonify({'msg':'저장완료'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': '버킷 완료!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_bucket = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': all_bucket})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)