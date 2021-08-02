from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from kavenegar import KavenegarAPI
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
sms_api = KavenegarAPI('36577A39322F746556333677714F58442F6437584239485579676D683163386E746A2B78654832654149513D')
login_manager = LoginManager()