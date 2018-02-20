from datetime import datetime 
from app import db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine=create_engine('sqlite:///blog_post.db')
db_session=scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

Base=declarative_base()
Base.query=db_session.query_property()


class Post(db.Model):
	__tablename__='posts'
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(250))
	category=db.Column(db.String(250))
	content=db.Column(db.String(65535))
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow())

	def __repr__(self):
		return '{}: \n{}\n\t -Ankul'.format(self.title, self.content)
