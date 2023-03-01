# from flask import Flask, render_template, jsonify, request
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
# from time import time, gmtime

from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.team_3

#Atlas DB 접속
# client = MongoClient('localhost', 27017) 
# db = client.team_3

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('index.html')

#로그인
# @app.route('/users/me', methods=['GET', 'POST'])
# def login(userId):
#     if request.method == 'POST':
#         db.userslog.insert_one({'userId':userId}, {'time':gmtime(time())})

#회원가입
# @app.route('/users', methods=['POST'])
# def register():
#     return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})
#     # if request.method == 'GET':
#     #     return render_template("index.html")
#     # else:
#     #     #회원정보 생성
#     #     id_receive = request.form.get('id_give')
#     #     pw_receive = request.form.get('pw_give')
#     #     pwc_receive = request.form.get('pwc_give')
#     #     # userid = request.form.get('userid')
#     #     # password = request.form.get('password')
#     #     # re_password = request.form.get('re_password')

#     #     userinfo={ 'user_id':id_receive, 'user_pwd': pw_receive, }

#     #     if not (id_receive and pw_receive and pwc_receive) :
#     #         return "모두 입력해주세요"
#     #     elif pw_receive != pwc_receive:
#     #         return "비밀번호를 확인해주세요"
#     #     else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
#     #         db.users.insert_one(userinfo)
#     #         return "회원가입 완료"
#     #     return redirect('/register')
#     return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})

@app.route('/users', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        #회원정보 생성
        id_receive = request.form['id_give', None]
        pw_receive = request.form['pw_give', None]
        pwc_receive = request.form['pwc_give', None]
        # userid = request.form.get('userid')
        # password = request.form.get('password')
        # re_password = request.form.get('re_password')

        userinfo={ 'user_id': id_receive, 'user_pw': pw_receive, 'user_pwc': pwc_receive }

        if not (id_receive and pw_receive and pwc_receive) :
            return "모두 입력해주세요"
        elif pw_receive != pwc_receive:
            return "비밀번호를 확인해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            db.users.insert_one(userinfo)
            return "회원가입 완료"
        # return redirect('/register')

    # return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})

# @app.route('/user', methods=['GET', 'POST'])
# def register():
#     return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})
    #회원정보 생성
    # id_receive = request.form('id_give')
    # pw_receive = request.form('pw_give')
    # pwc_receive = request.form('pwc_give')
    # # userid = request.form.get('userid')
    # # password = request.form.get('password')
    # # re_password = request.form.ge('re_password')
    # userinfo={ 'user_id':id_receive, 'user_pw': pw_receive, 'user_pwc': pwc_receive}
    # if not (id_receive and pw_receive and pwc_receive) :
    #     return "모두 입력해주세요"
    # elif pw_receive != pwc_receive:
    #     return "비밀번호를 확인해주세요"
    # else: #모두 입력이 정상적으로 되었다면밑에명령실행(DB에 입력됨)
    #     db.users.insert_one(userinfo)
    #     return "회원가입 완료"
    # return redirect('/register')

    

#회원가입
# @app.route('/user/sign_in', methods=['POST'])
# def signup(userId, pw, name):
#     count = len(db.users.find({}))
#     if count == 0:
#         db.users.insert_one({'_id':0}, {'userId':userId}, 
#                              {'password':pw}, {'name':name},
#                              {'github':''}, {'insta':''},
#                              {'twitter':''}, {'intro':''},
#                              {'phone':''}, {'where':''},
#                              {'about':''}, {'blog':''})    
#         count += 1
        
#     else:
#         db.users.insert_one({'_id':count}, {'userId':userId}, 
#                              {'password':pw}, {'name':name},
#                              {'github':''}, {'insta':''},
#                              {'twitter':''}, {'intro':''},
#                              {'phone':''}, {'where':''},
#                              {'about':''}, {'blog':''}) 
#         count += 1
        
# #팀원 전체 조회
# @app.route('/user/get', methods=['GET'])
# def get_all(name=None):
#     db.users.find({})
#     return render_template('hello.html', name=name)
# #상세 정보 조회
# @app.route('/user/d_get', methods=['GET'])
# def get_sub(_id):
#     return db.users.find({'_id':_id})
# #프로필 수정
# @app.route('/user/<userId>/fix_profile', methods=['POST'])
# def update(userId, name, phone, github, email,
#             where, about, blog, insta):
#     db.users.update({'userId':userId}, {{'name':name,
#                                           'phone':phone,
#                                           'github':github,
#                                           'email':email,
#                                           'where':where,
#                                           'about':about,
#                                           'blog':blog,
#                                           'insta':insta}})
# #프로필 삭제
# @app.route('/user/delete', methods=['POST'])
# def hello(id):
#     db.users.delete_one({'id':id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)