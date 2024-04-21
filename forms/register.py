from flask_wtf import FlaskForm
from wtforms import (
	EmailField,
	PasswordField,
	StringField,
	SubmitField,
)
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
	email = EmailField('Email', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			EqualTo('password_repeat', message='Passwords must match'),
		],
	)
	password_repeat = PasswordField('Repeat password', validators=[DataRequired()])
	submit = SubmitField('Login')
