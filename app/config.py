import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or 'not-a-regular-key'
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABSE_URL') or 'sqlite:///' + os.path.join(basedir, 'posts.db')
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	UPLOADS_DEFAULT_DEST = '/Users/ankulgup/Documents/img/'
	UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/'
	 
	UPLOADED_IMAGES_DEST = '/Users/ankulgup/Documents/img/'
	UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/'
