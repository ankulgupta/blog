from flask import render_template, redirect, request, flash, url_for
from app import blog
from forms import NewPost
from app import db
from db_base import db_session, init_db

init_db()

@blog.route('/')
@blog.route('/index')
def index():
	return render_template('index.html')

@blog.route('/about-me')
def about():
	return render_template('about.html')

@blog.route('/poems')
def poems():
	return render_template('poems.html')

@blog.route('/stories')
def stories():
	return render_template('stories.html')

@blog.route('/addnew', methods=['GET','POST'])
def addNew():
	post=NewPost(request.form)
	if request.method=='POST' and post.validate():
		print 'Success'
		blogpost=NewPost()
		save_changes(blogpost, post, isnew=True)
		return redirect(url_for('index'))
	else:
		print 'Fail'
		flash(post.errors)
	
	return render_template('newpost.html', form=post)


def save_changes(blogpost, form, isnew=False):
	blogpost.title=form.title.data
	blogpost.category=form.category.data
	blogpost.content=form.content.data

	if isnew:
		db_session.add(blogpost)

	db_session.commit()