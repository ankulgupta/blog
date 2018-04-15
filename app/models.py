from datetime import datetime 
from app import db, login
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config

# db.engine=create_engine('sqlite:///' + os.path.join(basedir, 'posts.db')
# db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=db.engine))

Base=declarative_base()
# Base.query=db_session.query_property()

ACCESS = {
	'user':1,
	'admin':2
}

class User(UserMixin, db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(20), unique=True)
	password_hash = db.Column(db.String(250))
	access= db.Column(db.Integer)

	def __init__(self, email,access=ACCESS['user']):
		self.email = email
		self.access = access

	def __repr__(self):
		return ("{}:{}".format(self.email, self.password_hash))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash, password)

	def is_admin(self):
		print(self.access)
		print(ACCESS['admin'])
		return self.access == ACCESS['admin']

@login.user_loader
def load_user(id):
	print('Hit it')
	return User.query.get(int(id))

class Post(db.Model):
	__tablename__='posts'
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(250))
	category=db.Column(db.String(250))
	content=db.Column(db.String(65535))
	image_filename=db.Column(db.String, default=None, nullable=True)
	image_url=db.Column(db.String, default=None, nullable=True)
	timestamp=db.Column(db.Date, index=True, default=datetime.now().date())

	def __init__(self, title, category, content, image_filename=None, image_url=None):
		self.title = title
		self.category = category
		self.content = content
		self.image_url = image_url
		self.image_filename = image_filename

	def __repr__(self):
		# return "%s:\n %s\n\t -Ankul" % (self.title, self.content)
		return ("{}: {} \n\t -Ankul".format( self.title, self.category))
