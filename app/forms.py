from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class SignupForm(FlaskForm):
    FirstName = StringField('Username', validators=[InputRequired()])
    LastName = StringField('Username', validators=[InputRequired()])
    email = EmailField('Email address', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    agree = BooleanField()
