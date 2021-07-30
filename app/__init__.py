from flask import Flask

from app.users.routes import blueprint as users_blueprint
from app.posts.routes import blueprint as posts_blueprint
import app.exceptions as app_exception
from app.extensions import db, migrate


def register_blueprint(app):
	app.register_blueprint(users_blueprint)
	app.register_blueprint(posts_blueprint)

def register_error_handlers(app):
	app.register_error_handler(404, app_exception.page_not_found)
	app.register_error_handler(500, app_exception.server_error)


app = Flask(__name__)
register_blueprint(app)
register_error_handlers(app)
app.config.from_object('config.DevConfig')

db.init_app(app)

from app.users.models import User # is here due to circular_imports for migrate use
migrate.init_app(app, db)
