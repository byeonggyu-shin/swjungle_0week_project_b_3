from flask import Flask, render_template, jsonify, request, redirect, url_for, session
# from flask_login import LoginManager, login_user, login_required
# from user import User
from pymongo import MongoClient
import os
import hashlib
import jwt
import datetime
from time import time, gmtime
# from datetime import datetime

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)

#Atlas DB 접속
client = MongoClient('localhost', 27017) 
db = client.team_3

app.secret_key = 'My_Key'

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/profile')
# @login_required
# def profile():
#     # 로그인된 사용자만 접근 가능한 페이지
#     return 'Welcome to your profiile page'

# 메인 페이지
@app.route('/main')
def main():
    return render_template('mainpage.html')

#회원가입
@app.route('/user/sign_in', methods=['POST'])
def signup():
   count = len(list(db.users.find({})))
   name = request.form['name']
   userId = request.form['userId']
   pw = request.form['pw']
   pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

   # 이미 존재하는 아이디면 패스!
   if db.users.find_one({'userId': userId}):
      return jsonify({'result': 'fail', 'msg': '이미 사용 중인 아이디입니다.'})
   elif count == 0: 
        db.users.insert_one({'_id':0, 'userId':userId, 
                             'password':pw_hash, 'name':name,
                             'github':'', 'insta':'',
                             'about':'', 'blog':''})    
        count += 1
        
   else:
        db.users.insert_one({'_id':count, 'userId':userId, 
                             'password':pw_hash, 'name':name,
                             'github':'', 'insta':'',
                             'about':'', 'blog':''})  
        count += 1
   return jsonify({'result': 'success'})

# @login_manager.user_loader
# def load_user(user_id):
#     # 사용자 ID로 사용자 정보를 가져오는 함수
#     return User.get(user_id)

# @app.route('/login', methods=['POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         print('{}가 로그인 했습니다.'.format(form.data.get('userid')))
#         session['userId'] = form.data.get('userid')
#         return redirect('/')
#     return render_template('login.html', form=form)

# @app.route('/main')
# def main():
#     if 'id' in session:
#         id = session['id']
#         print(id)
#         return render_template("main.html")
#     else:
#         return render_template("login.html")

# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['id'] = request.form['id']
#         return render_template("main.html")
#     else:
#         return render_template("login.html")

# @app.route('/logout')
# def logout():
#     session.pop('id', None)
#     return render_template("main.html")

SECRET_KEY = 'secret_key'
@app.route('/users/me', methods=['POST'])
def login():
    # 로그인 처리
    id_receive = request.form['userId']
    pw_receive = request.form['pw']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({ 'userId': id_receive, 'password': pw_hash })

    if result is not None:
        # JWT 토큰 생성
        payload = {
            'userId': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        }
        # userId = id_receive
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/users/isAuth', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        # token을 시크릿키로 디코딩합니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        userinfo = db.users.find_one({'userId': payload['userId']}, {'_id': 0})
        return jsonify({'result': 'success', 'myname': userinfo['name']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        # 로그인 정보가 없으면 에러가 납니다!
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
        
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