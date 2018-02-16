from datetime import datetime 
from app import db

class Post(db.Model):
	__tablename__='posts'
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(250))
	category=db.Column(db.String(250))
	content=db.Column(db.String(65535))
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow())

	def __repr__(self):
		return '{}: \n{}\n\t -Ankul'.format(self.title, self.content)
