from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

#Atlas DB 접속
client = MongoClient('localhost', 27017) 
db = client.team_3

@app.route('/')
def home():
    return render_template('index.html')

#로그인
@app.route('/users/me', methods=['GET', 'POST'])
def loginlog(userId, time):
    db.userslog.insert_one({'userId':userId}, {'time':time})

#회원가입
@app.route('/user/sign_in', methods=['POST'])
def signup(userId, pw, name):
    count = len(db.users.find({}))
    if count == 0:
        db.users.insert_one({'_id':0}, {'userId':userId}, 
                             {'password':pw}, {'name':name},
                             {'github':''}, {'insta':''},
                             {'twitter':''}, {'intro':''},
                             {'phone':''}, {'where':''},
                             {'about':''}, {'blog':''})    
        count += 1
        
    else:
        db.users.insert_one({'_id':count}, {'userId':userId}, 
                             {'password':pw}, {'name':name},
                             {'github':''}, {'insta':''},
                             {'twitter':''}, {'intro':''},
                             {'phone':''}, {'where':''},
                             {'about':''}, {'blog':''}) 
        count += 1
        
#팀원 전체 조회
@app.route('/user/get', methods=['GET'])
def get_all(name=None):
    db.users.find({})
    return render_template('hello.html', name=name)
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
    response = request.form({'userId':userId})
    return jsonify(response)
#프로필 삭제
@app.route('/user/delete', methods=['POST'])
def hello(id):
    db.users.delete_one({'id':id})


app = Flask(__name__)
@app.route('/hello/<user>') # <user> 생성
def hello_name(user): # <user> 변수값을 함수로 넘김
    return render_template('index.html', name1=user, name2='This is Jinja2 template') # 변수들을 html로 넘김
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")