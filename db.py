from pymongo import MongoClient

client = MongoClient('localhost', 27017) 
db = client.team_3

# db.users.insert_one({'name':'teajun','age':26,'_id':0})


print(list(db.users.find({})))