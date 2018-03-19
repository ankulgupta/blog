from flask import render_template, redirect, request, flash, url_for
from app import blog, db
from forms import NewPost
from models import Base, Post


Base.metadata.drop_all(db.engine)
Base.metadata.create_all(db.engine)
db.session.commit()


@blog.route('/')
@blog.route('/index')
def index():
	page_title="My Ideas My Space"
	page_subtitle="Where I speak in a way I enjoy the most"
	records = db.session.query(Post).order_by(Post.timestamp.desc()).limit(5).all()
	return render_template('index.html', records=records, title=page_title, subheading=page_subtitle)

@blog.route('/about-me')
def about():
	page_title="About Me"
	page_subtitle="Who am I"
	return render_template('about.html', title=page_title, subtitle=page_subtitle)

@blog.route('/poems')
def poems():
	return render_template('poems.html')

@blog.route('/post/<int:record_id>')
def post(record_id):
	post_obj = get_or_abort(record_id)
	return render_template('post.html', post_data=post_obj)

@blog.route('/stories')
def stories():
	return render_template('stories.html')

@blog.route('/addnew', methods=['GET','POST'])
def addNew():
	page_title="Grace this world with a new post, Sensei"
	post=NewPost(request.form)
	if request.method=='POST' and post.validate():
		print 'Success'
		blogpost=Post()
		save_changes(blogpost, post, isnew=True)
		# return render_template('postData.html', form=post)
		return redirect(url_for('index'))
	else:
		print 'Fail'
		flash(post.errors)
	
	return render_template('newpost.html', form=post, title=page_title)


def save_changes(blogpost, form, isnew=False):
	# blogpost.id=1
	blogpost.title=form.title.data
	blogpost.category=dict(form.category.choices).get(form.category.data)
	blogpost.content=form.content.data

	if isnew:
		db.session.add(blogpost)

	db.session.commit()

def get_or_abort(post_id):
	obj = db.session.query(Post).get(post_id)
	print("I dont see it")
	if obj is None:
		# print("No object found!")
		abort(404)
	return obj
