
from flask import Flask,render_template,session,redirect,url_for
import numpy as np
from flask import jsonify,request
import joblib
import pymongo
import hashlib
import os

from Scripts.mongodb import Users
from Scripts.get_sim import similarity_orb
from Scripts.check_model import GetModel


model = GetModel()
user=Users()


UPLOAD_FOLDER_FIN='D:\mdp_2\Images\Fingerprint'
UPLOAD_FOLDER_SIG='D:\mdp_2\Images\Signatures'

import json

app=Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'GDtfDCFYjD'
app.config['UPLOAD_FOLDER_FIN']=UPLOAD_FOLDER_FIN
app.config['UPLOAD_FOLDER_SIG']=UPLOAD_FOLDER_SIG


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
            session['username']=user_data['username']
            return redirect(url_for('home'))
        
    else:
        return render_template('login.html')

#view for sign up

@app.route('/signup',methods=['GET','POST'])
def signup():
    if(request.method == 'POST'):
        username = request.form.get("username","Anonimous")
        password=request.form.get("password","12345678")
        fingerprint=request.files["fingerprint"]
        signature=request.files["signature"]

        if(user.ifuserexists(username) == 0):
            return "User exists"
        fingerprint_path=os.path.join(app.config['UPLOAD_FOLDER_FIN'], fingerprint.filename)
        signature_path=os.path.join(app.config['UPLOAD_FOLDER_SIG'], signature.filename)

        if(user.addnewuser(username,password,fingerprint_path,signature_path) == 0):
            return "cannot add user"
        fingerprint.save(fingerprint_path)
        signature.save(signature_path)
        session['username']=username

        return redirect(url_for('home'))
        return render_template('signup.html')
    return render_template('signup.html')

#view for home
@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        print("FFFF")
        return redirect(url_for('authenticate'))
    return render_template('home.html')


# view for logout
@app.route('/logout')

def logout():
    session['username']=None
    return redirect(url_for('landing'))

@app.route('/authenticate',methods=['GET','POST'])
def authenticate():
    if request.method=='POST':
        fingerprint = request.files["fingerprint"]
        signature = request.files["signature"]
        temp_fingerprint_path=os.path.join('D:/mdp_2/Images/temproary/',fingerprint.filename)
        temp_sign_path=os.path.join('D:/mdp_2/Images/temproary/',signature.filename)
        fingerprint.save(temp_fingerprint_path)
        signature.save(temp_sign_path)
        print(session['username'])
        username=session['username']
        user_details=user.getuser(username=username)
        fin_mathces = similarity_orb(user_details['fingerprint_Path'],temp_fingerprint_path)
        sign_mathces = model.predict_model(user_details['signature_path'],temp_sign_path)
        print(sign_mathces)
        if sign_mathces == 1 and fin_mathces ==1 :

            return "Sucess"

        else:
            return "Sorry try again!"

        return render_template('fileinput.html')
    return render_template('fileinput.html')

if __name__=='__main__':
    app.run(port=5000,debug=True)