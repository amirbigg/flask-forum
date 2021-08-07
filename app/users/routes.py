from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.users.models import User, Code, Follow
from app.users.forms import UserRegistrationForm, UserCodeVerifyForm, UserLoginForm, EmptyForm
from app.extensions import db, sms_api
from flask_login import login_user, logout_user, current_user
import random
import datetime


blueprint = Blueprint('users', __name__)


@blueprint.route('/register', methods=['post', 'get'])
def register():
	form = UserRegistrationForm()
	if form.validate_on_submit():
		rand_num = random.randint(1000, 9999)
		session['user_phone'] = form.phone.data
		params = {'sender':'', 'receptor':int(form.phone.data), 'message':rand_num}
		sms_api.sms_send(params)
		code = Code(
					number=rand_num,
					expire=datetime.datetime.now() + datetime.timedelta(minutes=10),
					phone=form.phone.data
					)
		db.session.add(code)
		db.session.commit()
		return redirect(url_for('users.verify'))
	return render_template('users/register.html', form=form)


@blueprint.route('/verify', methods=['post', 'get'])
def verify():
	user_phone = session.get('user_phone')
	code = Code.query.filter_by(phone=user_phone).first()
	form = UserCodeVerifyForm()
	if form.validate_on_submit():
		if code.expire < datetime.datetime.now():
			flash('Expiration Error, please try again', 'danger')
			return redirect('users.register')

		if form.code.data != str(code.number):
			flash('your code is wrong', 'danger')
		else:
			user = User(phone=user_phone)
			db.session.add(user)
			db.session.commit()
			flash('your account created successfully', 'info')
			return redirect('/')
	return render_template('users/verify.html', form=form)


@blueprint.route('/login', methods=['post', 'get'])
def login():
	form = UserLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(phone=form.phone.data).first()
		login_user(user)
		flash('you logged in')
		return redirect('/')
	return render_template('users/login.html', form=form)


@blueprint.route('/logout', methods=['get', 'post'])
def logout():
	logout_user()
	flash('you logged out')
	return redirect('/')


@blueprint.route('/profile')
def profile():
	return render_template('users/profile.html')


@blueprint.route('/user/<int:id>')
def user(id):
	following = False
	user = User.query.get_or_404(id)
	form = EmptyForm()
	relation = Follow.query.filter_by(follower=current_user.id, followed=user.id).first()
	if relation:
		following = True
	return render_template('users/user.html', user=user, form=form, following=following)


@blueprint.route('/follow/<int:user_id>', methods=['post'])
def follow(user_id):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=user_id).first()
		if user is None:
			flash('User Not Found', 'danger')
			return redirect('/')
		if user == current_user:
			flash('you cant follow yourself', 'info')
			return redirect('/')
		relation = Follow(follower=current_user.id, followed=user.id)
		db.session.add(relation)
		db.session.commit()
		flash(f'you followed {user.phone}', 'info')
		return redirect(url_for('users.user', id=user.id))
	return redirect('/')


@blueprint.route('/unfollow/<int:user_id>', methods=['post'])
def unfollow(user_id):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=user_id).first()
		if user is None:
			flash('User not found', 'danger')
			return redirect('/')
		if user == current_user:
			flash('you cant unfollow yourself', 'danger')
			return redirect('/')
		relation = Follow.query.filter_by(follower=current_user.id, followed=user.id).first()
		db.session.delete(relation)
		db.session.commit()
		flash(f'you unfollowed {user.phone}', 'info')
		return redirect(url_for('users.user', id=user.id))
	return redirect('/')
