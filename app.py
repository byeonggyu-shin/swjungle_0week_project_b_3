from flask_login import LoginManager, UserMixin, login_user, user_repo
from flask import Flask
from flask import request, render_template, url_for, redirect

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, email, name, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"USER: {self.id} = {self.name}"
    
    
@app.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'GET':
        next = request.args.get('next', '') # login 후 이동할 페이지 지정

    else:
        # form 방식으로 받아올 때에는 form에, json 방식으로 받아올 때에는 json에 원하는 정보가 담겨있음
        email = request.form.get('email')
        password = request.form.get('password')
        next = request.form.get('next')
        safe_next_redirect = url_for('index')

        if next:
            safe_next_redirect = next

        user = user_repo.get_by_email(email)
        if user.password == password:
        	# login 한 사용자의 정보를 session에 저장해줌
            login_user(user)
            return redirect(safe_next_redirect)

    return render_template('auth/login.html', next=next)

@app.route('/logout', methods=['GET'])
def logout():
    # flask login으로 logout >> 사용자 정보 세션 삭제
    logout_user()
    return redirect(url_for('index'))

@app.route('/private')

@login_required
def private_page():
    session['page'] = 'private'
    return render_template('main/private.html')

@login_manager.user_loader
def load_user(user_id):
	return user_repo.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    # print(dir(request))
    # login이 필요한 page에 접근 시 login page로 이동을 시켜줌
    query_string = urlencode(request.args)

    return redirect(url_for('auth.login', next=f'{request.path}?{query_string}'))