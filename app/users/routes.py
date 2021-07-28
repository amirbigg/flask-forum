from flask import Blueprint
from app.users.models import User


blueprint = Blueprint('users', __name__)


@blueprint.route('/login')
def login():
	return 'Login page'