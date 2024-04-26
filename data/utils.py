from flask_restful import abort

from data import db_session


def abort_if_not_found(id: int, obj):
	session = db_session.create_session()
	data = session.get(obj, id)
	if not data:
		abort(404, error=f'{obj.__name__} {id} not found')
	return data
