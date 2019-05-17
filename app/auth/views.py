# app/auth/views.py

from flask import flash, redirect, render_template, url_for, abort, Flask
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Participant,Workshop


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """
    Handle requests to the /signup route
    Add a participant to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        participant = Participant(firstname=form.firstname.data,
                              lastname=form.lastname.data,
                              username=form.username.data,
                              email=form.email.data,
                              password=form.password.data
                              )

        # add participant to the database
        db.session.add(participant)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/signup.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether participant exists in the database and whether
        # the password entered matches the password in the database
        participant=Participant.query.filter_by(email=form.email.data).first()
        if participant is not None and participant.verify_password(
                form.password.data):
            # log participant in
            login_user(participant)

            # redirect to the appropriate dashboard page
            if participant.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log a participant out through the logout link
    """
    logout_user()
    flash('You have successfully logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
