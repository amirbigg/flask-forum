from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from kavenegar import KavenegarAPI
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
sms_api = KavenegarAPI('Your Kavenegar Api Key')
login_manager = LoginManager()
