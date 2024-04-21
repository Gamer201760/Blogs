from flask_restful import Resource

from data import db_session
from data.user import User
from data.utils import abort_if_not_found


class UserResource(Resource):
	def get(self, id: int):
		user: User = abort_if_not_found(id, User)
		return user.to_dict(rules=('-jobs', '-hashed_password'))

	def delete(self, id: int):
		abort_if_not_found(id, User)
		sess = db_session.create_session()
		user = sess.get(User, id)
		sess.delete(user)
		sess.commit()
		return {'success': 'ok'}
