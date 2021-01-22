from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class RegistrationForm(Form):
    username = StringField('Username', [Length(min=4, max=25)])
    password = PasswordField('Password', [DataRequired()])

class LoginForm(Form):
    username = StringField('Username', [Length(min=4, max=25)])
    password = PasswordField('Password', [DataRequired()])

class ChangePassword(Form):
    password = PasswordField('New Password', [DataRequired(), EqualTo(
        'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password')

class UsernameForm(Form):
    username = StringField('Username', [Length(min=4, max=25)])