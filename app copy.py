from flask import Flask, url_for, request, session, redirect, app
from markupsafe import escape
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config["PERMANENT_SESSISON_LIFETIME"] = timedelta(minutes=1)

@app.route('/')
def index():
    if 'username' in session:
        return '로그인 성공! 아이디는 %s' % escape(session['username']) + \
        "<br><a href = '/logout'>로그아웃</a>"

    return "로그인 해주세요. <br><a href = '/login> 로그인 하러가기! </a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))

    return '''
    <form action = "" method = "post">
        <p><input type = "text" name = "username" /></p>
        <p><input type = "submit" value = "Login" /></p>
    </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)