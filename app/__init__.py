from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_migrate import Migrate

blog = Flask(__name__)

blog.config.from_object(Config)

blog.static_folder = 'static'

# blog.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
# blog.secret_key='notnullkey'

db=SQLAlchemy(blog)
migrate = Migrate(blog, db)
images = UploadSet('images', IMAGES)
configure_uploads(blog, images)

from app import routes
