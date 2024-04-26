from flask_login import current_user, login_required
from flask_restful import Resource

from data import db_session
from data.article import Article
from data.utils import abort_if_not_found

from .parser import edit_parser, parser


class ArticleResource(Resource):
	def get(self, id: int):
		sess = db_session.create_session()
		return sess.get(Article, id).to_dict()

	@login_required
	def delete(self, id: int):
		if not current_user.is_admin:
			return {'error': 'You don`t have permissions'}
		abort_if_not_found(id, Article)
		sess = db_session.create_session()
		sess.delete(sess.get(Article, id))
		sess.commit()
		return {'success': 'ok'}

	@login_required
	def put(self, id: int):
		if not current_user.is_admin:
			return {'error': 'You don`t have permissions'}
		abort_if_not_found(id, Article)
		sess = db_session.create_session()
		article = sess.get(Article, id)
		args = edit_parser.parse_args()

		if args['title']:
			article.title = args['title']
		if args['text']:
			article.text = args['text']
		if args['img_url']:
			article.img_url = args['img_url']
		if args['read_time']:
			article.read_time = args['read_time']

		sess.commit()
		return {'success': 'ok'}


class ArticleListResource(Resource):
	def get(self):
		sess = db_session.create_session()
		return list(
			map(lambda x: x.to_dict(rules=('-img_url',)), sess.query(Article).all())
		)

	@login_required
	def post(self):
		if not current_user.is_admin:
			return {'error': 'You don`t have permissions'}
		sess = db_session.create_session()

		args = parser.parse_args()
		article = Article()
		article.title = args['title']
		article.text = args['text']
		article.img_url = args['img_url']
		article.read_time = args['read_time']
		sess.add(article)
		sess.commit()
		return {'id': article.id}
