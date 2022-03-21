from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .. import models
from .forms import LoginForm, RegistrationForm

from functools import wraps

def requires_roles(*roles):
  def wrapper(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
      if current_user.get_role() not in roles:
        #Redirect the user to an unauthorized notice!
        return redirect(url_for('auth.login'))
      return f(*args, **kwargs)
    return wrapped
  return wrapper

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@requires_roles('doctor')
@auth.route('/registerPatient', methods=['GET', 'POST'])
def registerPatient():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.date_of_birth)
        patient = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    date_of_birth=form.date_of_birth.data,
                    email=form.email.data,
                    username=form.username.data,
                    role_id=2,
                    password=form.password.data)
        models.addPatient(patient)
        flash('Patient Created')
        return redirect(url_for('main.index'))
    return render_template('auth/registerPatient.html', form=form)
