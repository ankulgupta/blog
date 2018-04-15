from flask import render_template, redirect, request, flash, url_for, abort
from app import blog, db, images
from forms import NewPost, LoginForm, RegistrationForm
from app.models import Base, Post, User, ACCESS
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import math

Base.metadata.drop_all(db.engine)
Base.metadata.create_all(db.engine)
# Post.__table__.create(db.engine)
# User.__table__.create(db.engine)
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

	page_title = "My Poems"
	if page == page_count:
		hasNext = None 
	else:
		hasNext = 1
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
@login_required
def addNew():
	if current_user.is_admin:
		page_title="Grace this world with a new post, Sensei"
		post=NewPost()
		if request.method=='POST' and post.validate_on_submit():
			if 'post_image' not in request.files:
				flash('No Files')
				return 'no file found'
			filename=images.save(request.files['post_image'])
			url=images.url(filename)
			blogpost=Post(post.title.data, post.category.data, post.content.data, filename, url)
			save_changes(blogpost, post, isnew=True)
			# return render_template('postData.html', form=post)
			return redirect(url_for('index'))
		else:
			flash(post.errors)
		
		return render_template('newpost.html', form=post, title=page_title)
	else:
		abort(404)

@blog.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated and current_user.is_admin():
		return redirect(url_for('addnew'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('index'))
		login_user(user)
		if user.is_admin():
			redirect(url_for('addNew'))

	return render_template('login.html', title="Sign In", form=form, page_heading="Sign In")

@blog.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated and current_user.is_admin():
		return redirect(url_for('addNew'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, access=1)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Registered')
		redirect(url_for('login'))

	return render_template('register.html', title="Register", form=form, page_heading="New User Registration")

def save_changes(blogpost, form, isnew=False):
	blogpost.title=form.title.data
	blogpost.category=dict(form.category.choices).get(form.category.data)
	blogpost.content=form.content.data

	if isnew:
		db.session.add(blogpost)

	db.session.commit()

def get_or_abort(post_id):
	obj = db.session.query(Post).get(post_id)
	if obj is None:
		# print("No object found!")
		abort(404)
	return obj
