from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

blog = Flask(__name__)

blog.config.from_object(Config)

blog.static_folder = 'static'

# blog.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
# blog.secret_key='notnullkey'

db=SQLAlchemy(blog)

from app import routes
