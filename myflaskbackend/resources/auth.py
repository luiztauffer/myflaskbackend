from flask import (request, make_response, current_app, render_template, flash,
                   redirect)
from flask_login import (login_required, logout_user, current_user, login_user,
                         UserMixin)
from flask_restful import Resource
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from werkzeug.security import generate_password_hash, check_password_hash
from myflaskbackend import login_manager


class RegistrationForm(FlaskForm):
    username_validators = [DataRequired(), Length(min=4, max=20)]
    username = StringField('Username', validators=username_validators)
    email_validators = [DataRequired(), Email()]
    email = StringField('Email', validators=email_validators)
    password_validators = [DataRequired(), Length(min=4, max=20)]
    password = PasswordField('Password', validators=password_validators)
    confirm_password_validators = [DataRequired(), EqualTo('password')]
    confirm_password = PasswordField('Confirm password', validators=confirm_password_validators)

    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email_validators = [DataRequired(), Email()]
    email = StringField('Email', validators=email_validators)
    password_validators = [DataRequired(), Length(min=4, max=20)]
    password = PasswordField('Password', validators=password_validators)

    submit = SubmitField('Login')


class Signup(Resource):
    """
    Signup for new users.
    """
    def get(self):
        form = RegistrationForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('signup.html', form=form), 200, headers)

    def post(self):
        form = request.form
        username = form['username']
        password = form['password']
        flash(f'Account created for {username}', 'success')
        return redirect('home')


class Login(Resource):
    """
    Login for registered users.

    $ curl -i -X POST -F -d "username=value1&password=value2" http://localhost:5000/login
    """
    def get(self):
        form = LoginForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html', form=form), 200, headers)

    def post(self):
        # Test if it is already logged in
        if current_user.is_authenticated:
            return print('User already logged in')

        # Load users credentials to compare with login attempts
        users_data_path = Path(__file__).parent.parent.absolute() / 'users_data.json'
        with open(users_data_path) as json_file:
            users_data = json.load(json_file)

        # Compare with user supplied credentials
        form = request.form
        user_name = form['username']
        user_pass = form['password']
        match_list = [user_name == user['user_name'] for user in users_data['all_users']]
        login_success = False
        if any(match_list):
            # If username is correct
            user_ind = match_list.index(True)
            if user_pass == users_data['all_users'][user_ind]['password']:
                # If password is also correct
                login_success = True

        if login_success:
            msg = f'Login successful! Welcome {user_name}!'
            print(msg)
            return make_response(msg, 200)
        else:
            msg = f'Login failed for user: {user_name}'
            print(msg)
            return make_response(msg, 401)


class Logout(Resource):
    """
    Logout current user.
    """
    method_decorators = [login_required]

    def logout():
        logout_user()
        return 'User logged out'


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))


# class User(UserMixin, db.Model):
#     """Model for user accounts."""
#
#     __tablename__ = 'flasklogin-users'
#
#     id = db.Column(db.Integer,
#                    primary_key=True)
#     name = db.Column(db.String,
#                      nullable=False,
#                      unique=False)
#     email = db.Column(db.String(40),
#                       unique=True,
#                       nullable=False)
#     password = db.Column(db.String(200),
#                          primary_key=False,
#                          unique=False,
#                          nullable=False)
#     website = db.Column(db.String(60),
#                         index=False,
#                         unique=False,
#                         nullable=True)
#     created_on = db.Column(db.DateTime,
#                            index=False,
#                            unique=False,
#                            nullable=True)
#     last_login = db.Column(db.DateTime,
#                            index=False,
#                            unique=False,
#                            nullable=True)
#
#     def set_password(self, password):
#         """Create hashed password."""
#         self.password = generate_password_hash(password, method='sha256')
#
#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password, password)
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)
