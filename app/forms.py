from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NewPost(FlaskForm):
	title = StringField('Title')
	PostTypes=[('Poem','Poem'),('Story','Story')]
	category = SelectField('Category', choices=PostTypes)
	content = TextAreaField('Content')
	submit = SubmitField('Submit')
