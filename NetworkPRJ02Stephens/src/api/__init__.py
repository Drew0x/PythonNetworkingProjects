'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student: Andrew Stephens
Description: Activity 13 - Quotes API
'''

from flask import Flask

app = Flask("Quotes API")

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
db.init_app(app)

# db from models
# from app import models
# with app.app_context():
#     db.create_all()

#original\/
from api import routes

#from . import routes