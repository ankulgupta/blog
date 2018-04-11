from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_migrate import Migrate
from flask_login import LoginManager

blog = Flask(__name__)

blog.config.from_object(Config)

blog.static_folder = 'static'

# blog.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
# blog.secret_key='notnullkey'

db=SQLAlchemy(blog)
db.session.commit()
migrate = Migrate(blog, db)
images = UploadSet('images', IMAGES)
configure_uploads(blog, images)
login = LoginManager(blog)
login.login_view = 'login'

from app import routes, models