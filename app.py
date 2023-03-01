from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os
from time import time, gmtime

app = Flask(__name__)

#Atlas DB 접속
client = MongoClient('localhost', 27017) 
db = client.team_3

@app.route('/')
def home():
    return render_template('index.html')

#로그인
@app.route('/user/me', methods=['GET', 'POST'])
def login():
    userId = request.form('userId')
    db.userslog.insert_one({'userId':userId}, {'time':gmtime(time())})
    # return jsonify({'mgs':db.userlog.find({})})

#회원가입
@app.route('/user/sign_in', methods=['POST'])
def signup(userId, pw, name):
   count = len(db.users.find({}))
   name = request.form['name']
   userId = request.form['userId']
   pw = request.form['pw']
   if db.users.find_one({'userId': userId}):
      return jsonify({'result': 'fail', 'msg': '이미 사용 중인 아이디입니다.'})
   elif count == 0: 
        db.users.insert_one({'_id':0, 'userId':userId, 
                             'password':pw, 'name':name,
                             'github':'', 'insta':'',
                             'twitter':'', 'intro':'',
                             'phone':'', 'where':'',
                             'about':'', 'blog':''})    
        count += 1
        
    else:
        db.users.insert_one({'_id':count, 'userId':userId, 
                             'password':pw, 'name':name,
                             'github':'', 'insta':'',
                             'twitter':'', 'intro':'',
                             'phone':'', 'where':'',
                             'about':'', 'blog':''}) 
        count += 1
   return jsonify({'result': 'success'}) 
        
#팀원 전체 조회
@app.route('/user/get', methods=['GET'])
def get_all(name=None):
    db_all = db.users.find({})
    return render_template('mainpage.html', db_all=db_all)
#상세 정보 조회
@app.route('/user/d_get', methods=['GET'])
def get_sub(_id):
    return db.users.find({'_id':_id})
#프로필 수정
@app.route('/user/<userId>/fix_profile', methods=['POST'])
def update(userId, name, phone, github, email,
            where, about, blog, insta):
    db.users.update({'userId':userId}, {{'name':name,
                                          'phone':phone,
                                          'github':github,
                                          'email':email,
                                          'where':where,
                                          'about':about,
                                          'blog':blog,
                                          'insta':insta}})
#프로필 삭제
@app.route('/user/delete', methods=['POST'])
def hello(id):
    db.users.delete_one({'id':id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)