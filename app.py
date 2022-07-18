
from flask import Flask,render_template,session,redirect,url_for
import numpy as np
from flask import jsonify,request
import joblib
import pymongo
import hashlib
from Scripts.mongodb import Users
user=Users()


# from Scripts.mongodb import *
# User=p
# from user import routes
import json

# from user.models import User
app=Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'GDtfDCFYjD'

# landing view

@app.route('/')
def landing():

    return render_template('landing.html')


# view for login
@app.route('/login',methods=['GET','POST'])
def login():
    if session['username'] is not None:
        return redirect(url_for('home'))

    if(request.method == 'POST'):
        username = request.form.get("username","Anonimous")
        password=request.form.get("password","12345678")
        user_data=user.getuser(username)
        if user_data is None:
            return "Something is wrong"
        if password==user_data['password']:
            return redirect(url_for('home'))
        
    else:
        return render_template('login.html')

#view for sign up

@app.route('/signup',methods=['GET','POST'])
def signup():
    if(request.method == 'POST'):
        username = request.form.get("username","Anonimous")
        password=request.form.get("password","12345678")
        if(user.ifuserexists(username) == 0):
            return "User exists"
        password
        if(user.addnewuser(username,password) == 0):
            return "cannot add user"
        session['username']='username'
        return redirect(url_for('home'))
        return render_template('signup.html')
    return render_template('signup.html')

#view for home
@app.route('/home')
def home():

    return render_template('home.html')


# view for logout
@app.route('/logout')

def logout():
    session['username']=None
    return redirect(url_for('landing'))

if __name__=='__main__':
    app.run(port=5000,debug=True)