from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import images

class NewPost(FlaskForm):
	title = StringField('Title')
	PostTypes=[('Poem','Poem'),('Story','Story')]
	category = SelectField('Category', choices=PostTypes)
	content = TextAreaField('Content')
	submit = SubmitField('Submit')
	post_image = FileField('Post Image', validators=[FileAllowed(images, 'Image Only!')])