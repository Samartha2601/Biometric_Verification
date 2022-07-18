import pymongo
import uuid
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['BankBot']
User=db['User']
print(db.list_collection_names())

class Users:
    def __init__(self) -> None:
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = client['BankBot']
        self.User=self.db['User']

    def ifuserexists(self,username):
        user=self.User.find_one({'username':username})
        print(user)
        if user is None:
            return 1
        else:
            return 0
    
    def addnewuser(self,username,password,fingerprint="",signature=""):
        new_user={
            "username":username,
            "password":password,
            "fingerprint_Path":fingerprint,
            "signature_path":signature
        }
        if self.User.insert_one(new_user):
            return 1
        return 0
    
    def getuser(self,username):
        if self.ifuserexists(username) == 0:
            return self.User.find_one({'username':username})




