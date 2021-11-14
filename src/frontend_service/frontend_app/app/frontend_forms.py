from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField, StringField, SelectField, RadioField, FieldList, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Email
import email_validator
import pycountry

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	submit = SubmitField('login')


class RegisterForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	first_name = StringField('firstname', validators=[DataRequired()])
	last_name = StringField('lastname', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Email()])
	submit = SubmitField('register')

class MultiCheck(SelectMultipleField):
	widget = widgets.TableWidget()
	option_widget = widgets.CheckboxInput()

class NewNote(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	description = StringField('description', validators=[DataRequired()])
	category = MultiCheck(None)
	country = SelectField('country', choices=[])
	city = StringField('city', validators=[DataRequired()])
	yt_link = FieldList(StringField('Youtube Link', validators=[DataRequired()]), min_entries=1, max_entries=10)
	fb_link = FieldList(StringField('Facebook Link', validators=[DataRequired()]), min_entries=1, max_entries=10)
	blog_link = FieldList(StringField('Blog Link', validators=[DataRequired()]), min_entries=1, max_entries=10)
	insta_link = FieldList(StringField('Instagram Link', validators=[DataRequired()]), min_entries=1, max_entries=10)
	gmap = StringField('gmap', validators=[DataRequired()])


class SelectForm(FlaskForm):
    country = SelectField('country', choices=[('Select', 'Select')])
    city = SelectField('city', choices=[('Select', 'Select')])