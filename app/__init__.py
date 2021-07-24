from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.users.routes import blueprint as users_blueprint
from app.posts.routes import blueprint as posts_blueprint


app = Flask(__name__)

app.config.from_object('config.DevConfig')

app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)

db = SQLAlchemy(app)
db.create_all()
