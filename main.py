from datetime import timedelta

from flask import Flask, make_response, redirect, render_template
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_restful import Api

from data import db_session
from data.__all_models import *  # noqa: F403
from data.user import User
from forms.login import LoginForm
from forms.register import RegisterForm
from resources import user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(365)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
api.add_resource(user.UserListResource, '/api/v2/user')
api.add_resource(user.UserResource, '/api/v2/user/<int:id>')


def main():
	db_session.global_init('db/blogs.db')
	app.run(debug=True, port=8080)


@app.errorhandler(404)
def not_found(_):
	return make_response({'error': 'Not found'}, 404)


@app.errorhandler(400)
def bad_request(_):
	return make_response({'error': 'Bad Request'}, 400)


@app.errorhandler(405)
def method_not_allowed(_):
	return make_response({'error': 'Method Not Allowed'}, 405)


@login_manager.user_loader
def load_user(user_id):
	return db_session.create_session().get(User, user_id)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/register', methods=['GET', 'POST'])
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


if __name__ == '__main__':
	main()
