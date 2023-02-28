from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

#Atlas DB 접속
load_dotenv()
ID = os.getenv("ID")
PW = os.getenv("PW")
client = MongoClient(f'mongodb+srv://{ID}:{PW}@cluster0.30nb9z3.mongodb.net/?retryWrites=true&w=majority', 27017) 
db = client.team_3


app = Flask(__name__)
@app.route('/hello/<user>') # <user> 생성
def hello_name(user): # <user> 변수값을 함수로 넘김
    return render_template('index.html', name1=user, name2='This is Jinja2 template') # 변수들을 html로 넘김
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")