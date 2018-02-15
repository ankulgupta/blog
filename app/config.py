import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or 'not-a-regular-key'
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABSE_URL') or 'sqlite:///' + os.path.join(basedir, 'posts.db')
	SQLALCHEMY_TRACK_MODIFICATIONS=False