from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import User
from flask_login import current_user
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Invalid username')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username already exists')

class SearchUserForm(FlaskForm):
    username = StringField('Search user', validators=[DataRequired()])
    submit = SubmitField('Search')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('user not found')
        elif user == User.query.get(int(current_user.get_id())):
            raise ValidationError("can't create a chat with yourself")

class SendMessageForm(FlaskForm):
    message = StringField('Send message', validators=[DataRequired()])
    submit = SubmitField('Send')
