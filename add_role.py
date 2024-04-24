import data.__all_models  # noqa: F401
from data import db_session
from data.role import Role

db_session.global_init('db/blogs.db')
sess = db_session.create_session()

role = Role()
role.name = 'Customer'
sess.add(role)
sess.commit()
