import data.__all_models  # noqa: F401
from data import db_session
from data.user import User

db_session.global_init('db/blogs.db')
sess = db_session.create_session()

sess.get(User, 3).role_id = 1

sess.commit()
