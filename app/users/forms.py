from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import ValidationError
from app.users.models import User, Code


class UserRegistrationForm(FlaskForm):
	phone = StringField('Phone')

	def validate_phone(self, phone):
		codes = Code.query.filter_by(phone=phone.data)
		if codes:
			Code.query.filter_by(phone=phone.data).delete()

		user = User.query.filter_by(phone=phone.data).first()
		if user:
			raise ValidationError('This phone already exists')



class UserCodeVerifyForm(FlaskForm):
	code = StringField('Code')