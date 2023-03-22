from flask_wtf import FlaskForm
from wtforms.validators import input_required, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField

class Signupform(FlaskForm):
    firstname = StringField('First Name', validators=[input_required(), Length(max=50)])
    lastname = StringField('Last Name', validators=[input_required(), Length(max=50)])
    username = StringField('Username: ', validators=[input_required(), Length(max=50)])
    email = EmailField('Email: ', validators=[input_required(), Length(max=50)])
    password = PasswordField('Password: ', validators=[input_required(), Length(max=50)])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[input_required(), Length(max=50)])
    password = PasswordField('Password', validators=[input_required(), Length(max=50)])
    remember = BooleanField('Remember')
    submit = SubmitField('Log In')