from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=100)])
	text = TextAreaField('Text', validators=[DataRequired()])
	preview_img = StringField('Preview img', validators=[DataRequired()])
	read_time = IntegerField('Read time', validators=[DataRequired()])
	submit = SubmitField('Sumbit')
