# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Participant


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """

    firstname=StringField('First Name',validators=[DataRequired()])
    lastname=StringField('Last Name',validators=[DataRequired()])
    username=StringField('User Name',validators=[DataRequired()])
    email=StringField('Email Address',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('ConfirmPassword')])
    ConfirmPassword=PasswordField('Confirm Password')
    submit=SubmitField('Sign Up')


    def validate_email(self, field):
        if Participant.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Participant.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

