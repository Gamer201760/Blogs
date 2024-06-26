import sqlalchemy
import sqlalchemy.orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Article(SqlAlchemyBase, SerializerMixin):
	__tablename__ = 'article'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	title = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
	text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
	img_url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
	read_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
	relase_date = sqlalchemy.Column(
		sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()
	)
