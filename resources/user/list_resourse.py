from flask_restful import Resource, abort

from data import db_session
from data.user import User

from .parser import parser


class UserListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        user = sess.query(User).all()
        return [u.to_dict(only=('id', 'email', 'name', 'surname')) for u in user]

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        if sess.query(User).filter(User.email == args['email']).count() > 0:
            abort(400, message={'error': 'User already exists'})
        user = User()
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.set_password(args['password'])
        sess.add(user)
        sess.commit()
        return {'id': user.id}
