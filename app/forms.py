from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import images
from app.models import User

class NewPost(FlaskForm):
	title = StringField('Title')
	PostTypes=[('Poem','Poem'),('Story','Story')]
	category = SelectField('Category', choices=PostTypes)
	content = TextAreaField('Content')
	submit = SubmitField('Submit')
	post_image = FileField('Post Image', validators=[FileAllowed(images, 'Image Only!')])

class LoginForm(FlaskForm):
	email = StringField('Email')
	password = PasswordField('Password')
	submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[Email(), DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	# def validate_email(self, email):
	# 	user = User.query.filter_by(email=email.data).first()
	# 	if user is not None:
	# 		raise ValidationError('Please use a different email address')