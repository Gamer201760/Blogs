import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, make_response, redirect, render_template
from flask_login import LoginManager, login_required, logout_user

from blueprints import article, user
from data import db_session
from data.__all_models import *  # noqa: F403
from data.article import Article
from data.user import User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(365)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	return db_session.create_session().get(User, user_id)


def main():
	db_session.global_init('db/blogs.db')
	app.register_blueprint(user.bp)
	app.register_blueprint(article.bp)
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


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')


@app.route('/')
def index():
	return render_template(
		'index.html', articles=db_session.create_session().query(Article).all()
	)


if __name__ == '__main__':
	main()
