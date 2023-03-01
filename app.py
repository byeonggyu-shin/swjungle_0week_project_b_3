from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

#Atlas DB 접속
client = MongoClient('localhost', 27017) 
db = client.team_3

#로그인 페이지
@app.route('/')
def home():
    return render_template('index.html')

# 메인 페이지
@app.route('/main')
def main():
    return render_template('mainpage.html')

# # 메인페이지 
# @app.route('/main')
# def mainpage():
#     return render_template('mainpage.html')
#로그인
# @app.route('/users/me', methods=['GET', 'POST'])
# def login(userId):
#     if request.method == 'POST':
#         db.userslog.insert_one({'userId':userId}, {'time':gmtime(time())})

# 로그인 페이지
@app.route('/users/me', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 로그인 처리
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        result = db.users.find_one({ 'userId': id_receive, 'password': pw_receive })
        if id_receive == result['userId'] and pw_receive == result['password']:
            # 로그인 성공 시 메인 페이지로 리다이렉트
            # return jsonify({'result': 'success'})
            return redirect(url_for('login'))
        else:
            # 로그인 실패 시 다시 로그인 페이지로 이동
            return redirect(url_for('login'))
    else:
        return '''
            <form class="login_form" id="signupForm">
                <div>UserName</div>
                <input class="login_input" type="text"  id="user_name" />
                <div>ID</div>
                <input class="login_input" type="text"  id="user_ID" />
                <div>Password</div>
                <input class="login_input"  type="password" id="user_PW" />
                <div>Password Check</div>
                <input class="login_input"  type="password" />
          </form>
        '''


#회원가입
@app.route('/user/sign_in', methods=['POST'])
# def signup(userId,pw,name):
def signup():
   count = len(list(db.users.find({})))
   name = request.form['name']
   userId = request.form['userId']
   pw = request.form['pw']

   if count == 0: 
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
#프로필 삭제
@app.route('/user/delete', methods=['POST'])
def hello(id):
    db.users.delete_one({'id':id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)