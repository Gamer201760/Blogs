from datetime import datetime

from flask import Blueprint, render_template
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
		return render_template('article.html', form=form)
	return render_template('article.html', title='Статья', form=form)
