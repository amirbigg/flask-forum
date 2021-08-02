from app.database import BaseModel
from app.extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(BaseModel, UserMixin):
	username = db.Column(db.String(30), unique=True, nullable=True)
	email = db.Column(db.String(60), unique=True, nullable=True)
	phone = db.Column(db.String(11), unique=True, nullable=False)

	def __repr__(self):
		return f'{self.__class__.__name__} ({self.id}, {self.username})'


class Code(BaseModel):
	number = db.Column(db.Integer)
	expire = db.Column(db.DateTime, nullable=False)
	phone = db.Column(db.String(11), unique=True, nullable=False)

	def __repr__(self):
		return f'{self.__class__.__name__} ({self.phone}, {self.number})'
