from flask import Blueprint


blueprint = Blueprint('posts', __name__)


@blueprint.route('/posts')
def posts():
	return 'POSTS'