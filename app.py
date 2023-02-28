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

