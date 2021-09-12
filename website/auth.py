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

from . import db
from .models import Users
# imports

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')


@auth.route('/logout')
def logout():
	return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if req.method == 'POST':
		if verify_form_data(req.form) :
			create_user(req.form)

	return render_template('signup.html')


# function to verify post parameters
# returns true if all fields passes
def verify_form_data(formData) :
    email = formData.get('email')
    firstName = formData.get('firstName')
    password = formData.get('password')
    confirmPassword = formData.get('confirmPassword')

    if len(email) == 0 :
        flash(
        'Email is required',
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
		'Account created',
		category='success'
	)

	# redirect to the home page
	return redirect(url_for('views.home'))
