import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Niranjan']
students=db['Niru']
print(db.list_collection_names())
print(students.find_one()['_id'])