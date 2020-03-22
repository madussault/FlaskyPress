"""Contains the routes involved in the authentication process.
"""

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm
from app.auth import bp
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from app import db


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """The route a user go to register as the blog admin.
    """
    title = 'Register'
    if User.query.first():
        flash("Someone has already registered as the owner of this blog and as"
              " a result no more registration are accepted.", 'info')
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.set_password(form.pass_field1.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered as the sole user of this blog.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=title, form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """The route a user go to log into the app.
    """
    title = 'Sign In'
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.index'))
    user = User.query.first()
    if not user:
        flash('You need to register before using the functionality of '
              'this blog.', 'warning')
        return redirect(url_for('auth.register'))
    form = LoginForm()
    if form.validate_on_submit():
        if user.check_password(form.pass_field.data):
            login_user(user, remember=form.remember_me.data)
            # or request.form.get('next')
            next_page = request.args.get('next')
            flash('You are now logged in.', 'success')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Incorrect password.', 'danger')
    return render_template('auth/login.html', form=form, title=title)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """The route a user go to log out of the app.
    """
    title = 'Log out'
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('auth/logout.html', title=title)
