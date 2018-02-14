from flask import render_template, redirect, request, flash
from app import blog
from app.forms import NewPost

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
		return redirect(url_for('index'))
	else:
		print 'Fail'

	flash(post.errors)
	return render_template('newpost.html', form=post)
