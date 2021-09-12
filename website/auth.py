from flask import (
  Blueprint,
  render_template,
  request as req,
  flash
)

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
		email = req.form.get('email')
		firstName = req.form.get('firstName')
		password = req.form.get('password')
		confirmPassword = req.form.get('confirmPassword')

		if len(email) == 0 :
			flash(
				'Email is required',
				category='error'
			)

		elif len(firstName) < 3:
			flash(
				'First Name must be greater than 2 characters.',
				category='error'
    	)

		elif len(password) < 8:
			flash(
				'Password must be at least 8 characters.',
				category='error'
			)

		elif password != confirmPassword:
			flash(
     		'Passwords don \'t match!',
				category='error'
    	)

		else:
			flash(
				'Account created',
				category='success'
			)

	return render_template('signup.html')
