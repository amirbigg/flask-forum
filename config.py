import os


class Config:
	BASE_DIR = os.path.abspath(os.path.dirname(__file__))
	CSRF_ENABLED = True
	CSRF_SESSION_KEY = '9636f726106502d39b365ff821c97f1f2957abc343081e9769462423f88fa91d'
	SECRET_KEY = '8c717e5691f9bb75558cbd8dfad5688f179a9ad86e2f82b1fedd698fba9b55cb'


class ProdConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = ...


class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'app.db')