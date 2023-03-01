from flask import Flask, render_template, jsonify, request , redirect, url_for, session
from pymongo import MongoClient
from time import time, gmtime

app = Flask(__name__)
app.secret_key = "secret_key"
#Atlas DB 접속
client = MongoClient('localhost', 27017) 
db = client.team_3

@app.route('/')
def home():
    return render_template('index.html')

#회원가입
@app.route('/register', methods=['POST'])
def signup():
   count = len(list(db.users.find({})))
   name = request.form['name']
   userId = request.form['userId']
   pw = request.form['pw']

   if db.users.find_one({'userId': userId}):
      return jsonify({'result': 'fail', 'msg': '이미 사용 중인 아이디입니다.'})
   elif count == 0: 
        db.users.insert_one({'_id':0, 'userId':userId, 
                             'password':pw, 'name':name,
                             'github':'',  'email':'', 'insta':'',
                             'about':'', 'blog':''})    
        count += 1
   else:
        db.users.insert_one({'_id':count, 'userId':userId, 
                             'password':pw, 'name':name,
                             'github':'', 'email':'', 'insta':'',
                             'about':'', 'blog':''})  
        count += 1
   return jsonify({'result': 'success'}) 
        
#로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 사용자 입력 정보 받기
        userId = request.form['userId']
        password = request.form['pw']

        # MongoDB에서 사용자 정보 찾기
        user = db.users.find_one({'userId': userId, 'password': password})

        if user:
            # 로그인 정보를 세션에 저장
            session['userId'] = userId
            return jsonify({'result': "success" , 'userId' : userId})
        else:
            return jsonify({'result': 'fail','msg': "아이디와 비밀번호를 확인해 주십시오."})
            # return render_template('index.html',error="Invalid username or password")

    return render_template('index.html')

# 메인페이지
@app.route('/mainpage', methods=['GET'])
def mainpage():
    db_all = db.users.find({})
    if 'userId' in session:
        return render_template('mainpage.html', db_all=db_all , userId=session['userId'])
    else:
        return redirect(url_for('login'))
    
#상세 정보 조회
@app.route('/userinfo', methods=['GET'])
def get_sub(_id):
    return db.users.find({'_id':_id})

#프로필 수정
@app.route('/useinfo/edit', methods=['POST'])
def update():

    id = request.form['userId']
    name = request.form['name']
    github = request.form['github']
    email = request.form['email']
    about = request.form['about']
    blog = request.form['blog']
    insta = request.form['insta']

    print(id)
    print(name)
    print(insta)
    db.users.update_one({'_id': id}, {'$set': {'name':name,
                                          'github':github,
                                          'email':email,
                                          'about':about,
                                          'blog':blog,
                                          'insta':insta}}
                                          )
    return jsonify({'result': 'success'}) 
#프로필 삭제
@app.route('/user/delete', methods=['POST'])
def hello(id):
    db.users.delete_one({'id':id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)