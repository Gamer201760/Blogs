from flask import Blueprint, redirect, render_template
from flask_login import login_user

from data import db_session
from data.user import User
from forms.login import LoginForm
from forms.register import RegisterForm

bp = Blueprint('users', __name__, template_folder='templates')


@bp.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		user = db_sess.query(User).filter(User.username == form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember_me.data)
			return redirect('/')
		return render_template(
			'login.html', message='Неправильный логин или пароль', form=form
		)
	return render_template('login.html', title='Авторизация', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		if db_sess.query(User).filter(User.username == form.username.data).count() > 0:
			return render_template(
				'register.html',
				title='Регистрация',
				message='Пользователь с такой почтой уже существует',
				form=form,
			)
		user = User()
		user.email = form.email.data
		user.username = form.username.data
		user.role_id = 1
		user.set_password(form.password.data)
		try:
			db_sess.merge(user)
			db_sess.commit()
		except Exception:
			return render_template(
				'register.html',
				title='Регистрация',
				message='Не предвидинная ошибка',
				form=form,
			)
		return redirect('/login')
	return render_template('register.html', title='Регистрация', form=form)
