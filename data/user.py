import sqlalchemy
import sqlalchemy.orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
	__tablename__ = 'user'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
	username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
	hashed_password = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
	role_id = sqlalchemy.Column(
		sqlalchemy.Integer, sqlalchemy.ForeignKey('role.id'), nullable=False
	)

	role = sqlalchemy.orm.relationship('Role', back_populates='user')

	def set_password(self, password: str):
		self.hashed_password = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		return check_password_hash(self.hashed_password, password)
