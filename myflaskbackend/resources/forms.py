from flask import render_template, make_response
from flask_restful import Resource
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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


class RegistrationPage(Resource):
    def get(self):
        form = RegistrationForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('registration.html', form=form), 200, headers)


class LoginPage(Resource):
    def get(self):
        form = LoginForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html', form=form), 200, headers)
