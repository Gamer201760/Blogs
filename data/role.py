import sqlalchemy
import sqlalchemy.orm

from .db_session import SqlAlchemyBase


class Role(SqlAlchemyBase):
	__tablename__ = 'role'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

	user = sqlalchemy.orm.relationship('User', back_populates='role')

	def __str__(self):
		return self.name
