from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'sri'

@app.route('/')
def welcome():
    return "Hello world"

@app.route('/home')
def home():
    return "This is home page"

from controller import *