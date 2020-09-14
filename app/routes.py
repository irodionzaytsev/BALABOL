from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RegistrationForm, SearchUserForm, SendMessageForm
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Chat, Message
from app import db
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dialogues', methods=['GET','POST'])
@login_required
def dialogues():
    user = User.query.get(int(current_user.get_id()))
    chats = user.chats
    contacts = []
    for chat in chats:
        for contact in chat.users:
            if contact.username != user.username:
                contacts.append({"username" : contact.username, "chat" : chat.id})
    form = SearchUserForm()
    if form.validate_on_submit():
        contact = User.query.filter_by(username=form.username.data).first()
        for chat in chats:
            for user in chat.users:
                if user.username == contact.username:
                    return redirect("{}?chat={}".format(url_for('messages'), chat.id))
        new_chat = Chat(users=[user, contact])
        db.session.add(new_chat)
        db.session.commit()
        return redirect("{}?chat={}".format(url_for('messages'), new_chat.id))
    return render_template('dialogues.html', contacts=contacts, form=form)

@app.route('/messages', methods=['GET','POST'])
@login_required
def messages():
    try:
        chat_id = int(request.args.get('chat'))
        chat = Chat.query.get(chat_id)
        form = SendMessageForm()
        if form.validate_on_submit():
            user = User.query.get(int(current_user.get_id()))
            message = Message(message=form.message.data, sent_from=user, chat=chat)
            db.session.add(message)
            db.session.commit()
        messages = []
        for message in chat.messages:
            messages.append({'author':message.sent_from.username, 'text':message.message})
        return render_template('messages.html', form=form, messages=messages)
    except Exception as e:
        print(e)
        return redirect(url_for('dialogues'))

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

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        print(user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
    

