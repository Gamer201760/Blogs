import sqlalchemy
import sqlalchemy.orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Role(SqlAlchemyBase, SerializerMixin):
	__tablename__ = 'role'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

	user = sqlalchemy.orm.relationship('User', back_populates='role')

	def __str__(self):
		return self.name
