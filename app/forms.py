from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class NewPost(FlaskForm):
	title = StringField('Title')
	PostTypes=[('Poem','Poem'),('Story','Story')]
	category = SelectField('Category', choices=PostTypes)
	content = StringField('Content')
	submit = SubmitField('Submit')
