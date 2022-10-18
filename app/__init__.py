from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'l8G5zgBO2OvULPfkeIwyPFSOGxTH48vv'
from app import routes