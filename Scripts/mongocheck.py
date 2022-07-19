import pymongo
import uuid
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['BankBot']
User=db['User']
print(db.list_collection_names())


print(User.find_one({'username':"nsdnnma"}))