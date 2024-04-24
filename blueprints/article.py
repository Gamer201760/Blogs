from datetime import datetime

import markdown
from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required

from data import db_session
from data.article import Article
from forms.article import ArticleForm

bp = Blueprint('articles', __name__, template_folder='templates', url_prefix='/article')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def article():
	form = ArticleForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		obj = Article()
		obj.user_id = current_user.id
		obj.title = form.title.data
		obj.text = form.text.data
		obj.img_url = form.preview_img.data
		obj.read_time = form.read_time.data
		obj.relase_date = datetime.now()
		db_sess.add(obj)
		db_sess.commit()
		return redirect(f'/article/{obj.id}')
	return render_template('article.html', title='Статья', form=form)


@bp.route('/<int:id>', methods=['GET'])
def get(id: int):
	db_sess = db_session.create_session()
	article = db_sess.get(Article, id)
	if article is None:
		return redirect('/')
	return render_template(
		'view_article.html',
		article=article,
		text=markdown.markdown(
			article.text, extensions=['nl2br'], output_format='html'
		),
	)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id: int):
	if current_user.is_admin is False:
		return redirect('/')
	db_sess = db_session.create_session()
	obj = db_sess.get(Article, id)

	form = ArticleForm()
	if request.method == 'GET':
		form.title.data = obj.title
		form.text.data = obj.text
		form.read_time.data = obj.read_time

	form.read_time.validators = []
	form.title.validators = []
	form.text.validators = []
	form.preview_img.validators = []

	if form.validate_on_submit():
		if obj is None:
			return redirect('/')

		if form.title.data != obj.title:
			obj.title = form.title.data
		if form.text.data != obj.text:
			obj.text = form.text.data
		if form.preview_img.data != obj.img_url:
			obj.img_url = form.preview_img.data
		if form.read_time.data != obj.read_time:
			obj.read_time = form.read_time.data

		db_sess.merge(obj)
		db_sess.commit()
		return redirect(f'/article/{obj.id}')
	return render_template('article.html', title='Редактирование', form=form)


@bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id: int):
	if current_user.is_admin:
		db_sess = db_session.create_session()
		article = db_sess.get(Article, id)
		if article:
			db_sess.delete(article)
			db_sess.commit()
	return redirect('/')
