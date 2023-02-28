from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
ID = os.getenv("ID")
PW = os.getenv("PW")
client = MongoClient(f'mongodb+srv://{ID}:{PW}@cluster0.30nb9z3.mongodb.net/?retryWrites=true&w=majority', 27017) 
db = client.team_3

db.users.insert_one({'name':'teajun','age':26,'_id':0})


print(ID)