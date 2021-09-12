# imports
from flask import (
  Blueprint,
  render_template,
  request as req,
  flash,
  redirect,
  url_for
)

from werkzeug.security import (
  generate_password_hash,
  check_password_hash
)

from flask_login import (
  login_user,
  login_required,
  logout_user,
  current_user
)

from . import db
from .models import Users
# imports

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if req.method == 'POST' :
		verify_login_data(req.form)

	return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if req.method == 'POST':
		if verify_signup_data(req.form):
			create_user(req.form)

	return render_template('signup.html')


# function to verify post parameters on signup form
# returns true if all fields passes
def verify_signup_data(formData) :
	email = formData.get('email')
	firstName = formData.get('firstName')
	password = formData.get('password')
	confirmPassword = formData.get('confirmPassword')

	user = Users.query.filter_by(email=email).first()

	if user :
		flash(
			'Email already exists in database.',
			category='success'
		)
		return False
	elif len(email) == 0 :
		flash(
			'Email is required.',
			category='error'
		)
		return False
	elif len(firstName) < 3 :
		flash(
			'First Name must be greater than 2 characters.',
			category='error'
		)
		return False
	elif len(password) < 8 :
		flash(
			'Password must be at least 8 characters.',
			category='error'
		)
		return False
	elif password != confirmPassword :
		flash(
			'Passwords don \'t match!',
			category='error'
		)
		return False
	else :
		return True


# function to save a new user in database
def create_user(formData) :
	email = formData.get('email')
	firstName = formData.get('firstName')
	password = formData.get('password')

	# create user data
	new_user = Users(
		email=email,
		first_name=firstName,
			password=generate_password_hash(password, method='sha256')
	)

	# save user data in database
	db.session.add(new_user)
	db.session.commit()

	# show success message
	flash(
		'Account created!',
		category='success'
	)

	# redirect to the home page
	return redirect(url_for('views.home'))


# function to verify login
def verify_login_data(formData) :
	email = formData.get('email')
	password = formData['password']

	# get a user by provided email address
	user = Users.query.filter_by(email=email).first()

	if user :
		if check_password_hash(user.password, password) :
			flash(
					'Logged in successfully!',
					category='success'
			)

			login_user(
				user,
				remember=True
			)

			# redirect to home page
			return redirect(url_for('views.home'))
		else :
			flash(
				'Incorrect email and password combination.',
				category='error'
			)
	else :
		flash(
			'Email does not exist.',
			category='error'
		)
