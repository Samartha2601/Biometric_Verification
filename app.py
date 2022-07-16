from flask import Flask,render_template
import numpy as np
from flask import jsonify,request
import joblib
# from Scripts.mongodb import *
import json
app=Flask(__name__)


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')


if __name__=='__main__':
    app.run(port=5000,debug=True)