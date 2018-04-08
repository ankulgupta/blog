from flask import render_template, redirect, request, flash, url_for, abort
from app import blog, db, images
from forms import NewPost
from models import Base, Post
import math

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
	header = "Ankul Gupta"
	return render_template('about.html', page_title=page_title, page_subtitle=page_subtitle, title=header)

@blog.route('/poems', defaults={'page':1})
@blog.route('/poems/<int:page>')
def poems(page):
	# poems = db.session.query(Post).order_by(Post.timestamp.desc()).filter(Post.category == 'Poem').limit(10).all()
	post_count = db.session.query(Post).filter(Post.category=='Poem').count()
	page_count = (post_count/15) if ((post_count%15)==0) else ((post_count/15)+1)

	if page > page_count:
		abort(404)
	poems = db.session.query(Post).filter(Post.id <= post_count-(15*(page-1))).filter(Post.id > post_count-(15*page)).order_by(Post.id.desc())
	
	# page_count = math.ceil(float(post_count/15))
	print("Here post count is")
	print(post_count-(15*(page-1)))
	print(post_count-(15*page))
	page_title = "My Poems"
	if page == page_count:
		hasNext = None 
	else:
		hasNext = 1
	print(hasNext)
	return render_template('poems.html', records=poems, title=page_title, pageNum=(page+1), hasNext=hasNext)

@blog.route('/post/<int:record_id>')
def post(record_id):
	page_title="My Ideas My Space"
	post_obj = get_or_abort(record_id)
	return render_template('post.html', post_data=post_obj)

@blog.route('/stories', defaults={'page':1})
@blog.route('/stories/<int:page>')
def stories(page):
	post_count = db.session.query(Post).filter(Post.category=='Story').count()
	page_count = (post_count/15) if ((post_count%15)==0) else ((post_count/15)+1)

	if page>page_count:
		abort(404)
	# stories = db.session.query(Post).order_by(Post.timestamp.desc()).filter(Post.category == 'Story').limit(10).all()
	stories = db.session.query(Post).filter(Post.id <= post_count-(15*(page-1))).filter(Post.id > post_count-(15*page)).order_by(Post.id.desc())
	page_title = "My Stories"
	if page==page_count:
		hasNext = None
	else:
		hasNext = 1
	return render_template('stories.html', records=stories, title=page_title, pageNum=(page+1), hasNext=hasNext)

@blog.route('/addnew', methods=['GET','POST'])
def addNew():
	page_title="Grace this world with a new post, Sensei"
	post=NewPost()
	if request.method=='POST' and post.validate_on_submit():
		print 'Success'
		if 'post_image' not in request.files:
			flash('No Files')
			return 'no file found'
		filename=images.save(request.files['post_image'])
		url=images.url(filename)
		blogpost=Post(post.title.data, post.category.data, post.content.data, filename, url)
		print 'There'
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
		print('Posting data')

	db.session.commit()
	print("Checkpoint")

def get_or_abort(post_id):
	obj = db.session.query(Post).get(post_id)
	print("I dont see it")
	if obj is None:
		# print("No object found!")
		abort(404)
	return obj
