from flask import render_template, redirect, flash, url_for
from app.forms import LoginForm, RegistrationForm
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dialogues')
@login_required
def dialogues():
    return render_template('dialogues.html')

@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.password != form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dialogues'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    return render_template('register.html', form=form)
    

