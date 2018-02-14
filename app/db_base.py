from app import db

class Post(db.Model):
	__tablename__='posts'
	id=db.Column(db.Integer, primary_key=true)
	title=db.Column(String(250))
	category=dm.Column(String(250))
	content=db.Column(String(65535))

	def __repr__(self):
		return '{}: \n{}\n\t -Ankul'.format(self.title, self.content)

engine=create_engine('sqlite:///blog_post.db')

Base.metadata.create_all(engine)