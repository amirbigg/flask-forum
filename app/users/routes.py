from flask import Blueprint


blueprint = Blueprint('users', __name__)


@blueprint.route('/login')
def login():
	return 'Login page'