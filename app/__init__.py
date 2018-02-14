from flask import Flask
from flask_sqlalchemy import SQLAlchemy

blog = Flask(__name__)
blog.static_folder = 'static'

blog.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
blog.secret_key='notnullkey'

db=SQLAlchemy(blog)

from app import routes
