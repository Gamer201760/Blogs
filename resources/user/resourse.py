from flask_login import current_user, login_required
from flask_restful import Resource, abort
from sqlalchemy import or_

from data import db_session
from data.user import User
from data.utils import abort_if_not_found

from .parser import parser


class UserResource(Resource):
	@login_required
	def get(self):
		obj: dict = current_user.to_dict(
			rules=('-role', '-role_id', '-article', '-hashed_password')
		)
		obj['role'] = current_user.role.name
		return obj

	@login_required
	def delete(self):
		abort_if_not_found(current_user.id, User)
		sess = db_session.create_session()
		sess.delete(sess.get(User, current_user.id))
		sess.commit()
		return {'success': 'ok'}


class UserListResource(Resource):
	def post(self):
		args = parser.parse_args()
		db_sess = db_session.create_session()
		if (
			db_sess.query(User)
			.filter(or_(User.username == args['username'], User.email == args['email']))
			.count()
			> 0
		):
			abort(400, message={'error': 'User already exists'})

		user = User()
		user.email = args['email']
		user.username = args['username']
		user.set_password(args['password'])
		db_sess.add(user)
		db_sess.commit()
		return {'id': user.id}
