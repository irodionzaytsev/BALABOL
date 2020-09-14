from app import db
from datetime import datetime
from flask_login import UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32),index=True, unique=True)
    password = db.Column(db.String(32))
    chats = db.relationship('Chat', secondary='link')
    def __repr__(self):
        return '<username: {} password: {}>'.format(self.username, self.password)
from app import login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class Link(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True)
    
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', secondary='link')
    messages = db.relationship('Message', backref='chat')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    sent_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sent_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sent_from = db.relationship("User", foreign_keys=[sent_from_id])
    sent_to = db.relationship('User', foreign_keys=[sent_to_id])
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Message: {}>'.format(self.message)
